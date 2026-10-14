#!/usr/bin/env python3
"""
Test script for the fixed spider generation sources
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Testet, ob alle Module korrekt importiert werden können"""
    print("Testing imports...")
    
    try:
        from crawler.improved_doom_crawler import ImprovedDoomCrawler
        print("✓ ImprovedDoomCrawler imported successfully")
    except Exception as e:
        print(f"✗ Failed to import ImprovedDoomCrawler: {e}")
        return False
    
    try:
        from enhanced_random_crawler_generator import EnhancedRandomCrawlerGenerator
        print("✓ EnhancedRandomCrawlerGenerator imported successfully")
    except Exception as e:
        print(f"✗ Failed to import EnhancedRandomCrawlerGenerator: {e}")
        return False
        
    try:
        from database.doom_sqldb import DoomSQLDB
        print("✓ DoomSQLDB imported successfully")
    except Exception as e:
        print(f"✗ Failed to import DoomSQLDB: {e}")
        return False
    
    try:
        from config.config_loader import load_config, load_proxy_list
        print("✓ Config loader imported successfully")
    except Exception as e:
        print(f"✗ Failed to import config loader: {e}")
        return False
        
    print("All imports successful!")
    return True

def test_basic_functionality():
    """Testet grundlegende Funktionalität"""
    print("\nTesting basic functionality...")
    
    try:
        from enhanced_random_crawler_generator import EnhancedRandomCrawlerGenerator
        generator = EnhancedRandomCrawlerGenerator()
        
        # Test random config generation
        config = generator.generate_random_crawler_config()
        print("✓ Random crawler configuration generated successfully")
        
        # Test recipe generation
        recipe = generator.generate_crawler_recipe("random")
        print("✓ Random crawler recipe generated successfully")
        
        # Test multiple crawlers
        multi_crawlers = generator.generate_multiple_random_crawlers(2)
        print("✓ Multiple random crawlers generated successfully")
        
        print("Basic functionality test passed!")
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

if __name__ == "__main__":
    print("Running tests for spider generation sources...")
    
    success = True
    success &= test_imports()
    success &= test_basic_functionality()
    
    if success:
        print("\n🎉 All tests passed! The spider generation sources are working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
        sys.exit(1)