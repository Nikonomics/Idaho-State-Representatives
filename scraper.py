import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re
from models import Representative, Contact, Party, Chamber, HouseSeat, Committee

class IdahoLegislatureScraper:
    BASE_URL = "https://legislature.idaho.gov"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def scrape_senate_members(self) -> List[Representative]:
        """Scrape all Senate members from the membership page"""
        url = f"{self.BASE_URL}/senate/membership/"
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
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
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
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
        """Get all legislators and committees"""
        return {
            'senators': self.scrape_senate_members(),
            'representatives': self.scrape_house_members(),
            'committees': self.scrape_committees()
        }