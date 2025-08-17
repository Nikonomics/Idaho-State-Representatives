import openai
from typing import List, Dict, Optional
from models import Representative, ProblemAnalysis, RepresentativeAnalysis

class RepresentativeAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        self.client = openai.OpenAI(api_key=api_key) if api_key else None
    
    def analyze_problem(self, problem_description: str, all_reps: List[Representative]) -> ProblemAnalysis:
        """Analyze a problem and recommend committees and representatives to contact"""
        
        # Committee mapping based on common Idaho legislative issues
        committee_mapping = {
            'agriculture': ['Agriculture Affairs', 'Agricultural Affairs'],
            'business': ['Commerce & Human Resources', 'Business'],
            'education': ['Education', 'Educational Affairs'],
            'environment': ['Environment, Energy & Technology', 'Resources & Environment'],
            'health': ['Health & Welfare'],
            'transportation': ['Transportation & Defense'],
            'taxes': ['Revenue & Taxation', 'Ways & Means'],
            'law enforcement': ['Judiciary, Rules & Administration'],
            'government': ['State Affairs', 'Local Government'],
            'budget': ['Joint Finance-Appropriations Committee', 'Ways & Means']
        }
        
        # Simple keyword-based committee recommendation
        problem_lower = problem_description.lower()
        recommended_committees = []
        
        for issue, committees in committee_mapping.items():
            if issue in problem_lower:
                recommended_committees.extend(committees)
        
        # Find representatives on recommended committees
        target_reps = []
        for rep in all_reps:
            if any(committee in rep.committees for committee in recommended_committees):
                target_reps.append(rep)
        
        # Generate strategy based on problem type
        strategy = self._generate_strategy(problem_description, recommended_committees)
        talking_points = self._generate_talking_points(problem_description)
        
        return ProblemAnalysis(
            problem_description=problem_description,
            recommended_committees=recommended_committees,
            target_representatives=target_reps,
            strategy=strategy,
            talking_points=talking_points
        )
    
    def analyze_representative(self, rep: Representative) -> RepresentativeAnalysis:
        """Perform deep analysis on a specific representative"""
        
        # Basic analysis based on available data
        key_issues = self._infer_key_issues(rep)
        background_summary = self._create_background_summary(rep)
        political_positions = self._infer_political_positions(rep)
        seat_risk_score = self._calculate_seat_risk(rep)
        likely_challengers = self._predict_challengers(rep)
        
        return RepresentativeAnalysis(
            representative=rep,
            key_issues=key_issues,
            background_summary=background_summary,
            political_positions=political_positions,
            seat_risk_score=seat_risk_score,
            likely_challengers=likely_challengers
        )
    
    def _generate_strategy(self, problem: str, committees: List[str]) -> str:
        """Generate a strategy for addressing the problem"""
        if not committees:
            return "Contact your district representatives directly to discuss this issue."
        
        strategy = f"Target the following committees: {', '.join(committees)}. "
        strategy += "Schedule meetings with committee chairs and members from your district. "
        strategy += "Prepare specific examples and data to support your position."
        
        return strategy
    
    def _generate_talking_points(self, problem: str) -> List[str]:
        """Generate talking points based on the problem"""
        return [
            "Clearly explain how this issue affects Idaho residents",
            "Provide specific examples and data",
            "Suggest concrete legislative solutions",
            "Emphasize economic or public safety impacts",
            "Request specific actions from the representative"
        ]
    
    def _infer_key_issues(self, rep: Representative) -> List[str]:
        """Infer key issues based on committee memberships and background"""
        issues = []
        
        if rep.committees:
            for committee in rep.committees:
                if 'agriculture' in committee.lower():
                    issues.append('Agriculture and Rural Development')
                elif 'education' in committee.lower():
                    issues.append('Education Policy')
                elif 'health' in committee.lower():
                    issues.append('Healthcare')
                elif 'business' in committee.lower() or 'commerce' in committee.lower():
                    issues.append('Business and Economic Development')
                elif 'environment' in committee.lower():
                    issues.append('Environmental Policy')
        
        # Infer from occupation
        if rep.occupation:
            if 'farm' in rep.occupation.lower() or 'ranch' in rep.occupation.lower():
                issues.append('Agriculture and Rural Issues')
            elif 'business' in rep.occupation.lower():
                issues.append('Business Development')
            elif 'education' in rep.occupation.lower() or 'teacher' in rep.occupation.lower():
                issues.append('Education')
        
        return list(set(issues)) if issues else ['General Legislative Matters']
    
    def _create_background_summary(self, rep: Representative) -> str:
        """Create a background summary"""
        summary = f"{rep.name} represents District {rep.district} in the Idaho {rep.chamber.value}. "
        
        if rep.occupation:
            summary += f"Professional background: {rep.occupation}. "
        
        if rep.party == Party.REPUBLICAN:
            summary += "Member of the Republican Party. "
        else:
            summary += "Member of the Democratic Party. "
        
        if rep.committees:
            summary += f"Serves on {len(rep.committees)} committees including {', '.join(rep.committees[:2])}."
        
        return summary
    
    def _infer_political_positions(self, rep: Representative) -> Dict[str, str]:
        """Infer political positions based on party and committees"""
        positions = {}
        
        if rep.party == Party.REPUBLICAN:
            positions.update({
                'Fiscal Policy': 'Generally supports lower taxes and reduced government spending',
                'Business Regulation': 'Tends to favor reduced regulations on businesses',
                'Social Issues': 'Typically conservative on social issues'
            })
        else:
            positions.update({
                'Fiscal Policy': 'May support targeted spending on public services',
                'Business Regulation': 'May favor consumer and worker protections',
                'Social Issues': 'Typically progressive on social issues'
            })
        
        return positions
    
    def _calculate_seat_risk(self, rep: Representative) -> float:
        """Calculate how at-risk the representative's seat is (0-10 scale)"""
        # Simple heuristic based on party and district
        # In reality, this would use voting history, demographics, etc.
        
        if rep.party == Party.REPUBLICAN:
            # Most Idaho districts are safely Republican
            return 2.0
        else:
            # Democratic seats in Idaho are generally more competitive
            return 6.0
    
    def _predict_challengers(self, rep: Representative) -> List[str]:
        """Predict likely challengers (placeholder implementation)"""
        # This would require extensive political research and data
        # For now, return generic possibilities
        
        if rep.party == Party.REPUBLICAN:
            return ["Primary challenger from the right", "Business community candidate"]
        else:
            return ["Republican challenger", "Independent candidate"]