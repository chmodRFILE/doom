#!/usr/bin/env python3
"""
Integration module for Dynamic Routing Engine with the Doom Crawler System
"""

import time
from typing import Dict, Any, Optional
from routing_engine.dynamic_routing_engine import DynamicRoutingEngine
from crawler.improved_doom_crawler import ImprovedDoomCrawler

class RoutingCrawlerIntegration:
    """
    Integration layer between the Dynamic Routing Engine and the Doom Crawler system
    This module ensures crawlers use appropriate routes based on target domains
    """
    
    def __init__(self, routing_engine: Optional[DynamicRoutingEngine] = None):
        """
        Initialize the integration
        
        Args:
            routing_engine (DynamicRoutingEngine): Instance of the routing engine
        """
        self.routing_engine = routing_engine or DynamicRoutingEngine()
        self.crawler = ImprovedDoomCrawler()
    
    def get_crawler_config_for_domain(self, domain: str) -> Optional[Dict[str, Any]]:
        """
        Get crawler configuration based on route for a specific domain
        
        Args:
            domain (str): Target domain
            
        Returns:
            Dict or None: Configuration for the crawler
        """
        try:
            # Get route for this domain
            route = self.routing_engine.get_route(domain)
            
            if not route:
                # Fallback to default configuration
                return self._get_default_crawler_config()
            
            # Convert route to crawler configuration
            config = {
                "user_agent": route.get("user_agent", self.crawler.config.get("user_agent")),
                "delay_between_requests": route.get("delay_range", [1, 3])[0],
                "max_retries": route.get("max_retries", 3),
                "proxies": route.get("proxies", []),
                "target_domains": route.get("target_domains", [])
            }
            
            return config
            
        except Exception as e:
            print(f"Error getting crawler config for {domain}: {e}")
            return self._get_default_crawler_config()
    
    def _get_default_crawler_config(self) -> Dict[str, Any]:
        """Get default crawler configuration"""
        return {
            "user_agent": "Mozilla/5.0 (compatible; Spider/1.0)",
            "delay_between_requests": 1,
            "max_retries": 3,
            "proxies": [],
            "target_domains": []
        }
    
    def add_route_for_crawler(self, crawler_config: Dict[str, Any]) -> bool:
        """
        Add a route configuration that can be used by crawlers
        
        Args:
            crawler_config (Dict): Crawler configuration to convert to route
            
        Returns:
            bool: True if successful
        """
        try:
            # Convert crawler config to route format
            route_config = {
                "id": f"route-{int(time.time())}",
                "target_domains": crawler_config.get("target_domains", []),
                "user_agent": crawler_config.get("user_agent", "Mozilla/5.0 (compatible; Spider/1.0)"),
                "delay_range": [crawler_config.get("delay_between_requests", 1), 
                               crawler_config.get("delay_between_requests", 1) + 2],
                "max_retries": crawler_config.get("max_retries", 3),
                "proxies": crawler_config.get("proxies", []),
                "priority": crawler_config.get("priority", 0)
            }
            
            return self.routing_engine.add_route(route_config)
            
        except Exception as e:
            print(f"Error adding route for crawler: {e}")
            return False
    
    def update_crawler_route(self, route_id: str, updated_config: Dict[str, Any]) -> bool:
        """
        Update an existing route configuration
        
        Args:
            route_id (str): Route identifier
            updated_config (Dict): Updated configuration
            
        Returns:
            bool: True if successful
        """
        try:
            return self.routing_engine.update_route(route_id, updated_config)
        except Exception as e:
            print(f"Error updating crawler route: {e}")
            return False

# Example usage function
def example_integration():
    """Example of how to use the routing crawler integration"""
    
    # Initialize integration
    integration = RoutingCrawlerIntegration()
    
    # Add a sample crawler configuration as a route
    crawler_config = {
        "target_domains": ["example.com", "test.org"],
        "user_agent": "CustomSpider/1.0",
        "delay_between_requests": 2,
        "max_retries": 5,
        "proxies": ["proxy1.example.com:8080"]
    }
    
    success = integration.add_route_for_crawler(crawler_config)
    print(f"Route added to routing engine: {success}")
    
    # Get configuration for a specific domain
    config = integration.get_crawler_config_for_domain("example.com")
    print(f"Crawler config for example.com: {config}")

if __name__ == "__main__":
    example_integration()