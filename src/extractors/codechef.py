"""
CodeChef data extractor module.
"""

import requests
import logging
from datetime import datetime
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class CodeChefExtractor:
    """
    Class for extracting user statistics from CodeChef.
    """
    
    def __init__(self, username):
        """
        Initialize with username.
        
        Args:
            username (str): CodeChef username
        """
        self.username = username
        self.profile_url = f"https://www.codechef.com/users/{username}"
    
    def get_stats(self ):
        """
        Get user statistics from CodeChef.
        
        Returns:
            dict: User statistics
        """
        try:
            # Get user profile page
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(self.profile_url, headers=headers)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract rating
            rating_element = soup.select_one(".rating-number")
            rating = int(rating_element.text.strip()) if rating_element else "N/A"
            
            # Extract rank/stars
            rank_element = soup.select_one(".rating-star")
            rank = rank_element.text.strip() if rank_element else "Unrated"
            
            # Extract problems solved
            problems_solved = 0
            try:
                # This is an approximation as CodeChef doesn't show total problems solved directly
                problems_element = soup.select_one(".problems-solved")
                if problems_element:
                    problems_text = problems_element.text
                    problems_solved = len(problems_text.split(",")) if "," in problems_text else 0
            except Exception as e:
                logger.warning(f"Could not extract problems solved: {e}")
            
            return {
                "platform": "CodeChef",
                "username": self.username,
                "status": "Active",
                "rating": rating,
                "max_rating": "N/A",  # CodeChef doesn't show max rating on profile
                "rank": rank,
                "problems_solved": problems_solved,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        except Exception as e:
            logger.error(f"Error extracting CodeChef stats: {e}")
            return self._get_error_stats()
    
    def _get_error_stats(self):
        """
        Return error stats when API call fails.
        
        Returns:
            dict: Error statistics
        """
        return {
            "platform": "CodeChef",
            "username": self.username,
            "status": "Error",
            "rating": "N/A",
            "max_rating": "N/A",
            "rank": "N/A",
            "problems_solved": 0,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
