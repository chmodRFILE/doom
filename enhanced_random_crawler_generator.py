"""
Enhanced Random Crawler Generator for Doom Web Crawler System
This module generates random crawler configurations with more sophisticated logic
"""

import json
import random
import os
from crawler.improved_doom_crawler import ImprovedDoomCrawler

class EnhancedRandomCrawlerGenerator:
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
            
    def get_available_proxies(self):
        """Get list of available proxies from config"""
        if 'proxy_list' in self.config and isinstance(self.config['proxy_list'], list):
            return self.config['proxy_list']
        else:
            # Fallback to proxy list file
            try:
                with open("config/proxy_list.txt", "r") as f:
                    proxies = [line.strip() for line in f if line.strip()]
                    return proxies
            except:
                return []
                
    def generate_random_proxy_list(self, max_proxies=5):
        """Generate a random subset of proxies from the existing list"""
        available_proxies = self.get_available_proxies()
        
        if not available_proxies:
            return []
            
        # Select random proxies (avoid duplicates)
        selected_proxies = random.sample(available_proxies, 
                                       min(max_proxies, len(available_proxies)))
        return selected_proxies
        
    def generate_random_user_agent(self):
        """Generate a random user agent string"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]
        return random.choice(user_agents)
        
    def generate_random_delay(self, min_delay=0.5, max_delay=3.0):
        """Generate a random delay between requests"""
        return round(random.uniform(min_delay, max_delay), 2)
        
    def generate_random_crawler_config(self):
        """Generate a completely random crawler configuration"""
        config = {
            "proxy_list": self.generate_random_proxy_list(),
            "user_agent": self.generate_random_user_agent(),
            "request_delay": self.generate_random_delay(),
            "max_workers": random.randint(1, 15),
            "timeout": random.randint(10, 60),
            "follow_redirects": random.choice([True, False]),
            "allow_robots": random.choice([True, False]),
            "use_cache": random.choice([True, False]),
            "retry_attempts": random.randint(0, 5)
        }
        return config
        
    def create_random_crawler(self):
        """Create a new crawler instance with random configuration"""
        random_config = self.generate_random_crawler_config()
        
        # Create crawler with random parameters (only max_workers supported by current API)
        crawler = ImprovedDoomCrawler(
            max_workers=random_config["max_workers"]
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
                    "follow_redirects": True,
                    "timeout": 30
                }
            },
            "social_media_scrapper": {
                "name": "Social Media Scrapper",
                "description": "Crawler for social media content extraction",
                "features": ["scraping", "networking", "proxy_support"],
                "config": {
                    "max_workers": 5,
                    "request_delay": random.uniform(1, 3),
                    "follow_redirects": False,
                    "timeout": 45
                }
            },
            "search_engine_crawler": {
                "name": "Search Engine Crawler",
                "description": "Crawler optimized for search engine scraping",
                "features": ["scraping", "proxy_support", "analysis"],
                "config": {
                    "max_workers": 8,
                    "request_delay": random.uniform(0.5, 2),
                    "follow_redirects": True,
                    "timeout": 60
                }
            },
            "image_downloader": {
                "name": "Image Downloader",
                "description": "Crawler focused on downloading images from web pages",
                "features": ["scraping", "image_extraction", "proxy_support"],
                "config": {
                    "max_workers": 10,
                    "request_delay": random.uniform(1, 4),
                    "follow_redirects": True,
                    "timeout": 30
                }
            },
            "data_extractor": {
                "name": "Data Extractor",
                "description": "General purpose data extraction crawler",
                "features": ["scraping", "analysis", "proxy_support"],
                "config": {
                    "max_workers": 6,
                    "request_delay": random.uniform(0.5, 2),
                    "follow_redirects": True,
                    "timeout": 45
                }
            }
        }
        
        if recipe_type == "random":
            # Return a random recipe
            return random.choice(list(recipes.values()))
        else:
            return recipes.get(recipe_type, recipes["email_scraper"])
            
    def generate_multiple_random_crawlers(self, count=3):
        """Generate multiple random crawler instances"""
        crawlers = []
        for i in range(count):
            crawler = self.create_random_crawler()
            crawlers.append({
                "id": i+1,
                "crawler": crawler,
                "config": self.generate_random_crawler_config()
            })
        return crawlers

# Example usage
if __name__ == "__main__":
    generator = EnhancedRandomCrawlerGenerator()
    
    # Generate a random crawler configuration
    print("Random Crawler Configuration:")
    config = generator.generate_random_crawler_config()
    for key, value in config.items():
        print(f"  {key}: {value}")
        
    # Create a random crawler instance
    print("\nCreating Random Crawler...")
    crawler = generator.create_random_crawler()
    print("Random crawler created successfully!")
    
    # Generate multiple crawlers
    print("\nGenerating Multiple Crawlers:")
    multi_crawlers = generator.generate_multiple_random_crawlers(3)
    for item in multi_crawlers:
        print(f"  Crawler {item['id']}: {item['config']['max_workers']} workers")
    
    # Generate a recipe
    print("\nRandom Recipe:")
    recipe = generator.generate_crawler_recipe("random")
    for key, value in recipe.items():
        print(f"  {key}: {value}")