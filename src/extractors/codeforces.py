"""
Codeforces data extractor module.
"""

import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CodeforcesExtractor:
    """
    Class for extracting user statistics from Codeforces.
    """
    
    def __init__(self, username):
        """
        Initialize with username.
        
        Args:
            username (str): Codeforces username
        """
        self.username = username
        self.api_url = f"https://codeforces.com/api/user.info?handles={username}"
        self.solved_problems_url = f"https://codeforces.com/api/user.status?handle={username}&from=1&count=1000"
    
    def get_stats(self ):
        """
        Get user statistics from Codeforces.
        
        Returns:
            dict: User statistics
        """
        try:
            # Get user info
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
            
            if data["status"] != "OK":
                logger.error(f"Error from Codeforces API: {data}")
                return self._get_error_stats()
            
            user_data = data["result"][0]
            
            # Get solved problems
            problems_response = requests.get(self.solved_problems_url)
            problems_response.raise_for_status()
            problems_data = problems_response.json()
            
            if problems_data["status"] != "OK":
                logger.error(f"Error from Codeforces API (problems): {problems_data}")
                problems_solved = 0
            else:
                # Count unique solved problems
                solved_problems = set()
                for submission in problems_data["result"]:
                    if submission["verdict"] == "OK":
                        problem_key = f"{submission['problem']['contestId']}-{submission['problem']['index']}"
                        solved_problems.add(problem_key)
                
                problems_solved = len(solved_problems)
            
            # Extract stats
            rating = user_data.get("rating", 0)
            max_rating = user_data.get("maxRating", 0)
            rank = user_data.get("rank", "Unrated")
            
            return {
                "platform": "Codeforces",
                "username": self.username,
                "status": "Active",
                "rating": rating,
                "max_rating": max_rating,
                "rank": rank,
                "problems_solved": problems_solved,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        except Exception as e:
            logger.error(f"Error extracting Codeforces stats: {e}")
            return self._get_error_stats()
    
    def _get_error_stats(self):
        """
        Return error stats when API call fails.
        
        Returns:
            dict: Error statistics
        """
        return {
            "platform": "Codeforces",
            "username": self.username,
            "status": "Error",
            "rating": "N/A",
            "max_rating": "N/A",
            "rank": "N/A",
            "problems_solved": 0,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
