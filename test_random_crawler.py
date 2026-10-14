#!/usr/bin/env python3
"""
Test script for the Random Crawler Generator
"""

from enhanced_random_crawler_generator import EnhancedRandomCrawlerGenerator

def test_random_crawler_generator():
    print("Testing Random Crawler Generator...")
    
    # Initialize generator
    generator = EnhancedRandomCrawlerGenerator()
    
    # Test 1: Generate random configuration
    print("\n1. Generating random configuration:")
    config = generator.generate_random_crawler_config()
    for key, value in config.items():
        print(f"   {key}: {value}")
    
    # Test 2: Create random crawler
    print("\n2. Creating random crawler instance:")
    crawler = generator.create_random_crawler()
    print("   Crawler created successfully!")
    
    # Test 3: Generate multiple crawlers
    print("\n3. Generating multiple crawlers:")
    multi_crawlers = generator.generate_multiple_random_crawlers(3)
    for item in multi_crawlers:
        print(f"   Crawler {item['id']}: {item['config']['max_workers']} workers")
    
    # Test 4: Generate recipe
    print("\n4. Generating random recipe:")
    recipe = generator.generate_crawler_recipe("random")
    print(f"   Name: {recipe['name']}")
    print(f"   Description: {recipe['description']}")
    print(f"   Features: {', '.join(recipe['features'])}")
    
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    test_random_crawler_generator()