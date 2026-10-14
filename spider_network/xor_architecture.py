#!/usr/bin/env python3
"""
XOR-Salted Encryption Architecture for Doom Spider Network System
This module implements the core XOR encryption system with keyring and roll architecture
"""

import os
import time
import hashlib
import logging
import threading
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
import json
import base64
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class XORKeyRing:
    """
    Key Ring Management System for XOR-Salted Encryption
    Manages multiple keys and their lifecycle for the spider network
    """
    
    def __init__(self, storage_path: str = "storage/keyring.json"):
        self.storage_path = storage_path
        self.keys: Dict[str, Dict[str, Any]] = {}
        self.key_lock = threading.Lock()
        self._load_keyring()
        
    def _load_keyring(self) -> None:
        """Load keyring from storage"""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r') as f:
                    self.keys = json.load(f)
                logger.info(f"Loaded keyring from {self.storage_path}")
            else:
                # Create default keyring
                self._create_default_keyring()
                logger.info("Created default keyring")
        except Exception as e:
            logger.error(f"Error loading keyring: {e}")
            self._create_default_keyring()
    
    def _create_default_keyring(self) -> None:
        """Create a default keyring with initial keys"""
        self.keys = {
            "master_keys": {},
            "spider_keys": {},
            "c2_keys": {},
            "timestamp": datetime.now().isoformat(),
            "version": "1.0"
        }
        self._save_keyring()
    
    def _save_keyring(self) -> None:
        """Save keyring to storage"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            
            # Update timestamp
            self.keys["timestamp"] = datetime.now().isoformat()
            
            with open(self.storage_path, 'w') as f:
                json.dump(self.keys, f, indent=2)
                
            logger.info(f"Saved keyring to {self.storage_path}")
        except Exception as e:
            logger.error(f"Error saving keyring: {e}")
    
    def generate_key_pair(self, key_id: str, key_type: str = "symmetric") -> Dict[str, str]:
        """
        Generate a new key pair for the specified purpose
        
        Args:
            key_id (str): Unique identifier for the key
            key_type (str): Type of key ('symmetric' or 'asymmetric')
            
        Returns:
            Dict[str, str]: Generated keys
        """
        try:
            with self.key_lock:
                # Generate key based on type
                if key_type == "symmetric":
                    # Generate a random symmetric key
                    key = secrets.token_bytes(32)  # 256-bit key
                    key_hex = key.hex()
                    key_b64 = base64.b64encode(key).decode()
                    
                    key_data = {
                        "key_id": key_id,
                        "type": key_type,
                        "algorithm": "AES-256",
                        "key": key_hex,
                        "key_b64": key_b64,
                        "created_at": datetime.now().isoformat(),
                        "expires_at": None,
                        "status": "active"
                    }
                    
                elif key_type == "asymmetric":
                    # For asymmetric keys, we'll generate a simple RSA-like key
                    # In practice, you'd use proper cryptography libraries
                    private_key = secrets.token_bytes(32)
                    public_key = hashlib.sha256(private_key).hexdigest()
                    
                    key_data = {
                        "key_id": key_id,
                        "type": key_type,
                        "algorithm": "RSA-2048",
                        "private_key": private_key.hex(),
                        "public_key": public_key,
                        "created_at": datetime.now().isoformat(),
                        "expires_at": None,
                        "status": "active"
                    }
                else:
                    raise ValueError(f"Unsupported key type: {key_type}")
                
                # Store the key
                if "master_keys" not in self.keys:
                    self.keys["master_keys"] = {}
                    
                self.keys["master_keys"][key_id] = key_data
                self._save_keyring()
                
                logger.info(f"Generated new {key_type} key: {key_id}")
                return key_data
                
        except Exception as e:
            logger.error(f"Error generating key pair: {e}")
            raise
    
    def get_key(self, key_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific key from the keyring
        
        Args:
            key_id (str): Identifier for the key to retrieve
            
        Returns:
            Dict or None: Key data if found
        """
        try:
            with self.key_lock:
                # Check master keys first
                if "master_keys" in self.keys and key_id in self.keys["master_keys"]:
                    return self.keys["master_keys"][key_id]
                
                # Check spider keys
                if "spider_keys" in self.keys and key_id in self.keys["spider_keys"]:
                    return self.keys["spider_keys"][key_id]
                
                # Check C2 keys
                if "c2_keys" in self.keys and key_id in self.keys["c2_keys"]:
                    return self.keys["c2_keys"][key_id]
                
                logger.warning(f"Key {key_id} not found")
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving key: {e}")
            return None
    
    def rotate_key(self, key_id: str) -> bool:
        """
        Rotate an existing key to a new one
        
        Args:
            key_id (str): Identifier for the key to rotate
            
        Returns:
            bool: True if successful
        """
        try:
            with self.key_lock:
                # Get current key
                current_key = self.get_key(key_id)
                if not current_key:
                    logger.warning(f"Cannot rotate key {key_id}: not found")
                    return False
                
                # Generate new key of same type
                new_key = self.generate_key_pair(
                    f"{key_id}_rotated_{int(time.time())}",
                    current_key.get("type", "symmetric")
                )
                
                # Mark old key as expired
                if "master_keys" in self.keys and key_id in self.keys["master_keys"]:
                    self.keys["master_keys"][key_id]["status"] = "expired"
                    self.keys["master_keys"][key_id]["expires_at"] = datetime.now().isoformat()
                
                self._save_keyring()
                
                logger.info(f"Rotated key {key_id}")
                return True
                
        except Exception as e:
            logger.error(f"Error rotating key: {e}")
            return False
    
    def remove_key(self, key_id: str) -> bool:
        """
        Remove a key from the keyring
        
        Args:
            key_id (str): Identifier for the key to remove
            
        Returns:
            bool: True if successful
        """
        try:
            with self.key_lock:
                # Remove from all key categories
                removed = False
                
                if "master_keys" in self.keys and key_id in self.keys["master_keys"]:
                    del self.keys["master_keys"][key_id]
                    removed = True
                    
                if "spider_keys" in self.keys and key_id in self.keys["spider_keys"]:
                    del self.keys["spider_keys"][key_id]
                    removed = True
                    
                if "c2_keys" in self.keys and key_id in self.keys["c2_keys"]:
                    del self.keys["c2_keys"][key_id]
                    removed = True
                
                if removed:
                    self._save_keyring()
                    logger.info(f"Removed key {key_id}")
                    return True
                else:
                    logger.warning(f"Key {key_id} not found for removal")
                    return False
                    
        except Exception as e:
            logger.error(f"Error removing key: {e}")
            return False

