import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re
import time
import json
import os
from datetime import datetime, timedelta
from models import Representative, Contact, Party, Chamber, HouseSeat, Committee

class IdahoLegislatureScraper:
    BASE_URL = "https://legislature.idaho.gov"
    CACHE_FILE = "cache.json"
    CACHE_DURATION_HOURS = 1
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session.headers.update(self.headers)
    
    def _load_cache(self) -> Optional[Dict]:
        """Load cached data if it exists and is fresh"""
        try:
            if os.path.exists(self.CACHE_FILE):
                with open(self.CACHE_FILE, 'r') as f:
                    cache_data = json.load(f)
                
                cache_time = datetime.fromisoformat(cache_data.get('timestamp', ''))
                if datetime.now() - cache_time < timedelta(hours=self.CACHE_DURATION_HOURS):
                    print(f"Using cached data from {cache_time}")
                    
                    # Convert dictionaries back to objects
                    cached_dict_data = cache_data.get('data', {})
                    return {
                        'senators': [self._dict_to_rep(rep_dict) for rep_dict in cached_dict_data.get('senators', [])],
                        'representatives': [self._dict_to_rep(rep_dict) for rep_dict in cached_dict_data.get('representatives', [])],
                        'committees': [self._dict_to_committee(committee_dict) for committee_dict in cached_dict_data.get('committees', [])]
                    }
        except Exception as e:
            print(f"Error loading cache: {e}")
        return None
    
    def _save_cache(self, data: Dict):
        """Save data to cache with timestamp"""
        try:
            # Convert Representative objects to dictionaries for JSON serialization
            serializable_data = {
                'senators': [self._rep_to_dict(rep) for rep in data['senators']],
                'representatives': [self._rep_to_dict(rep) for rep in data['representatives']],
                'committees': [self._committee_to_dict(committee) for committee in data['committees']]
            }
            
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'data': serializable_data
            }
            with open(self.CACHE_FILE, 'w') as f:
                json.dump(cache_data, f, indent=2)
            print("Data cached successfully")
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def _rep_to_dict(self, rep: Representative) -> Dict:
        """Convert Representative object to dictionary"""
        return {
            'name': rep.name,
            'party': rep.party.value,
            'district': rep.district,
            'chamber': rep.chamber.value,
            'house_seat': rep.house_seat.value if rep.house_seat else None,
            'contact': {
                'email': rep.contact.email,
                'home_phone': rep.contact.home_phone,
                'business_phone': rep.contact.business_phone,
                'statehouse_phone': rep.contact.statehouse_phone,
                'mailing_address': rep.contact.mailing_address
            },
            'occupation': rep.occupation,
            'term_number': rep.term_number,
            'committees': rep.committees,
            'bio': rep.bio
        }
    
    def _committee_to_dict(self, committee: Committee) -> Dict:
        """Convert Committee object to dictionary"""
        return {
            'name': committee.name,
            'chamber': committee.chamber.value,
            'chair': committee.chair,
            'vice_chair': committee.vice_chair,
            'members': committee.members
        }
    
    def _dict_to_rep(self, rep_dict: Dict) -> Representative:
        """Convert dictionary back to Representative object"""
        contact = Contact(
            email=rep_dict['contact']['email'],
            home_phone=rep_dict['contact'].get('home_phone'),
            business_phone=rep_dict['contact'].get('business_phone'),
            statehouse_phone=rep_dict['contact'].get('statehouse_phone'),
            mailing_address=rep_dict['contact'].get('mailing_address')
        )
        
        return Representative(
            name=rep_dict['name'],
            party=Party(rep_dict['party']),
            district=rep_dict['district'],
            chamber=Chamber(rep_dict['chamber']),
            contact=contact,
            occupation=rep_dict.get('occupation'),
            term_number=rep_dict.get('term_number'),
            house_seat=HouseSeat(rep_dict['house_seat']) if rep_dict.get('house_seat') else None,
            committees=rep_dict.get('committees', []),
            bio=rep_dict.get('bio')
        )
    
    def _dict_to_committee(self, committee_dict: Dict) -> Committee:
        """Convert dictionary back to Committee object"""
        return Committee(
            name=committee_dict['name'],
            chamber=Chamber(committee_dict['chamber']),
            chair=committee_dict.get('chair'),
            vice_chair=committee_dict.get('vice_chair'),
            members=committee_dict.get('members', [])
        )
    
    def _make_request(self, url: str) -> Optional[BeautifulSoup]:
        """Make a request with error handling and rate limiting"""
        try:
            print(f"Fetching: {url}")
            time.sleep(3)  # Rate limiting
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def scrape_senate_members(self) -> List[Representative]:
        """Scrape all Senate members from the membership page"""
        url = f"{self.BASE_URL}/senate/membership/"
        soup = self._make_request(url)
        
        if not soup:
            return []
        
        senators = []
        # Find member cards or entries
        member_elements = soup.find_all('div', class_='member-card') or soup.find_all('tr')
        
        for element in member_elements:
            senator = self._parse_member_data(element, Chamber.SENATE)
            if senator:
                senators.append(senator)
        
        return senators
    
    def scrape_house_members(self) -> List[Representative]:
        """Scrape all House members from the membership page"""
        url = f"{self.BASE_URL}/house/membership/"
        soup = self._make_request(url)
        
        if not soup:
            return []
        
        representatives = []
        member_elements = soup.find_all('div', class_='member-card') or soup.find_all('tr')
        
        for element in member_elements:
            rep = self._parse_member_data(element, Chamber.HOUSE)
            if rep:
                representatives.append(rep)
        
        return representatives
    
    def _parse_member_data(self, element, chamber: Chamber) -> Optional[Representative]:
        """Parse individual member data from HTML element"""
        try:
            # Extract text content
            text = element.get_text(strip=True)
            
            # Parse name
            name_match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', text)
            if not name_match:
                return None
            name = name_match.group(1)
            
            # Parse party
            party = Party.REPUBLICAN if '(R)' in text else Party.DEMOCRAT
            
            # Parse district
            district_match = re.search(r'District (\d+)', text)
            if not district_match:
                return None
            district = int(district_match.group(1))
            
            # Parse house seat if applicable
            house_seat = None
            if chamber == Chamber.HOUSE:
                seat_match = re.search(r'Seat ([AB])', text)
                if seat_match:
                    house_seat = HouseSeat.A if seat_match.group(1) == 'A' else HouseSeat.B
            
            # Parse contact info
            email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', text)
            email = email_match.group(1) if email_match else ""
            
            # Parse phone numbers
            phone_matches = re.findall(r'(\(\d{3}\) \d{3}-\d{4})', text)
            home_phone = phone_matches[0] if len(phone_matches) > 0 else None
            statehouse_phone = phone_matches[1] if len(phone_matches) > 1 else None
            
            # Parse occupation
            occupation_match = re.search(r'Occupation: ([^,\n]+)', text)
            occupation = occupation_match.group(1) if occupation_match else None
            
            contact = Contact(
                email=email,
                home_phone=home_phone,
                statehouse_phone=statehouse_phone
            )
            
            return Representative(
                name=name,
                party=party,
                district=district,
                chamber=chamber,
                contact=contact,
                occupation=occupation,
                house_seat=house_seat
            )
            
        except Exception as e:
            print(f"Error parsing member data: {e}")
            return None
    
    def scrape_committees(self) -> List[Committee]:
        """Scrape all committees and their membership"""
        committees = []
        
        # Scrape Senate committees
        senate_committees = self._scrape_chamber_committees("senate")
        committees.extend(senate_committees)
        
        # Scrape House committees
        house_committees = self._scrape_chamber_committees("house")
        committees.extend(house_committees)
        
        return committees
    
    def _scrape_chamber_committees(self, chamber: str) -> List[Committee]:
        """Scrape committees for a specific chamber"""
        committees = []
        chamber_enum = Chamber.SENATE if chamber == "senate" else Chamber.HOUSE
        
        # This would need to be implemented based on the actual committee page structure
        # For now, returning empty list as placeholder
        return committees
    
    def get_all_data(self) -> Dict:
        """Get all legislators and committees with caching"""
        # Check cache first
        cached_data = self._load_cache()
        if cached_data:
            return cached_data
        
        print("Cache expired or missing, scraping fresh data...")
        
        try:
            data = {
                'senators': self.scrape_senate_members(),
                'representatives': self.scrape_house_members(),
                'committees': self.scrape_committees()
            }
            
            # Save to cache
            self._save_cache(data)
            return data
            
        except Exception as e:
            print(f"Error scraping data: {e}")
            
            # Try to return cached data even if expired
            try:
                if os.path.exists(self.CACHE_FILE):
                    with open(self.CACHE_FILE, 'r') as f:
                        cache_data = json.load(f)
                    print("Website unavailable, using cached data")
                    return cache_data.get('data', {})
            except:
                pass
            
            # Return minimal fallback data
            print("No cached data available, returning empty data")
            return {
                'senators': [],
                'representatives': [],
                'committees': []
            }