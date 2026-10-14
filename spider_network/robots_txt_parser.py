"""
robots.txt Parser for the Spider Network
This module parses robots.txt files to validate backend access and ensure compliance with web crawling policies.
"""

import re
from urllib.parse import urljoin, urlparse
from typing import List, Set

class RobotsTxtParser:
    """
    A parser for robots.txt files that validates spider access and extracts rules.
    """
    
    def __init__(self):
        self.rules = []
        self.disallowed_paths = set()
        self.allowed_paths = set()
        
    def parse_robots_txt(self, content: str) -> None:
        """
        Parse the robots.txt content and extract rules.
        
        Args:
            content (str): The content of the robots.txt file
        """
        # Reset previous rules
        self.rules = []
        self.disallowed_paths = set()
        self.allowed_paths = set()
        
        # Split into lines
        lines = content.strip().split('\n')
        
        current_user_agent = None
        current_rules = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
                
            # Parse User-agent
            user_agent_match = re.match(r'User-agent:\s*(.*)', line, re.IGNORECASE)
            if user_agent_match:
                current_user_agent = user_agent_match.group(1).strip()
                current_rules = []
                continue
                
            # Parse Disallow
            disallow_match = re.match(r'Disallow:\s*(.*)', line, re.IGNORECASE)
            if disallow_match:
                path = disallow_match.group(1).strip()
                if path:
                    self.disallowed_paths.add(path)
                    current_rules.append(('disallow', path))
                    
            # Parse Allow
            allow_match = re.match(r'Allow:\s*(.*)', line, re.IGNORECASE)
            if allow_match:
                path = allow_match.group(1).strip()
                if path:
                    self.allowed_paths.add(path)
                    current_rules.append(('allow', path))
                    
            # Parse Crawl-delay
            crawl_delay_match = re.match(r'Crawl-delay:\s*(.*)', line, re.IGNORECASE)
            if crawl_delay_match:
                delay = crawl_delay_match.group(1).strip()
                if delay:
                    current_rules.append(('crawl-delay', delay))
                    
        # Store rules with user agent context
        if current_user_agent:
            self.rules.append({
                'user_agent': current_user_agent,
                'rules': current_rules
            })
    
    def is_path_allowed(self, path: str, user_agent: str = '*') -> bool:
        """
        Check if a path is allowed for crawling.
        
        Args:
            path (str): The path to check
            user_agent (str): The user agent to check against
            
        Returns:
            bool: True if the path is allowed, False otherwise
        """
        # Check if path is explicitly disallowed
        for disallowed_path in self.disallowed_paths:
            if self._path_matches(path, disallowed_path):
                return False
                
        # Check if path is explicitly allowed (higher priority than disallow)
        for allowed_path in self.allowed_paths:
            if self._path_matches(path, allowed_path):
                return True
                
        # Default to allowed if no rules match
        return True
    
    def _path_matches(self, path: str, pattern: str) -> bool:
        """
        Check if a path matches a pattern.
        
        Args:
            path (str): The path to check
            pattern (str): The pattern to match against
            
        Returns:
            bool: True if the path matches the pattern
        """
        # Handle exact match
        if pattern == '*':
            return True
            
        # Handle prefix matching
        if pattern.endswith('*'):
            prefix = pattern[:-1]
            return path.startswith(prefix)
            
        # Handle exact match
        return path == pattern
    
    def get_crawl_delay(self, user_agent: str = '*') -> int:
        """
        Get the crawl delay for a specific user agent.
        
        Args:
            user_agent (str): The user agent to check
            
        Returns:
            int: The crawl delay in seconds
        """
        # Default delay is 0 seconds
        delay = 0
        
        for rule_group in self.rules:
            if rule_group['user_agent'] == user_agent or rule_group['user_agent'] == '*':
                for rule_type, value in rule_group['rules']:
                    if rule_type == 'crawl-delay':
                        try:
                            delay = int(value)
                        except ValueError:
                            pass  # Invalid delay value, keep default
                            
        return delay

# Example usage
if __name__ == "__main__":
    # Sample robots.txt content
    sample_content = """
User-agent: *
Disallow: /private/
Disallow: /admin/
Allow: /public/
Disallow: /api/v1/*
Allow: /api/v1/public/

User-agent: SpiderBot
Disallow: /secret/
Crawl-delay: 5

User-agent: *
Crawl-delay: 2
"""
    
    parser = RobotsTxtParser()
    parser.parse_robots_txt(sample_content)
    
    print("Disallowed paths:", parser.disallowed_paths)
    print("Allowed paths:", parser.allowed_paths)
    print("Is /private/ allowed?", parser.is_path_allowed("/private/"))
    print("Is /public/ allowed?", parser.is_path_allowed("/public/"))
    print("Crawl delay for SpiderBot:", parser.get_crawl_delay("SpiderBot"))
    print("Crawl delay for *:", parser.get_crawl_delay("*"))