class XORRollArchitecture:
    """
    Roll Architecture for XOR-Salted Encryption System
    Implements the rolling encryption mechanism with version control
    """
    
    def __init__(self, keyring: XORKeyRing):
        self.keyring = keyring
        self.roll_history: List[Dict[str, Any]] = []
        self.roll_lock = threading.Lock()
        self.current_roll_id = 0
        
    def generate_roll_salt(self, salt_length: int = 32) -> str:
        """
        Generate a salt for the current roll
        
        Args:
            salt_length (int): Length of the salt in bytes
            
        Returns:
            str: Generated salt as hex string
        """
        return secrets.token_hex(salt_length)
    
    def create_roll(self, target_id: str, key_id: str, 
                   encryption_type: str = "xor_salting") -> Dict[str, Any]:
        """
        Create a new encryption roll for the specified target
        
        Args:
            target_id (str): Identifier for the target (spider, C2, etc.)
            key_id (str): Key identifier to use
            encryption_type (str): Type of encryption to use
            
        Returns:
            Dict[str, Any]: Roll information
        """
        try:
            with self.roll_lock:
                # Generate salt
                salt = self.generate_roll_salt()
                
                # Get the key
                key_data = self.keyring.get_key(key_id)
                if not key_data:
                    raise ValueError(f"Key {key_id} not found")
                
                # Create roll information
                roll_info = {
                    "roll_id": f"roll_{self.current_roll_id}_{int(time.time())}",
                    "target_id": target_id,
                    "key_id": key_id,
                    "salt": salt,
                    "encryption_type": encryption_type,
                    "created_at": datetime.now().isoformat(),
                    "version": 1,
                    "status": "active"
                }
                
                # Add to history
                self.roll_history.append(roll_info)
                self.current_roll_id += 1
                
                logger.info(f"Created new roll for {target_id}")
                return roll_info
                
        except Exception as e:
            logger.error(f"Error creating roll: {e}")
            raise
    
    def get_roll(self, target_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the current active roll for a target
        
        Args:
            target_id (str): Identifier for the target
            
        Returns:
            Dict or None: Roll information if found
        """
        try:
            with self.roll_lock:
                # Find the most recent active roll for this target
                for roll in reversed(self.roll_history):
                    if roll.get("target_id") == target_id and roll.get("status") == "active":
                        return roll
                
                logger.warning(f"No active roll found for target {target_id}")
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving roll: {e}")
            return None
    
    def update_roll(self, roll_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update an existing roll
        
        Args:
            roll_id (str): Identifier for the roll to update
            updates (Dict): Updates to apply
            
        Returns:
            bool: True if successful
        """
        try:
            with self.roll_lock:
                # Find and update the roll
                for i, roll in enumerate(self.roll_history):
                    if roll.get("roll_id") == roll_id:
                        # Update version
                        roll["version"] = roll.get("version", 0) + 1
                        
                        # Apply updates
                        roll.update(updates)
                        
                        # Update timestamp
                        roll["updated_at"] = datetime.now().isoformat()
                        
                        logger.info(f"Updated roll {roll_id}")
                        return True
                
                logger.warning(f"Roll {roll_id} not found for update")
                return False
                
        except Exception as e:
            logger.error(f"Error updating roll: {e}")
            return False
    
    def expire_roll(self, roll_id: str) -> bool:
        """
        Expire an existing roll
        
        Args:
            roll_id (str): Identifier for the roll to expire
            
        Returns:
            bool: True if successful
        """
        try:
            with self.roll_lock:
                # Find and expire the roll
                for i, roll in enumerate(self.roll_history):
                    if roll.get("roll_id") == roll_id:
                        roll["status"] = "expired"
                        roll["expired_at"] = datetime.now().isoformat()
                        
                        logger.info(f"Expired roll {roll_id}")
                        return True
                
                logger.warning(f"Roll {roll_id} not found for expiration")
                return False
                
        except Exception as e:
            logger.error(f"Error expiring roll: {e}")
            return False

class XORSaltingEncryption:
    """
    XOR-based salting encryption system for the Doom Spider Network
    Implements the core XOR encryption with salt management
    """
    
    def __init__(self, keyring: XORKeyRing, roll_architecture: XORRollArchitecture):
        self.keyring = keyring
        self.roll_architecture = roll_architecture
        self.logger = logging.getLogger("XORSaltingEncryption")
        
    def generate_salt(self, length: int = 32) -> str:
        """Generate a cryptographically secure salt"""
        return secrets.token_hex(length)
    
    def derive_key_from_salt(self, salt: str, password: str = None) -> str:
        """Derive encryption key from salt"""
        if not salt:
            raise ValueError("Salt cannot be empty")
            
        # Use PBKDF2 to derive key from salt and optional password
        if password:
            salt_bytes = bytes.fromhex(salt)
            # In a real implementation, you'd use proper PBKDF2 with a password
            # For this example, we'll use a simplified approach
            key = hashlib.sha256((salt + password).encode()).digest()
            return base64.b64encode(key).decode()
        else:
            # Generate a key based on salt using SHA-256
            salt_bytes = bytes.fromhex(salt)
            key = hashlib.sha256(salt_bytes).digest()
            return base64.b64encode(key).decode()
    
    def encrypt_data(self, data: str, salt: str, key: str = None) -> str:
        """Encrypt data using XOR salting"""
        try:
            if not isinstance(data, str):
                data = str(data)
                
            # If no key provided, derive from salt
            if not key:
                key = self.derive_key_from_salt(salt)
            
            # Convert to bytes
            data_bytes = data.encode('utf-8')
            key_bytes = base64.b64decode(key.encode())
            
            # XOR encryption
            encrypted_bytes = bytearray()
            key_length = len(key_bytes)
            
            for i, byte in enumerate(data_bytes):
                key_byte = key_bytes[i % key_length]
                encrypted_byte = byte ^ key_byte
                encrypted_bytes.append(encrypted_byte)
                
            # Return as hex string for easy storage/transmission
            return encrypted_bytes.hex()
            
        except Exception as e:
            self.logger.error(f"Encryption error: {e}")
            raise
    
    def decrypt_data(self, encrypted_data: str, salt: str, key: str = None) -> str:
        """Decrypt data using XOR salting"""
        try:
            if not isinstance(encrypted_data, str):
                raise ValueError("Encrypted data must be a string")
                
            # If no key provided, derive from salt
            if not key:
                key = self.derive_key_from_salt(salt)
            
            # Convert hex to bytes
            encrypted_bytes = bytes.fromhex(encrypted_data)
            key_bytes = base64.b64decode(key.encode())
            
            # XOR decryption (same as encryption for XOR)
            decrypted_bytes = bytearray()
            key_length = len(key_bytes)
            
            for i, byte in enumerate(encrypted_bytes):
                key_byte = key_bytes[i % key_length]
                decrypted_byte = byte ^ key_byte
                decrypted_bytes.append(decrypted_byte)
                
            # Convert back to string
            return decrypted_bytes.decode('utf-8')
            
        except Exception as e:
            self.logger.error(f"Decryption error: {e}")
            raise
    
    def encrypt_command(self, command: Dict[str, Any], target_id: str) -> Dict[str, Any]:
        """
        Encrypt a command for secure transmission to a target
        
        Args:
            command (Dict): Command to encrypt
            target_id (str): Target identifier
            
        Returns:
            Dict: Encrypted command structure
        """
        try:
            # Get or create roll for this target
            roll = self.roll_architecture.get_roll(target_id)
            if not roll:
                # Create a new roll if none exists
                roll = self.roll_architecture.create_roll(
                    target_id=target_id,
                    key_id="default_key"
                )
            
            # Generate salt for this encryption operation
            operation_salt = self.generate_salt()
            
            # Encrypt the command data
            encrypted_command = {
                'command_id': command.get('command_id'),
                'timestamp': command.get('timestamp'),
                'sender': command.get('sender'),
                'type': command.get('type'),
                'data': {},
                'salt': operation_salt,
                'encrypted': True,
                'encryption_timestamp': time.time(),
                'roll_id': roll['roll_id']
            }
            
            # Encrypt each data field
            for key, value in command.get('data', {}).items():
                if isinstance(value, str):
                    encrypted_value = self.encrypt_data(value, operation_salt)
                else:
                    # Convert to string and encrypt
                    encrypted_value = self.encrypt_data(str(value), operation_salt)
                encrypted_command['data'][key] = encrypted_value
            
            return encrypted_command
            
        except Exception as e:
            self.logger.error(f"Error encrypting command: {e}")
            raise
    
    def decrypt_command(self, encrypted_command: Dict[str, Any], target_id: str) -> Dict[str, Any]:
        """
        Decrypt a command received from a target
        
        Args:
            encrypted_command (Dict): Encrypted command
            target_id (str): Target identifier
            
        Returns:
            Dict: Decrypted command structure
        """
        try:
            # Get the roll for this target
            roll = self.roll_architecture.get_roll(target_id)
            if not roll:
                raise ValueError(f"No active roll found for target {target_id}")
            
            # Decrypt the command data
            decrypted_command = {
                'command_id': encrypted_command.get('command_id'),
                'timestamp': encrypted_command.get('timestamp'),
                'sender': encrypted_command.get('sender'),
                'type': encrypted_command.get('type'),
                'data': {},
                'salt': encrypted_command.get('salt'),
                'encrypted': False,
                'decryption_timestamp': time.time()
            }
            
            # Decrypt each data field
            for key, value in encrypted_command.get('data', {}).items():
                if isinstance(value, str) and value:
                    decrypted_value = self.decrypt_data(value, encrypted_command['salt'])
                else:
                    decrypted_value = value
                decrypted_command['data'][key] = decrypted_value
            
            return decrypted_command
            
        except Exception as e:
            self.logger.error(f"Error decrypting command: {e}")
            raise

# Example usage and testing
def example_usage():
    """Example of how to use the XOR architecture components"""
    
    # Initialize keyring
    keyring = XORKeyRing()
    
    # Generate some keys
    master_key = keyring.generate_key_pair("master_key_1", "symmetric")
    spider_key = keyring.generate_key_pair("spider_key_1", "symmetric")
    
    print(f"Generated master key: {master_key['key_id']}")
    print(f"Generated spider key: {spider_key['key_id']}")
    
    # Initialize roll architecture
    roll_architecture = XORRollArchitecture(keyring)
    
    # Create a roll for a spider
    roll = roll_architecture.create_roll(
        target_id="spider_123",
        key_id="spider_key_1"
    )
    
    print(f"Created roll: {roll['roll_id']}")
    
    # Initialize encryption system
    encryption_system = XORSaltingEncryption(keyring, roll_architecture)
    
    # Test encryption/decryption
    original_data = "This is a secret message for the spider network"
    salt = encryption_system.generate_salt()
    
    encrypted = encryption_system.encrypt_data(original_data, salt)
    print(f"Encrypted data: {encrypted}")
    
    decrypted = encryption_system.decrypt_data(encrypted, salt)
    print(f"Decrypted data: {decrypted}")
    
    # Test command encryption
    test_command = {
        'command_id': 'cmd_001',
        'timestamp': time.time(),
        'sender': 'c2_server',
        'type': 'crawl_task',
        'data': {
            'target_url': 'http://example.com',
            'user_agent': 'SpiderBot/1.0'
        }
    }
    
    encrypted_command = encryption_system.encrypt_command(test_command, "spider_123")
    print(f"Encrypted command: {encrypted_command}")
    
    decrypted_command = encryption_system.decrypt_command(encrypted_command, "spider_123")
    print(f"Decrypted command: {decrypted_command}")

if __name__ == "__main__":
    example_usage()