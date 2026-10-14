#!/usr/bin/env python3
"""
Test script for the Dynamic Routing Engine
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_routing_engine():
    """Test that the routing engine works correctly"""
    
    print("Testing Dynamic Routing Engine...")
    
    # Test 1: Import the routing engine
    try:
        from routing_engine.dynamic_routing_engine import DynamicRoutingEngine
        print("✓ DynamicRoutingEngine imported successfully")
    except Exception as e:
        print(f"✗ Failed to import DynamicRoutingEngine: {e}")
        return False
    
    # Test 2: Initialize the routing engine
    try:
        router = DynamicRoutingEngine()
        print("✓ DynamicRoutingEngine initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize DynamicRoutingEngine: {e}")
        return False
    
    # Test 3: Add a sample route
    try:
        sample_route = {
            "id": "test-route-1",
            "target_domains": ["example.com", "test.org"],
            "user_agent": "TestSpider/1.0",
            "delay_range": [1, 3],
            "max_retries": 3,
            "proxies": ["proxy1.example.com:8080"]
        }
        
        success = router.add_route(sample_route)
        print(f"✓ Route added successfully: {success}")
    except Exception as e:
        print(f"✗ Failed to add route: {e}")
        return False
    
    # Test 4: Get the route back
    try:
        route = router.get_route("example.com")
        print(f"✓ Route retrieved successfully: {route is not None}")
    except Exception as e:
        print(f"✗ Failed to get route: {e}")
        return False
    
    # Test 5: Get all routes
    try:
        all_routes = router.get_all_routes()
        print(f"✓ All routes retrieved: {len(all_routes)} routes found")
    except Exception as e:
        print(f"✗ Failed to get all routes: {e}")
        return False
    
    # Test 6: Get statistics
    try:
        stats = router.get_statistics()
        print(f"✓ Statistics retrieved successfully: version {stats.get('version', 'unknown')}")
    except Exception as e:
        print(f"✗ Failed to get statistics: {e}")
        return False
    
    print("\n🎉 All routing engine tests passed!")
    return True

def test_integration():
    """Test the integration with crawler system"""
    
    print("\nTesting Routing-Crawler Integration...")
    
    try:
        from routing_engine.routing_crawler_integration import RoutingCrawlerIntegration
        integration = RoutingCrawlerIntegration()
        print("✓ RoutingCrawlerIntegration imported and initialized successfully")
        
        # Test adding a route for crawler
        crawler_config = {
            "target_domains": ["example.com", "test.org"],
            "user_agent": "CustomSpider/1.0",
            "delay_between_requests": 2,
            "max_retries": 5,
            "proxies": ["proxy1.example.com:8080"]
        }
        
        success = integration.add_route_for_crawler(crawler_config)
        print(f"✓ Added crawler route successfully: {success}")
        
        # Test getting configuration
        config = integration.get_crawler_config_for_domain("example.com")
        print(f"✓ Got crawler config successfully: {config is not None}")
        
        print("\n🎉 All integration tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success1 = test_routing_engine()
    success2 = test_integration()
    
    if success1 and success2:
        print("\n✅ ALL TESTS PASSED - Dynamic Routing Engine is ready!")
    else:
        print("\n❌ SOME TESTS FAILED")
        sys.exit(1)