"""
Random Crawler Generator for Doom Web Crawler System
This module generates random crawler configurations based on existing parameters
"""

import json
import random
import os
from crawler.improved_doom_crawler import ImprovedDoomCrawler

class RandomCrawlerGenerator:
    def __init__(self, config_path="config/crawler_config.json"):
        self.config_path = config_path
        self.load_config()
        
    def load_config(self):
        """Load existing crawler configuration"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = {}
            
    def generate_random_proxy_list(self, max_proxies=5):
        """Generate a random subset of proxies from the existing list"""
        if 'proxy_list' not in self.config:
            return []
            
        available_proxies = self.config['proxy_list']
        if not available_proxies:
            return []
            
        # Select random proxies (avoid duplicates)
        selected_proxies = random.sample(available_proxies, 
                                       min(max_proxies, len(available_proxies)))
        return selected_proxies
        
    def generate_random_user_agent(self):
        """Generate a random user agent string"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
            "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36"
        ]
        return random.choice(user_agents)
        
    def generate_random_delay(self, min_delay=1, max_delay=5):
        """Generate a random delay between requests"""
        return random.uniform(min_delay, max_delay)
        
    def generate_random_crawler_config(self):
        """Generate a completely random crawler configuration"""
        config = {
            "proxy_list": self.generate_random_proxy_list(),
            "user_agent": self.generate_random_user_agent(),
            "request_delay": self.generate_random_delay(),
            "max_workers": random.randint(1, 10),
            "timeout": random.randint(10, 30),
            "follow_redirects": random.choice([True, False]),
            "allow_robots": random.choice([True, False])
        }
        return config
        
    def create_random_crawler(self):
        """Create a new crawler instance with random configuration"""
        random_config = self.generate_random_crawler_config()
        
        # Create crawler with random parameters
        crawler = ImprovedDoomCrawler(
            proxy_list=random_config["proxy_list"],
            user_agent=random_config["user_agent"],
            request_delay=random_config["request_delay"],
            max_workers=random_config["max_workers"],
            timeout=random_config["timeout"]
        )
        
        return crawler
        
    def generate_crawler_recipe(self, recipe_type="random"):
        """Generate a crawler recipe based on type"""
        recipes = {
            "email_scraper": {
                "name": "Email Scraper",
                "description": "Crawler focused on extracting email addresses",
                "features": ["scraping", "email_extraction", "proxy_support"],
                "config": {
                    "max_workers": 3,
                    "request_delay": random.uniform(2, 5),
                    "follow_redirects": True
                }
            },
            "social_media_scrapper": {
                "name": "Social Media Scrapper",
                "description": "Crawler for social media content extraction",
                "features": ["scraping", "networking", "proxy_support"],
                "config": {
                    "max_workers": 5,
                    "request_delay": random.uniform(1, 3),
                    "follow_redirects": False
                }
            },
            "search_engine_crawler": {
                "name": "Search Engine Crawler",
                "description": "Crawler optimized for search engine scraping",
                "features": ["scraping", "proxy_support", "analysis"],
                "config": {
                    "max_workers": 8,
                    "request_delay": random.uniform(0.5, 2),
                    "follow_redirects": True
                }
            }
        }
        
        if recipe_type == "random":
            # Return a random recipe
            return random.choice(list(recipes.values()))
        else:
            return recipes.get(recipe_type, recipes["email_scraper"])

# Example usage
if __name__ == "__main__":
    generator = RandomCrawlerGenerator()
    
    # Generate a random crawler configuration
    print("Random Crawler Configuration:")
    config = generator.generate_random_crawler_config()
    for key, value in config.items():
        print(f"  {key}: {value}")
        
    # Create a random crawler instance
    print("\nCreating Random Crawler...")
    crawler = generator.create_random_crawler()
    print("Random crawler created successfully!")
    
    # Generate a recipe
    print("\nRandom Recipe:")
    recipe = generator.generate_crawler_recipe("random")
    for key, value in recipe.items():
        print(f"  {key}: {value}")