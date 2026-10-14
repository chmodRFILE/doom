#!/usr/bin/env python3
"""
Integration module for XOR encryption system with the routing engine
"""

import json
import os
import threading
from typing import Dict, Any, Optional
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our XOR architecture components
from spider_network.xor_architecture import XORSaltingEncryption, XORKeyRing, XORRollArchitecture

class XORRoutingIntegration:
    """
    Integration layer between XOR encryption system and routing engine
    Handles secure communication between spiders and C2 systems through routing
    """
    
    def __init__(self, config_path: str = "config/xor_config.json"):
        """
        Initialize the XOR-routing integration
        
        Args:
            config_path (str): Path to XOR configuration file
        """
        self.config_path = config_path
        self.config = {}
        self.keyring = None
        self.roll_architecture = None
        self.encryption_system = None
        self.integration_lock = threading.Lock()
        
        # Load configuration
        self._load_config()
        
        # Initialize components
        self._initialize_components()
    
    def _load_config(self) -> None:
        """Load XOR configuration from file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
                logger.info(f"Loaded XOR configuration from {self.config_path}")
            else:
                # Create default configuration
                self._create_default_config()
                logger.info("Created default XOR configuration")
        except Exception as e:
            logger.error(f"Error loading XOR config: {e}")
            self._create_default_config()
    
    def _create_default_config(self) -> None:
        """Create a default XOR configuration"""
        self.config = {
            "xor_system": {
                "encryption_algorithm": "xor_salting",
                "salt_length": 32,
                "key_rotation_interval": 86400,
                "roll_history_limit": 1000,
                "max_key_storage": 100,
                "security_level": "high"
            },
            "keyring": {
                "storage_path": "storage/keyring.json",
                "default_keys": {
                    "master_key": "default_master_key_1234567890",
                    "c2_key": "c2_key_1234567890",
                    "spider_key": "spider_key_1234567890"
                }
            },
            "roll_architecture": {
                "default_roll_duration": 3600,
                "roll_rotation_enabled": true,
                "audit_logging": true
            }
        }
        self._save_config()
    
    def _save_config(self) -> None:
        """Save current XOR configuration to file"""
        try:
            # Create directory if it doesn't exist
            Path(self.config_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
                
            logger.info(f"Saved XOR configuration to {self.config_path}")
        except Exception as e:
            logger.error(f"Error saving XOR config: {e}")
    
    def _initialize_components(self) -> None:
        """Initialize all XOR system components"""
        try:
            with self.integration_lock:
                # Initialize keyring
                keyring_storage = self.config.get("keyring", {}).get("storage_path", "storage/keyring.json")
                self.keyring = XORKeyRing(keyring_storage)
                
                # Initialize roll architecture
                self.roll_architecture = XORRollArchitecture(self.keyring)
                
                # Initialize encryption system
                self.encryption_system = XORSaltingEncryption(self.keyring, self.roll_architecture)
                
                logger.info("XOR routing integration components initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing XOR components: {e}")
            raise
    
    def encrypt_route_config(self, route_config: Dict[str, Any], target_domain: str) -> Dict[str, Any]:
        """
        Encrypt a route configuration for secure transmission
        
        Args:
            route_config (Dict): Route configuration to encrypt
            target_domain (str): Target domain for the route
            
        Returns:
            Dict: Encrypted route configuration
        """
        try:
            with self.integration_lock:
                # Create a roll for this domain if it doesn't exist
                roll = self.roll_architecture.get_roll(target_domain)
                if not roll:
                    roll = self.roll_architecture.create_roll(
                        target_id=target_domain,
                        key_id="default_key"
                    )
                
                # Encrypt the route configuration
                encrypted_config = {
                    "route_id": route_config.get("id"),
                    "target_domains": route_config.get("target_domains"),
                    "encrypted_data": {},
                    "roll_id": roll["roll_id"],
                    "timestamp": route_config.get("timestamp", 0),
                    "version": route_config.get("version", 1)
                }
                
                # Encrypt each field
                for key, value in route_config.items():
                    if key not in ["id", "target_domains", "timestamp", "version"]:
                        # Only encrypt non-configuration fields
                        if isinstance(value, str):
                            salt = self.encryption_system.generate_salt()
                            encrypted_value = self.encryption_system.encrypt_data(value, salt)
                            encrypted_config["encrypted_data"][key] = {
                                "value": encrypted_value,
                                "salt": salt
                            }
                        else:
                            # Convert to string and encrypt
                            salt = self.encryption_system.generate_salt()
                            encrypted_value = self.encryption_system.encrypt_data(str(value), salt)
                            encrypted_config["encrypted_data"][key] = {
                                "value": encrypted_value,
                                "salt": salt
                            }
                
                logger.info(f"Encrypted route configuration for {target_domain}")
                return encrypted_config
                
        except Exception as e:
            logger.error(f"Error encrypting route config: {e}")
            raise
    
    def decrypt_route_config(self, encrypted_config: Dict[str, Any], target_domain: str) -> Dict[str, Any]:
        """
        Decrypt a route configuration
        
        Args:
            encrypted_config (Dict): Encrypted route configuration
            target_domain (str): Target domain for the route
            
        Returns:
            Dict: Decrypted route configuration
        """
        try:
            with self.integration_lock:
                # Decrypt the route configuration
                decrypted_config = {
                    "id": encrypted_config.get("route_id"),
                    "target_domains": encrypted_config.get("target_domains"),
                    "timestamp": encrypted_config.get("timestamp"),
                    "version": encrypted_config.get("version")
                }
                
                # Decrypt each encrypted field
                for key, value in encrypted_config.get("encrypted_data", {}).items():
                    if isinstance(value, dict) and "value" in value and "salt" in value:
                        try:
                            decrypted_value = self.encryption_system.decrypt_data(
                                value["value"], 
                                value["salt"]
                            )
                            decrypted_config[key] = decrypted_value
                        except Exception as decrypt_error:
                            logger.warning(f"Failed to decrypt field {key}: {decrypt_error}")
                            decrypted_config[key] = value["value"]  # Keep original if decryption fails
                
                logger.info(f"Decrypted route configuration for {target_domain}")
                return decrypted_config
                
        except Exception as e:
            logger.error(f"Error decrypting route config: {e}")
            raise
    
    def get_encryption_status(self) -> Dict[str, Any]:
        """
        Get current encryption system status
        
        Returns:
            Dict: Status information
        """
        try:
            with self.integration_lock:
                return {
                    "keyring": {
                        "keys_count": len(self.keyring.keys.get("master_keys", {})),
                        "timestamp": self.keyring.keys.get("timestamp")
                    },
                    "roll_architecture": {
                        "active_rolls": len([r for r in self.roll_architecture.roll_history if r.get("status") == "active"]),
                        "total_rolls": len(self.roll_architecture.roll_history)
                    },
                    "encryption_system": {
                        "initialized": True
                    }
                }
        except Exception as e:
            logger.error(f"Error getting encryption status: {e}")
            return {"error": str(e)}

# Example usage
def example_usage():
    """Example of how to use the XOR routing integration"""
    
    # Initialize integration
    integration = XORRoutingIntegration()
    
    # Test route configuration
    test_route = {
        "id": "route_001",
        "target_domains": ["example.com", "test.org"],
        "user_agent": "CustomSpider/1.0",
        "delay_range": [2, 5],
        "proxies": ["proxy1.example.com:8080", "proxy2.example.com:3128"],
        "max_retries": 5,
        "priority": 1,
        "timestamp": 1640995200,
        "version": 1
    }
    
    # Encrypt the route
    encrypted = integration.encrypt_route_config(test_route, "example.com")
    print(f"Encrypted route: {encrypted}")
    
    # Decrypt it back
    decrypted = integration.decrypt_route_config(encrypted, "example.com")
    print(f"Decrypted route: {decrypted}")
    
    # Get status
    status = integration.get_encryption_status()
    print(f"Encryption status: {status}")

if __name__ == "__main__":
    example_usage()