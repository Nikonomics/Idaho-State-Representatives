from dataclasses import dataclass
from typing import List, Optional, Dict
from enum import Enum

class Party(Enum):
    REPUBLICAN = "R"
    DEMOCRAT = "D"

class Chamber(Enum):
    HOUSE = "House"
    SENATE = "Senate"

class HouseSeat(Enum):
    A = "A"
    B = "B"

@dataclass
class Contact:
    email: str
    home_phone: Optional[str] = None
    business_phone: Optional[str] = None
    statehouse_phone: Optional[str] = None
    mailing_address: Optional[str] = None

@dataclass
class Committee:
    name: str
    chamber: Chamber
    chair: Optional[str] = None
    vice_chair: Optional[str] = None
    members: List[str] = None

@dataclass
class Representative:
    name: str
    party: Party
    district: int
    chamber: Chamber
    contact: Contact
    occupation: Optional[str] = None
    term_number: Optional[int] = None
    house_seat: Optional[HouseSeat] = None  # Only for House members
    committees: List[str] = None
    bio: Optional[str] = None
    
    def __post_init__(self):
        if self.committees is None:
            self.committees = []

@dataclass
class District:
    number: int
    house_reps: List[Representative]
    senate_rep: Representative
    
@dataclass
class ProblemAnalysis:
    problem_description: str
    recommended_committees: List[str]
    target_representatives: List[Representative]
    strategy: str
    talking_points: List[str]

@dataclass
class RepresentativeAnalysis:
    representative: Representative
    key_issues: List[str]
    background_summary: str
    political_positions: Dict[str, str]
    seat_risk_score: float  # 0-10 scale
    likely_challengers: List[str]
    voting_record_summary: Optional[str] = None