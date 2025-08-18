"""
Sample data for testing the Idaho Representatives tool
This provides realistic test data when the scraper can't access live data
"""

from models import Representative, Contact, Party, Chamber, HouseSeat, Committee

def get_sample_data():
    """Generate comprehensive Idaho legislative data for testing"""
    
    # All 35 Senate districts with sample senators
    senators = [
        Representative(name="Mary Souza", party=Party.REPUBLICAN, district=1, chamber=Chamber.SENATE, 
                     contact=Contact(email="msouza1@gov.idaho.gov", statehouse_phone="(208) 332-1000"), 
                     occupation="Retired Educator", committees=["Education", "Health & Welfare"]),
        Representative(name="Jim Woodward", party=Party.REPUBLICAN, district=2, chamber=Chamber.SENATE,
                     contact=Contact(email="jwoodward2@gov.idaho.gov", statehouse_phone="(208) 332-1001"),
                     occupation="Attorney", committees=["Judiciary, Rules & Administration"]),
        Representative(name="Scott Herndon", party=Party.REPUBLICAN, district=3, chamber=Chamber.SENATE,
                     contact=Contact(email="sherndon3@gov.idaho.gov", statehouse_phone="(208) 332-1002"),
                     occupation="Business Owner", committees=["State Affairs"]),
        Representative(name="Ben Toews", party=Party.REPUBLICAN, district=4, chamber=Chamber.SENATE,
                     contact=Contact(email="btoews4@gov.idaho.gov", statehouse_phone="(208) 332-1003"),
                     occupation="Engineer", committees=["Transportation & Defense"]),
        Representative(name="Carl Crabtree", party=Party.REPUBLICAN, district=5, chamber=Chamber.SENATE,
                     contact=Contact(email="ccrabtree5@gov.idaho.gov", statehouse_phone="(208) 332-1004"),
                     occupation="Farmer", committees=["Agricultural Affairs"]),
        Representative(name="Tammy Nichols", party=Party.REPUBLICAN, district=6, chamber=Chamber.SENATE,
                     contact=Contact(email="tnichols6@gov.idaho.gov", statehouse_phone="(208) 332-1005"),
                     occupation="Business Owner", committees=["Commerce & Human Resources"]),
        Representative(name="Brian Lenney", party=Party.REPUBLICAN, district=7, chamber=Chamber.SENATE,
                     contact=Contact(email="blenney7@gov.idaho.gov", statehouse_phone="(208) 332-1006"),
                     occupation="Retired Military", committees=["Transportation & Defense"]),
        Representative(name="Lori Den Hartog", party=Party.REPUBLICAN, district=8, chamber=Chamber.SENATE,
                     contact=Contact(email="ldenhartog8@gov.idaho.gov", statehouse_phone="(208) 332-1007"),
                     occupation="Educator", committees=["Education"]),
        Representative(name="Abby Lee", party=Party.REPUBLICAN, district=9, chamber=Chamber.SENATE,
                     contact=Contact(email="alee9@gov.idaho.gov", statehouse_phone="(208) 332-1008"),
                     occupation="Healthcare Professional", committees=["Health & Welfare"]),
        Representative(name="Patti Anne Lodge", party=Party.REPUBLICAN, district=10, chamber=Chamber.SENATE,
                     contact=Contact(email="plodge10@gov.idaho.gov", statehouse_phone="(208) 332-1009"),
                     occupation="Business Owner", committees=["Commerce & Human Resources"]),
        Representative(name="Todd Lakey", party=Party.REPUBLICAN, district=11, chamber=Chamber.SENATE,
                     contact=Contact(email="tlakey11@gov.idaho.gov", statehouse_phone="(208) 332-1010"),
                     occupation="Attorney", committees=["Judiciary, Rules & Administration"]),
        Representative(name="Glenneda Zuiderveld", party=Party.REPUBLICAN, district=12, chamber=Chamber.SENATE,
                     contact=Contact(email="gzuiderveld12@gov.idaho.gov", statehouse_phone="(208) 332-1011"),
                     occupation="Healthcare Professional", committees=["Health & Welfare"]),
        Representative(name="Lori Den Hartog", party=Party.REPUBLICAN, district=13, chamber=Chamber.SENATE,
                     contact=Contact(email="ldenhartog13@gov.idaho.gov", statehouse_phone="(208) 332-1012"),
                     occupation="Education Administrator", committees=["Education"]),
        Representative(name="C. Scott Grow", party=Party.REPUBLICAN, district=14, chamber=Chamber.SENATE,
                     contact=Contact(email="sgrow14@gov.idaho.gov", statehouse_phone="(208) 332-1013"),
                     occupation="Attorney", committees=["Judiciary, Rules & Administration"]),
        Representative(name="Chuck Winder", party=Party.REPUBLICAN, district=15, chamber=Chamber.SENATE,
                     contact=Contact(email="cwinder15@gov.idaho.gov", statehouse_phone="(208) 332-1014"),
                     occupation="Business Owner", committees=["Commerce & Human Resources"]),
        Representative(name="Grant Burgoyne", party=Party.DEMOCRAT, district=16, chamber=Chamber.SENATE,
                     contact=Contact(email="gburgoyne16@gov.idaho.gov", statehouse_phone="(208) 332-1015"),
                     occupation="Attorney", committees=["Judiciary, Rules & Administration"]),
        Representative(name="Laurie Lickley", party=Party.REPUBLICAN, district=17, chamber=Chamber.SENATE,
                     contact=Contact(email="llickley17@gov.idaho.gov", statehouse_phone="(208) 332-1016"),
                     occupation="Healthcare Professional", committees=["Health & Welfare"]),
        Representative(name="Janie Ward-Engelking", party=Party.DEMOCRAT, district=18, chamber=Chamber.SENATE,
                     contact=Contact(email="jward-engelking18@gov.idaho.gov", statehouse_phone="(208) 332-1017"),
                     occupation="Retired Teacher", committees=["Education"]),
        Representative(name="Rick Just", party=Party.REPUBLICAN, district=19, chamber=Chamber.SENATE,
                     contact=Contact(email="rjust19@gov.idaho.gov", statehouse_phone="(208) 332-1018"),
                     occupation="Business Owner", committees=["Commerce & Human Resources"]),
        Representative(name="Carl Crabtree", party=Party.REPUBLICAN, district=20, chamber=Chamber.SENATE,
                     contact=Contact(email="ccrabtree20@gov.idaho.gov", statehouse_phone="(208) 332-1019"),
                     occupation="Farmer", committees=["Agricultural Affairs"]),
        Representative(name="Mark Harris", party=Party.REPUBLICAN, district=21, chamber=Chamber.SENATE,
                     contact=Contact(email="mharris21@gov.idaho.gov", statehouse_phone="(208) 332-1020"),
                     occupation="Business Owner", committees=["Commerce & Human Resources"]),
        Representative(name="Kevin Cook", party=Party.REPUBLICAN, district=22, chamber=Chamber.SENATE,
                     contact=Contact(email="kcook22@gov.idaho.gov", statehouse_phone="(208) 332-1021"),
                     occupation="Educator", committees=["Education"]),
        Representative(name="Geoff Schroeder", party=Party.REPUBLICAN, district=23, chamber=Chamber.SENATE,
                     contact=Contact(email="gschroeder23@gov.idaho.gov", statehouse_phone="(208) 332-1022"),
                     occupation="Attorney", committees=["Judiciary, Rules & Administration"]),
        Representative(name="Hernán Martínez", party=Party.REPUBLICAN, district=24, chamber=Chamber.SENATE,
                     contact=Contact(email="hmartinez24@gov.idaho.gov", statehouse_phone="(208) 332-1023"),
                     occupation="Business Owner", committees=["Commerce & Human Resources"]),
        Representative(name="Steve Bair", party=Party.REPUBLICAN, district=25, chamber=Chamber.SENATE,
                     contact=Contact(email="sbair25@gov.idaho.gov", statehouse_phone="(208) 332-1024"),
                     occupation="Farmer", committees=["Agricultural Affairs"]),
        Representative(name="Dave Lent", party=Party.REPUBLICAN, district=26, chamber=Chamber.SENATE,
                     contact=Contact(email="dlent26@gov.idaho.gov", statehouse_phone="(208) 332-1025"),
                     occupation="Business Owner", committees=["Commerce & Human Resources"]),
        Representative(name="Kelly Anthon", party=Party.REPUBLICAN, district=27, chamber=Chamber.SENATE,
                     contact=Contact(email="kanthon27@gov.idaho.gov", statehouse_phone="(208) 332-1026"),
                     occupation="Attorney", committees=["Judiciary, Rules & Administration"]),
        Representative(name="David Nelson", party=Party.REPUBLICAN, district=28, chamber=Chamber.SENATE,
                     contact=Contact(email="dnelson28@gov.idaho.gov", statehouse_phone="(208) 332-1027"),
                     occupation="Business Owner", committees=["Commerce & Human Resources"]),
        Representative(name="Jim Patrick", party=Party.REPUBLICAN, district=29, chamber=Chamber.SENATE,
                     contact=Contact(email="jpatrick29@gov.idaho.gov", statehouse_phone="(208) 332-1028"),
                     occupation="Healthcare Professional", committees=["Health & Welfare"]),
        Representative(name="Ron Taylor", party=Party.REPUBLICAN, district=30, chamber=Chamber.SENATE,
                     contact=Contact(email="rtaylor30@gov.idaho.gov", statehouse_phone="(208) 332-1029"),
                     occupation="Farmer", committees=["Agricultural Affairs"]),
        Representative(name="Regina Bayer", party=Party.DEMOCRAT, district=31, chamber=Chamber.SENATE,
                     contact=Contact(email="rbayer31@gov.idaho.gov", statehouse_phone="(208) 332-1030"),
                     occupation="Educator", committees=["Education"]),
        Representative(name="Mark Nye", party=Party.DEMOCRAT, district=32, chamber=Chamber.SENATE,
                     contact=Contact(email="mnye32@gov.idaho.gov", statehouse_phone="(208) 332-1031"),
                     occupation="Business Owner", committees=["Commerce & Human Resources"]),
        Representative(name="Linda Wright Hartgen", party=Party.REPUBLICAN, district=33, chamber=Chamber.SENATE,
                     contact=Contact(email="lhartgen33@gov.idaho.gov", statehouse_phone="(208) 332-1032"),
                     occupation="Educator", committees=["Education"]),
        Representative(name="Angie Barkell", party=Party.REPUBLICAN, district=34, chamber=Chamber.SENATE,
                     contact=Contact(email="abarkell34@gov.idaho.gov", statehouse_phone="(208) 332-1033"),
                     occupation="Business Owner", committees=["Commerce & Human Resources"]),
        Representative(name="Rod Furniss", party=Party.REPUBLICAN, district=35, chamber=Chamber.SENATE,
                     contact=Contact(email="rfurniss35@gov.idaho.gov", statehouse_phone="(208) 332-1034"),
                     occupation="Farmer/Rancher", committees=["Agricultural Affairs"])
    ]
    
    # Sample house representatives
    representatives = [
        Representative(
            name="Judy Boyle",
            party=Party.REPUBLICAN,
            district=9,
            chamber=Chamber.HOUSE,
            house_seat=HouseSeat.A,
            contact=Contact(
                email="jboyle@gov.idaho.gov",
                statehouse_phone="(208) 332-1000"
            ),
            occupation="Retired",
            term_number=8,
            committees=["Health & Welfare", "Ways & Means"]
        ),
        Representative(
            name="Lauren Necochea",
            party=Party.DEMOCRAT,
            district=19,
            chamber=Chamber.HOUSE,
            house_seat=HouseSeat.A,
            contact=Contact(
                email="lnecochea@gov.idaho.gov",
                statehouse_phone="(208) 332-1000"
            ),
            occupation="Community Organizer",
            term_number=3,
            committees=["Education", "State Affairs"]
        ),
        Representative(
            name="Mike Moyle",
            party=Party.REPUBLICAN,
            district=14,
            chamber=Chamber.HOUSE,
            house_seat=HouseSeat.A,
            contact=Contact(
                email="mmoyle@gov.idaho.gov",
                statehouse_phone="(208) 332-1000"
            ),
            occupation="Business Owner",
            term_number=12,
            committees=["Ways & Means", "Revenue & Taxation"]
        ),
        Representative(
            name="Rod Furniss",
            party=Party.REPUBLICAN,
            district=35,
            chamber=Chamber.HOUSE,
            house_seat=HouseSeat.A,
            contact=Contact(
                email="rfurniss@gov.idaho.gov",
                statehouse_phone="(208) 332-1000"
            ),
            occupation="Farmer/Rancher",
            term_number=6,
            committees=["Agricultural Affairs", "Environment, Energy & Technology"]
        ),
        Representative(
            name="Melissa Wintrow",
            party=Party.DEMOCRAT,
            district=19,
            chamber=Chamber.HOUSE,
            house_seat=HouseSeat.B,
            contact=Contact(
                email="mwintrow@gov.idaho.gov",
                statehouse_phone="(208) 332-1000"
            ),
            occupation="Social Worker",
            term_number=4,
            committees=["Health & Welfare", "Judiciary, Rules & Administration"]
        ),
        Representative(
            name="Bryan Zollinger",
            party=Party.REPUBLICAN,
            district=20,
            chamber=Chamber.HOUSE,
            house_seat=HouseSeat.A,
            contact=Contact(
                email="bzollinger@gov.idaho.gov",
                statehouse_phone="(208) 332-1000"
            ),
            occupation="Attorney",
            term_number=5,
            committees=["Judiciary, Rules & Administration", "State Affairs"]
        )
    ]
    
    # Sample committees
    committees = [
        Committee(
            name="Education",
            chamber=Chamber.SENATE,
            chair="Lori Den Hartog",
            members=["Mary Souza", "Jim Woodward", "Janie Ward-Engelking"]
        ),
        Committee(
            name="Education",
            chamber=Chamber.HOUSE,
            chair="Julie VanOrden",
            members=["Lauren Necochea", "Wendy Horman", "Gayann DeMordaunt"]
        ),
        Committee(
            name="Health & Welfare",
            chamber=Chamber.SENATE,
            chair="Fred Martin",
            members=["Mary Souza", "Todd Lakey", "Melissa Wintrow"]
        ),
        Committee(
            name="Agricultural Affairs",
            chamber=Chamber.HOUSE,
            chair="Caroline Nilsson Troy",
            members=["Rod Furniss", "Clark Kauffman", "Judy Boyle"]
        ),
        Committee(
            name="Ways & Means",
            chamber=Chamber.HOUSE,
            chair="Wendy Horman",
            members=["Mike Moyle", "Judy Boyle", "Steven Harris"]
        )
    ]
    
    return {
        'senators': senators,
        'representatives': representatives,
        'committees': committees
    }