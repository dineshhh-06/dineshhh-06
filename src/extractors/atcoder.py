"""
AtCoder data extractor module.
"""

import requests
import logging
from datetime import datetime
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class AtCoderExtractor:
    """
    Class for extracting user statistics from AtCoder.
    """
    
    def __init__(self, username):
        """
        Initialize with username.
        
        Args:
            username (str): AtCoder username
        """
        self.username = username
        self.profile_url = f"https://atcoder.jp/users/{username}"
    
    def get_stats(self ):
        """
        Get user statistics from AtCoder.
        
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
            rating = "N/A"
            rank = "Unrated"
            
            # Find the table with user information
            tables = soup.select("table.dl-table")
            if tables:
                for table in tables:
                    rows = table.select("tr")
                    for row in rows:
                        cells = row.select("td, th")
                        if len(cells) >= 2:
                            header = cells[0].text.strip()
                            value = cells[1].text.strip()
                            
                            if "Rating" in header:
                                try:
                                    rating = int(value.split()[0])
                                except (ValueError, IndexError):
                                    rating = "N/A"
                            
                            if "Class" in header or "Rank" in header:
                                rank = value
            
            # Extract problems solved (this is an approximation)
            problems_solved = 0
            submissions_link = soup.select_one("a[href*='/submissions?f.Status=AC']")
            if submissions_link:
                try:
                    # Try to extract the count from the link text
                    text = submissions_link.text.strip()
                    if "(" in text and ")" in text:
                        count_str = text.split("(")[1].split(")")[0]
                        problems_solved = int(count_str)
                except Exception as e:
                    logger.warning(f"Could not extract problems solved: {e}")
            
            return {
                "platform": "AtCoder",
                "username": self.username,
                "status": "Active",
                "rating": rating,
                "max_rating": "N/A",  # AtCoder doesn't show max rating directly on profile
                "rank": rank,
                "problems_solved": problems_solved,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        except Exception as e:
            logger.error(f"Error extracting AtCoder stats: {e}")
            return self._get_error_stats()
    
    def _get_error_stats(self):
        """
        Return error stats when API call fails.
        
        Returns:
            dict: Error statistics
        """
        return {
            "platform": "AtCoder",
            "username": self.username,
            "status": "Error",
            "rating": "N/A",
            "max_rating": "N/A",
            "rank": "N/A",
            "problems_solved": 0,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
