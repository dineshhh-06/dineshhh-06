"""
GitHub README updater module for dark-themed competitive programming statistics.
Updates a section in the GitHub README.md with the latest competitive programming statistics.
"""

import os
import re
import json
import logging
from datetime import datetime

# Import extractors
from extractors.codeforces import CodeforcesExtractor
from extractors.leetcode import LeetCodeExtractor
from extractors.codechef import CodeChefExtractor
from extractors.atcoder import AtCoderExtractor
from extractors.cses import CSESExtractor

# Import config
from config import PROFILES

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("../data/readme_updater.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def collect_stats():
    """
    Collect statistics from all platforms.
    
    Returns:
        dict: Dictionary of statistics from all platforms
    """
    stats = {}
    
    # Codeforces
    try:
        logger.info("Collecting Codeforces stats...")
        cf_extractor = CodeforcesExtractor(PROFILES["codeforces"]["username"])
        stats["codeforces"] = cf_extractor.get_stats()
        logger.info(f"Codeforces stats collected: {stats['codeforces']}")
    except Exception as e:
        logger.error(f"Error collecting Codeforces stats: {e}")
        stats["codeforces"] = {
            "platform": "Codeforces",
            "username": PROFILES["codeforces"]["username"],
            "status": "Error",
            "rating": "N/A",
            "max_rating": "N/A",
            "rank": "N/A",
            "problems_solved": 0,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    # LeetCode
    try:
        logger.info("Collecting LeetCode stats...")
        lc_extractor = LeetCodeExtractor(PROFILES["leetcode"]["username"])
        stats["leetcode"] = lc_extractor.get_stats()
        logger.info(f"LeetCode stats collected: {stats['leetcode']}")
    except Exception as e:
        logger.error(f"Error collecting LeetCode stats: {e}")
        stats["leetcode"] = {
            "platform": "LeetCode",
            "username": PROFILES["leetcode"]["username"],
            "status": "Error",
            "rating": "N/A",
            "max_rating": "N/A",
            "rank": "N/A",
            "problems_solved": 0,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    # CodeChef
    try:
        logger.info("Collecting CodeChef stats...")
        cc_extractor = CodeChefExtractor(PROFILES["codechef"]["username"])
        stats["codechef"] = cc_extractor.get_stats()
        logger.info(f"CodeChef stats collected: {stats['codechef']}")
    except Exception as e:
        logger.error(f"Error collecting CodeChef stats: {e}")
        stats["codechef"] = {
            "platform": "CodeChef",
            "username": PROFILES["codechef"]["username"],
            "status": "Error",
            "rating": "N/A",
            "max_rating": "N/A",
            "rank": "N/A",
            "problems_solved": 0,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    # AtCoder
    try:
        logger.info("Collecting AtCoder stats...")
        ac_extractor = AtCoderExtractor(PROFILES["atcoder"]["username"])
        stats["atcoder"] = ac_extractor.get_stats()
        logger.info(f"AtCoder stats collected: {stats['atcoder']}")
    except Exception as e:
        logger.error(f"Error collecting AtCoder stats: {e}")
        stats["atcoder"] = {
            "platform": "AtCoder",
            "username": PROFILES["atcoder"]["username"],
            "status": "Error",
            "rating": "N/A",
            "max_rating": "N/A",
            "rank": "N/A",
            "problems_solved": 0,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    # CSES
    try:
        logger.info("Collecting CSES stats...")
        cses_extractor = CSESExtractor(PROFILES["cses"]["username"])
        stats["cses"] = cses_extractor.get_stats()
        logger.info(f"CSES stats collected: {stats['cses']}")
    except Exception as e:
        logger.error(f"Error collecting CSES stats: {e}")
        stats["cses"] = {
            "platform": "CSES",
            "username": PROFILES["cses"]["username"],
            "status": "Error",
            "rating": "N/A",
            "max_rating": "N/A",
            "rank": "N/A",
            "problems_solved": 0,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    return stats

def generate_dark_theme_markdown(stats):
    """
    Generate dark-themed Markdown for GitHub README.
    
    Args:
        stats (dict): Dictionary of statistics from all platforms
    
    Returns:
        str: Dark-themed Markdown content
    """
    # Extract stats for each platform
    cf_stats = stats.get("codeforces", {})
    lc_stats = stats.get("leetcode", {})
    cc_stats = stats.get("codechef", {})
    ac_stats = stats.get("atcoder", {})
    cses_stats = stats.get("cses", {})
    
    # Get values with fallbacks
    cf_rating = cf_stats.get("rating", "N/A")
    cf_rank = cf_stats.get("rank", "N/A")
    cf_problems = cf_stats.get("problems_solved", 0)
    
    lc_problems = lc_stats.get("problems_solved", 0)
    lc_easy = lc_stats.get("easy_solved", 0)
    lc_medium = lc_stats.get("medium_solved", 0)
    lc_hard = lc_stats.get("hard_solved", 0)
    
    cc_rating = cc_stats.get("rating", "N/A")
    cc_rank = cc_stats.get("rank", "N/A")
    cc_problems = cc_stats.get("problems_solved", 0)
    
    ac_rating = ac_stats.get("rating", "N/A")
    ac_rank = ac_stats.get("rank", "N/A")
    ac_problems = ac_stats.get("problems_solved", 0)
    
    cses_problems = cses_stats.get("problems_solved", 0)
    
    # Calculate total problems
    total_problems = cf_problems + lc_problems + cc_problems + ac_problems + cses_problems
    
    # Calculate platform distribution percentages
    total = max(1, total_problems)  # Avoid division by zero
    cf_percent = round((cf_problems / total) * 100)
    lc_percent = round((lc_problems / total) * 100)
    others_percent = 100 - cf_percent - lc_percent
    
    # Format last updated date
    last_updated = datetime.now().strftime("%B %d, %Y")
    
    # Generate the Markdown
    markdown = f"""<!-- Competitive Programming Stats - Dark Theme -->

<div align="center">

  <!-- Title with custom styling -->
  <h2>🏆 Competitive Programming Stats</h2>

  <!-- Main Stats Cards - Top Row -->
  <a href="https://codeforces.com/profile/{PROFILES['codeforces']['username']}">
    <img src="https://img.shields.io/badge/Codeforces-{cf_rating}-58d3b9?style=for-the-badge&logo=codeforces&logoColor=white&labelColor=0d1117" alt="Codeforces">
  </a>
  <a href="https://leetcode.com/{PROFILES['leetcode']['username']}/">
    <img src="https://img.shields.io/badge/LeetCode-{lc_problems}_problems-58d3b9?style=for-the-badge&logo=leetcode&logoColor=white&labelColor=0d1117" alt="LeetCode">
  </a>
  <a href="https://www.codechef.com/users/{PROFILES['codechef']['username']}">
    <img src="https://img.shields.io/badge/CodeChef-{cc_rating}-58d3b9?style=for-the-badge&logo=codechef&logoColor=white&labelColor=0d1117" alt="CodeChef">
  </a>

  <!-- Stats Summary in GitHub-compatible table -->
  <table>
    <tr>
      <td align="center" width="200">
        <h1>{cf_rating}</h1>
        <strong>Codeforces Rating</strong>
        <br>
        <code>{cf_rank}</code>
      </td>
      <td align="center" width="200">
        <h1>{lc_problems}</h1>
        <strong>Problems Solved</strong>
        <br>
        <code>LeetCode</code>
      </td>
      <td align="center" width="200">
        <h1>{cc_rating}</h1>
        <strong>CodeChef Rating</strong>
        <br>
        <code>{cc_rank}</code>
      </td>
    </tr>
  </table>

  <!-- LeetCode Progress -->
  <h3>LeetCode Progress</h3>
  <a href="https://leetcode.com/{PROFILES['leetcode']['username']}/">
    <img src="https://img.shields.io/badge/Easy-{lc_easy}-3498db?style=flat-square&labelColor=0d1117" alt="Easy">
    <img src="https://img.shields.io/badge/Medium-{lc_medium}-f39c12?style=flat-square&labelColor=0d1117" alt="Medium">
    <img src="https://img.shields.io/badge/Hard-{lc_hard}-e74c3c?style=flat-square&labelColor=0d1117" alt="Hard">
  </a>

  <!-- Platform Distribution -->
  <h3>Platform Activity</h3>
  <a href="#">
    <img src="https://img.shields.io/badge/Codeforces-{cf_percent}%25-58d3b9?style=flat-square&labelColor=0d1117" alt="Codeforces">
    <img src="https://img.shields.io/badge/LeetCode-{lc_percent}%25-58d3b9?style=flat-square&labelColor=0d1117" alt="LeetCode">
    <img src="https://img.shields.io/badge/Others-{others_percent}%25-58d3b9?style=flat-square&labelColor=0d1117" alt="Others">
  </a>
  
  <br><br>
  <i>Last updated: {last_updated}</i>
</div>"""
    
    return markdown

def update_readme_section(readme_path, stats_markdown, section_header="## Competitive Programming Stats"):
    """
    Updates a specific section in the README.md file with new content.
    
    Args:
        readme_path (str): Path to the README.md file
        stats_markdown (str): New markdown content to insert
        section_header (str): Header that marks the section to update
    
    Returns:
        bool: True if update was successful, False otherwise
    """
    try:
        # Check if README exists
        if not os.path.exists(readme_path):
            logger.warning(f"README file not found at {readme_path}. Creating new file.")
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(f"{stats_markdown}\n")
            return True
        
        # Read existing README
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if section exists
        if section_header in content:
            # Find the section and replace it
            pattern = f"({re.escape(section_header)}.*?)(?=^#|\\Z)"
            replacement = stats_markdown
            
            # Use regex with DOTALL flag to match across multiple lines
            new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
            
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            logger.info(f"Updated section '{section_header}' in {readme_path}")
        else:
            # Section doesn't exist, append to the end
            with open(readme_path, 'a', encoding='utf-8') as f:
                f.write(f"\n{stats_markdown}\n")
                
            logger.info(f"Added new section '{section_header}' to {readme_path}")
        
        return True
    except Exception as e:
        logger.error(f"Error updating README: {e}")
        return False

def save_markdown_to_file(markdown, output_path):
    """
    Save Markdown to file.
    
    Args:
        markdown (str): Markdown content
        output_path (str): Path to save the file
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        logger.info(f"Markdown saved to {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving Markdown: {e}")
        return False

def main(readme_path=None):
    """
    Main function to update README with dark-themed competitive programming statistics.
    
    Args:
        readme_path (str): Path to the README.md file
    """
    # Set default path if not provided
    if not readme_path:
        readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "README.md")
    
    # Collect stats
    stats = collect_stats()
    
    # Generate dark-themed Markdown
    markdown = generate_dark_theme_markdown(stats)
    
    # Save to file for reference
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(output_dir, exist_ok=True)
    save_markdown_to_file(markdown, os.path.join(output_dir, "dark_theme_stats.md"))
    
    # Update README
    return update_readme_section(readme_path, markdown)

if __name__ == "__main__":
    # Run updater
    main()
