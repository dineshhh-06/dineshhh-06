"""
CSES data extractor module.
"""

import requests
import logging
from datetime import datetime
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class CSESExtractor:
    """
    Class for extracting user statistics from CSES.
    """
    
    def __init__(self, username):
        """
        Initialize with username.
        
        Args:
            username (str): CSES user ID
        """
        self.username = username
        self.profile_url = f"https://cses.fi/user/{username}"
    
    def get_stats(self ):
        """
        Get user statistics from CSES.
        
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
            
            # Extract problems solved
            problems_solved = 0
            
            # Look for the solved problems count
            content_div = soup.select_one(".content")
            if content_div:
                text = content_div.text
                if "Solved tasks" in text:
                    try:
                        # Try to extract the count
                        solved_line = [line for line in text.split("\n") if "Solved tasks" in line][0]
                        problems_solved = int(solved_line.split(":")[1].strip())
                    except (IndexError, ValueError) as e:
                        logger.warning(f"Could not extract problems solved: {e}")
            
            return {
                "platform": "CSES",
                "username": self.username,
                "status": "Active",
                "rating": "N/A",  # CSES doesn't have a rating system
                "max_rating": "N/A",
                "rank": "N/A",
                "problems_solved": problems_solved,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        except Exception as e:
            logger.error(f"Error extracting CSES stats: {e}")
            return self._get_error_stats()
    
    def _get_error_stats(self):
        """
        Return error stats when API call fails.
        
        Returns:
            dict: Error statistics
        """
        return {
            "platform": "CSES",
            "username": self.username,
            "status": "Error",
            "rating": "N/A",
            "max_rating": "N/A",
            "rank": "N/A",
            "problems_solved": 0,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
