import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class MLRecommender:
    """Simple placeholder for a recommendation model."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # In a production system, load trained model here

    def recommend_programs(self, user_profile: Dict, top_k: int = 5) -> List[Dict]:
        """
        Produce simple recommendations based on user's preferred country/program.
        user_profile example: {"country": "USA", "interests": ["computer science"], "gpa": 3.5}
        """
        recommendations = []
        # Placeholder rules-based recommendation. Replace with ML model in future.
        preferred_country = user_profile.get("country", "").lower()
        interests = [i.lower() for i in user_profile.get("interests", [])]

        # Dummy static list (in production load from KB)
        static_programs = [
            {"id": "usa-001", "university": "Harvard University", "program": "Computer Science", "country": "USA"},
            {"id": "uk-001", "university": "University of Oxford", "program": "Engineering", "country": "UK"},
            {"id": "canada-001", "university": "University of Toronto", "program": "Business Administration", "country": "Canada"}
        ]

        for p in static_programs:
            if preferred_country and preferred_country in p.get("country","").lower():
                recommendations.append(p)
            elif any(i in p.get("program","").lower() for i in interests):
                recommendations.append(p)

        # Fallback: return top K
        if not recommendations:
            recommendations = static_programs[:top_k]

        return recommendations[:top_k]
