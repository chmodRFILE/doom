#!/usr/bin/env python3
"""
Dynamic Routing Engine for the Infinite XOR-Salted Spider Network System
This module handles route configuration, real-time updates, and distribution
"""

import json
import os
import threading
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DynamicRoutingEngine:
    """
    Dynamic Routing Engine for managing spider network routes
    Implements the requirements from mindmap v1.0 for route configuration,
    real-time updates, and distribution
    """
    
    def __init__(self, config_path: str = "config/routing_config.json"):
        """
        Initialize the dynamic routing engine
        
        Args:
            config_path (str): Path to the routing configuration file
        """
        self.config_path = config_path
        self.routes: Dict[str, Any] = {}
        self.route_lock = threading.Lock()
        self.version_history: List[Dict] = []
        self.current_version = 0
        self._load_config()
        
    def _load_config(self) -> None:
        """Load routing configuration from file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.routes = json.load(f)
                logger.info(f"Loaded routing configuration from {self.config_path}")
            else:
                # Create default configuration
                self._create_default_config()
                logger.info("Created default routing configuration")
        except Exception as e:
            logger.error(f"Error loading routing config: {e}")
            self._create_default_config()
    
    def _create_default_config(self) -> None:
        """Create a default routing configuration"""
        self.routes = {
            "routes": [],
            "version": 0,
            "last_updated": datetime.now().isoformat(),
            "validation": {
                "enabled": True,
                "rules": [
                    {"type": "domain_format", "enabled": True},
                    {"type": "proxy_format", "enabled": True},
                    {"type": "user_agent_valid", "enabled": True}
                ]
            }
        }
        self._save_config()
    
    def _save_config(self) -> None:
        """Save current routing configuration to file"""
        try:
            # Create directory if it doesn't exist
            Path(self.config_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Update version and timestamp
            self.routes["version"] = self.current_version
            self.routes["last_updated"] = datetime.now().isoformat()
            
            with open(self.config_path, 'w') as f:
                json.dump(self.routes, f, indent=2)
                
            logger.info(f"Saved routing configuration to {self.config_path}")
        except Exception as e:
            logger.error(f"Error saving routing config: {e}")
    
    def add_route(self, route_config: Dict[str, Any]) -> bool:
        """
        Add a new route configuration
        
        Args:
            route_config (Dict): Route configuration including target domains, proxies, etc.
            
        Returns:
            bool: True if successful
        """
        try:
            with self.route_lock:
                # Validate the route configuration
                if not self._validate_route(route_config):
                    logger.warning("Route validation failed")
                    return False
                
                # Add to routes list
                if "routes" not in self.routes:
                    self.routes["routes"] = []
                
                self.routes["routes"].append(route_config)
                self.current_version += 1
                
                # Save configuration
                self._save_config()
                
                logger.info(f"Added new route for {route_config.get('target_domains', 'unknown')}")
                return True
                
        except Exception as e:
            logger.error(f"Error adding route: {e}")
            return False
    
    def update_route(self, route_id: str, updated_config: Dict[str, Any]) -> bool:
        """
        Update an existing route configuration
        
        Args:
            route_id (str): Identifier for the route to update
            updated_config (Dict): Updated route configuration
            
        Returns:
            bool: True if successful
        """
        try:
            with self.route_lock:
                # Find and update the route
                for i, route in enumerate(self.routes["routes"]):
                    if route.get("id") == route_id:
                        # Merge updated config with existing route
                        route.update(updated_config)
                        
                        # Update version
                        self.current_version += 1
                        
                        # Save configuration
                        self._save_config()
                        
                        logger.info(f"Updated route {route_id}")
                        return True
                
                logger.warning(f"Route {route_id} not found for update")
                return False
                
        except Exception as e:
            logger.error(f"Error updating route: {e}")
            return False
    
    def remove_route(self, route_id: str) -> bool:
        """
        Remove a route configuration
        
        Args:
            route_id (str): Identifier for the route to remove
            
        Returns:
            bool: True if successful
        """
        try:
            with self.route_lock:
                # Find and remove the route
                routes = self.routes["routes"]
                for i, route in enumerate(routes):
                    if route.get("id") == route_id:
                        routes.pop(i)
                        
                        # Update version
                        self.current_version += 1
                        
                        # Save configuration
                        self._save_config()
                        
                        logger.info(f"Removed route {route_id}")
                        return True
                
                logger.warning(f"Route {route_id} not found for removal")
                return False
                
        except Exception as e:
            logger.error(f"Error removing route: {e}")
            return False
    
    def get_route(self, target_domain: str) -> Optional[Dict[str, Any]]:
        """
        Get the appropriate route for a given target domain
        
        Args:
            target_domain (str): The domain to find a route for
            
        Returns:
            Dict or None: Route configuration if found
        """
        try:
            with self.route_lock:
                # Simple matching - in a real implementation, this could be more sophisticated
                for route in self.routes["routes"]:
                    domains = route.get("target_domains", [])
                    if target_domain in domains:
                        return route
                
                # Return default route if no specific match found
                default_route = self._get_default_route()
                if default_route:
                    return default_route
                    
                return None
                
        except Exception as e:
            logger.error(f"Error getting route for {target_domain}: {e}")
            return None
    
    def get_all_routes(self) -> List[Dict[str, Any]]:
        """Get all configured routes"""
        try:
            with self.route_lock:
                return self.routes.get("routes", [])
        except Exception as e:
            logger.error(f"Error getting all routes: {e}")
            return []
    
    def _validate_route(self, route_config: Dict[str, Any]) -> bool:
        """
        Validate a route configuration
        
        Args:
            route_config (Dict): Route configuration to validate
            
        Returns:
            bool: True if valid
        """
        try:
            # Check required fields
            if not route_config.get("target_domains"):
                logger.warning("Route missing target_domains")
                return False
                
            if not isinstance(route_config["target_domains"], list):
                logger.warning("target_domains must be a list")
                return False
            
            # Run validation rules
            validation = self.routes.get("validation", {})
            rules = validation.get("rules", [])
            
            for rule in rules:
                if rule["enabled"]:
                    if not self._run_validation_rule(rule, route_config):
                        logger.warning(f"Route failed validation rule: {rule['type']}")
                        return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating route: {e}")
            return False
    
    def _run_validation_rule(self, rule: Dict[str, Any], route_config: Dict[str, Any]) -> bool:
        """
        Run a specific validation rule
        
        Args:
            rule (Dict): Validation rule configuration
            route_config (Dict): Route configuration to validate
            
        Returns:
            bool: True if rule passes
        """
        try:
            rule_type = rule["type"]
            
            if rule_type == "domain_format":
                domains = route_config.get("target_domains", [])
                for domain in domains:
                    if not self._is_valid_domain(domain):
                        return False
                        
            elif rule_type == "proxy_format":
                proxies = route_config.get("proxies", [])
                for proxy in proxies:
                    if not self._is_valid_proxy(proxy):
                        return False
                        
            elif rule_type == "user_agent_valid":
                user_agent = route_config.get("user_agent")
                if user_agent and not isinstance(user_agent, str):
                    return False
                    
            return True
            
        except Exception as e:
            logger.error(f"Error running validation rule {rule['type']}: {e}")
            return False
    
    def _is_valid_domain(self, domain: str) -> bool:
        """Validate domain format"""
        # Simple domain validation - in real implementation could be more robust
        import re
        pattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, domain))
    
    def _is_valid_proxy(self, proxy: str) -> bool:
        """Validate proxy format"""
        # Simple proxy validation - in real implementation could be more robust
        import re
        pattern = r'^[a-zA-Z0-9.-]+:\d+$'
        return bool(re.match(pattern, proxy))
    
    def _get_default_route(self) -> Optional[Dict[str, Any]]:
        """Get default route configuration"""
        # This would contain fallback routing logic
        return {
            "id": "default",
            "target_domains": ["*"],
            "user_agent": "Mozilla/5.0 (compatible; Spider/1.0)",
            "delay_range": [1, 3],
            "max_retries": 3,
            "priority": 0
        }
    
    def hot_reload(self) -> bool:
        """
        Reload configuration from file (hot reload capability)
        
        Returns:
            bool: True if successful
        """
        try:
            self._load_config()
            logger.info("Routing engine successfully reloaded")
            return True
        except Exception as e:
            logger.error(f"Error during hot reload: {e}")
            return False
    
    def rollback_to_version(self, version: int) -> bool:
        """
        Rollback to a previous configuration version
        
        Args:
            version (int): Version number to rollback to
            
        Returns:
            bool: True if successful
        """
        try:
            # In a real implementation, this would restore from version history
            logger.info(f"Rollback to version {version} not implemented in basic version")
            return False
        except Exception as e:
            logger.error(f"Error during rollback: {e}")
            return False
    
    def get_route_distribution(self) -> Dict[str, Any]:
        """
        Get statistics about route distribution
        
        Returns:
            Dict: Distribution statistics
        """
        try:
            with self.route_lock:
                total_routes = len(self.routes.get("routes", []))
                domain_count = 0
                proxy_count = 0
                
                for route in self.routes.get("routes", []):
                    domains = route.get("target_domains", [])
                    proxies = route.get("proxies", [])
                    domain_count += len(domains)
                    proxy_count += len(proxies)
                
                return {
                    "total_routes": total_routes,
                    "total_domains": domain_count,
                    "total_proxies": proxy_count,
                    "version": self.routes.get("version", 0),
                    "last_updated": self.routes.get("last_updated")
                }
        except Exception as e:
            logger.error(f"Error getting route distribution: {e}")
            return {}
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about the routing engine
        
        Returns:
            Dict: Statistics about the routing engine
        """
        try:
            return {
                "engine": "DynamicRoutingEngine",
                "version": self.routes.get("version", 0),
                "last_updated": self.routes.get("last_updated"),
                "route_count": len(self.routes.get("routes", [])),
                "distribution": self.get_route_distribution()
            }
        except Exception as e:
            logger.error(f"Error getting engine statistics: {e}")
            return {}

# Example usage function
def example_usage():
    """Example of how to use the DynamicRoutingEngine"""
    
    # Initialize the routing engine
    router = DynamicRoutingEngine()
    
    # Add a sample route
    sample_route = {
        "id": "example-route-1",
        "target_domains": ["example.com", "test.org"],
        "user_agent": "CustomSpider/1.0",
        "delay_range": [2, 5],
        "proxies": ["proxy1.example.com:8080", "proxy2.example.com:3128"],
        "max_retries": 5,
        "priority": 1
    }
    
    success = router.add_route(sample_route)
    print(f"Route added successfully: {success}")
    
    # Get the route back
    route = router.get_route("example.com")
    print(f"Retrieved route: {route}")
    
    # Get all routes
    all_routes = router.get_all_routes()
    print(f"All routes: {len(all_routes)} found")
    
    # Get statistics
    stats = router.get_statistics()
    print(f"Engine statistics: {stats}")

if __name__ == "__main__":
    example_usage()