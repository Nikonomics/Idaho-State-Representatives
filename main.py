#!/usr/bin/env python3

import argparse
import json
import os
from typing import List, Optional, Dict
from dotenv import load_dotenv
from scraper import IdahoLegislatureScraper
from analyzer import RepresentativeAnalyzer
from models import Representative, Chamber

# Load environment variables
load_dotenv()

class IdahoRepsTool:
    def __init__(self):
        self.scraper = IdahoLegislatureScraper()
        api_key = os.getenv('OPENAI_API_KEY')
        self.analyzer = RepresentativeAnalyzer(api_key=api_key)
        self.data = None
    
    def load_data(self):
        """Load representative and committee data"""
        print("Loading Idaho legislature data...")
        self.data = self.scraper.get_all_data()
        print(f"Loaded {len(self.data['senators'])} senators and {len(self.data['representatives'])} house members")
    
    def find_my_representatives(self, district: int) -> Dict:
        """Find representatives for a specific district"""
        if not self.data:
            self.load_data()
        
        district_reps = {
            'senate': None,
            'house': []
        }
        
        # Find Senate representative
        for senator in self.data['senators']:
            if senator.district == district:
                district_reps['senate'] = senator
                break
        
        # Find House representatives (usually 2 per district)
        for rep in self.data['representatives']:
            if rep.district == district:
                district_reps['house'].append(rep)
        
        return district_reps
    
    def analyze_problem(self, problem_description: str):
        """Analyze a problem and recommend action"""
        if not self.data:
            self.load_data()
        
        all_reps = self.data['senators'] + self.data['representatives']
        analysis = self.analyzer.analyze_problem(problem_description, all_reps)
        
        print(f"\nPROBLEM ANALYSIS")
        print(f"Problem: {analysis.problem_description}")
        print(f"\nRecommended Committees:")
        for committee in analysis.recommended_committees:
            print(f"  - {committee}")
        
        print(f"\nTarget Representatives:")
        for rep in analysis.target_representatives[:5]:  # Show top 5
            print(f"  - {rep.name} (District {rep.district}, {rep.chamber.value})")
        
        print(f"\nStrategy: {analysis.strategy}")
        
        print(f"\nTalking Points:")
        for point in analysis.talking_points:
            print(f"  - {point}")
    
    def analyze_representative(self, name: str):
        """Perform deep analysis on a representative"""
        if not self.data:
            self.load_data()
        
        # Find the representative
        all_reps = self.data['senators'] + self.data['representatives']
        target_rep = None
        
        for rep in all_reps:
            if name.lower() in rep.name.lower():
                target_rep = rep
                break
        
        if not target_rep:
            print(f"Representative '{name}' not found.")
            return
        
        analysis = self.analyzer.analyze_representative(target_rep)
        
        print(f"\nREPRESENTATIVE ANALYSIS: {analysis.representative.name}")
        print(f"District: {analysis.representative.district}")
        print(f"Chamber: {analysis.representative.chamber.value}")
        print(f"Party: {analysis.representative.party.value}")
        
        print(f"\nBackground: {analysis.background_summary}")
        
        print(f"\nKey Issues:")
        for issue in analysis.key_issues:
            print(f"  - {issue}")
        
        print(f"\nPolitical Positions:")
        for topic, position in analysis.political_positions.items():
            print(f"  - {topic}: {position}")
        
        print(f"\nSeat Risk Score: {analysis.seat_risk_score}/10")
        print(f"Likely Challengers: {', '.join(analysis.likely_challengers)}")
    
    def list_committees(self):
        """List all committees and their members"""
        if not self.data:
            self.load_data()
        
        print("\nIDAHO LEGISLATIVE COMMITTEES")
        for committee in self.data['committees']:
            print(f"\n{committee.name} ({committee.chamber.value})")
            if committee.chair:
                print(f"  Chair: {committee.chair}")
            if committee.members:
                print(f"  Members: {', '.join(committee.members)}")

def main():
    parser = argparse.ArgumentParser(description='Idaho Representatives Contact Tool')
    parser.add_argument('--district', type=int, help='Find representatives for district number')
    parser.add_argument('--problem', type=str, help='Describe a problem to get committee recommendations')
    parser.add_argument('--analyze', type=str, help='Analyze a specific representative')
    parser.add_argument('--committees', action='store_true', help='List all committees')
    
    args = parser.parse_args()
    
    tool = IdahoRepsTool()
    
    if args.district:
        reps = tool.find_my_representatives(args.district)
        print(f"\nREPRESENTATIVES FOR DISTRICT {args.district}")
        
        if reps['senate']:
            senator = reps['senate']
            print(f"\nSenator: {senator.name} ({senator.party.value})")
            print(f"Email: {senator.contact.email}")
            if senator.contact.statehouse_phone:
                print(f"Phone: {senator.contact.statehouse_phone}")
        
        print(f"\nHouse Representatives:")
        for rep in reps['house']:
            print(f"  {rep.name} ({rep.party.value}) - Seat {rep.house_seat.value if rep.house_seat else 'Unknown'}")
            print(f"  Email: {rep.contact.email}")
            if rep.contact.statehouse_phone:
                print(f"  Phone: {rep.contact.statehouse_phone}")
    
    elif args.problem:
        tool.analyze_problem(args.problem)
    
    elif args.analyze:
        tool.analyze_representative(args.analyze)
    
    elif args.committees:
        tool.list_committees()
    
    else:
        print("Idaho Representatives Contact Tool")
        print("Usage examples:")
        print("  python main.py --district 15")
        print("  python main.py --problem 'Need better funding for rural schools'")
        print("  python main.py --analyze 'John Smith'")
        print("  python main.py --committees")

if __name__ == "__main__":
    main()