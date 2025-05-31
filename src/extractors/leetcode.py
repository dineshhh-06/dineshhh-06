"""
LeetCode data extractor module.
"""

import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class LeetCodeExtractor:
    """
    Class for extracting user statistics from LeetCode.
    """
    
    def __init__(self, username):
        """
        Initialize with username.
        
        Args:
            username (str): LeetCode username
        """
        self.username = username
        self.graphql_url = "https://leetcode.com/graphql"
        self.query = """
        query userProfile($username: String! ) {
          matchedUser(username: $username) {
            username
            submitStats: submitStatsGlobal {
              acSubmissionNum {
                difficulty
                count
                submissions
              }
            }
            profile {
              ranking
              reputation
              starRating
            }
          }
        }
        """
    
    def get_stats(self):
        """
        Get user statistics from LeetCode.
        
        Returns:
            dict: User statistics
        """
        try:
            # Make GraphQL request
            response = requests.post(
                self.graphql_url,
                json={
                    "query": self.query,
                    "variables": {"username": self.username}
                },
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                logger.error(f"Error from LeetCode API: {data['errors']}")
                return self._get_error_stats()
            
            if not data.get("data") or not data["data"].get("matchedUser"):
                logger.error(f"User not found on LeetCode: {self.username}")
                return self._get_error_stats()
            
            user_data = data["data"]["matchedUser"]
            
            # Extract stats
            submission_stats = user_data["submitStats"]["acSubmissionNum"]
            
            total_solved = 0
            easy_solved = 0
            medium_solved = 0
            hard_solved = 0
            
            for stat in submission_stats:
                if stat["difficulty"] == "All":
                    total_solved = stat["count"]
                elif stat["difficulty"] == "Easy":
                    easy_solved = stat["count"]
                elif stat["difficulty"] == "Medium":
                    medium_solved = stat["count"]
                elif stat["difficulty"] == "Hard":
                    hard_solved = stat["count"]
            
            ranking = user_data["profile"]["ranking"] if user_data["profile"]["ranking"] else "N/A"
            
            # Calculate acceptance rate
            total_submissions = sum(stat["submissions"] for stat in submission_stats if stat["difficulty"] == "All")
            acceptance_rate = round((total_solved / total_submissions) * 100, 1) if total_submissions > 0 else 0
            
            return {
                "platform": "LeetCode",
                "username": self.username,
                "status": "Active",
                "rating": total_solved,  # LeetCode doesn't have a rating system like Codeforces
                "max_rating": "N/A",
                "rank": ranking,
                "problems_solved": total_solved,
                "easy_solved": easy_solved,
                "medium_solved": medium_solved,
                "hard_solved": hard_solved,
                "acceptance_rate": acceptance_rate,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        except Exception as e:
            logger.error(f"Error extracting LeetCode stats: {e}")
            return self._get_error_stats()
    
    def _get_error_stats(self):
        """
        Return error stats when API call fails.
        
        Returns:
            dict: Error statistics
        """
        return {
            "platform": "LeetCode",
            "username": self.username,
            "status": "Error",
            "rating": "N/A",
            "max_rating": "N/A",
            "rank": "N/A",
            "problems_solved": 0,
            "easy_solved": 0,
            "medium_solved": 0,
            "hard_solved": 0,
            "acceptance_rate": 0,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
