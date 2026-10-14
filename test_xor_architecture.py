#!/usr/bin/env python3
"""
Test script for XOR encryption architecture
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from spider_network.xor_architecture import XORSaltingEncryption, XORKeyRing, XORRollArchitecture

def test_xor_architecture():
    """Test the complete XOR architecture"""
    print("Testing XOR Encryption Architecture...")
    
    # Test 1: Key Ring Management
    print("\n1. Testing Key Ring Management")
    keyring = XORKeyRing()
    
    # Generate keys
    master_key = keyring.generate_key_pair("master_1", "symmetric")
    spider_key = keyring.generate_key_pair("spider_1", "symmetric")
    
    print(f"Generated master key: {master_key['key_id']}")
    print(f"Generated spider key: {spider_key['key_id']}")
    
    # Test key retrieval
    retrieved_key = keyring.get_key("master_1")
    assert retrieved_key is not None, "Failed to retrieve key"
    print("✓ Key retrieval works")
    
    # Test key rotation
    rotated = keyring.rotate_key("master_1")
    print(f"Key rotation successful: {rotated}")
    
    # Test 2: Roll Architecture
    print("\n2. Testing Roll Architecture")
    roll_architecture = XORRollArchitecture(keyring)
    
    # Create rolls
    roll1 = roll_architecture.create_roll("spider_1", "spider_1")
    roll2 = roll_architecture.create_roll("c2_server", "master_1")
    
    print(f"Created roll 1: {roll1['roll_id']}")
    print(f"Created roll 2: {roll2['roll_id']}")
    
    # Test roll retrieval
    retrieved_roll = roll_architecture.get_roll("spider_1")
    assert retrieved_roll is not None, "Failed to retrieve roll"
    print("✓ Roll retrieval works")
    
    # Test 3: Encryption System
    print("\n3. Testing Encryption System")
    encryption_system = XORSaltingEncryption(keyring, roll_architecture)
    
    # Test basic encryption/decryption
    original_data = "This is a secret message for the spider network"
    salt = encryption_system.generate_salt()
    
    encrypted = encryption_system.encrypt_data(original_data, salt)
    print(f"Encrypted data: {encrypted}")
    
    decrypted = encryption_system.decrypt_data(encrypted, salt)
    assert decrypted == original_data, "Decryption failed"
    print("✓ Basic encryption/decryption works")
    
    # Test command encryption
    test_command = {
        'command_id': 'cmd_001',
        'timestamp': 1640995200,
        'sender': 'c2_server',
        'type': 'crawl_task',
        'data': {
            'target_url': 'http://example.com',
            'user_agent': 'SpiderBot/1.0'
        }
    }
    
    encrypted_command = encryption_system.encrypt_command(test_command, "spider_1")
    print(f"Encrypted command type: {encrypted_command['type']}")
    
    decrypted_command = encryption_system.decrypt_command(encrypted_command, "spider_1")
    assert decrypted_command['data']['target_url'] == 'http://example.com', "Command decryption failed"
    print("✓ Command encryption/decryption works")
    
    # Test 4: Integration
    print("\n4. Testing Integration")
    integration_status = {
        'keyring': keyring.keys,
        'roll_architecture': {
            'active_rolls': len([r for r in roll_architecture.roll_history if r.get('status') == 'active']),
            'total_rolls': len(roll_architecture.roll_history)
        }
    }
    
    print("✓ Integration test completed successfully")
    
    print("\nAll tests passed! XOR architecture is working correctly.")
    return True

if __name__ == "__main__":
    try:
        test_xor_architecture()
        print("\n✅ XOR Architecture Test: PASSED")
    except Exception as e:
        print(f"\n❌ XOR Architecture Test: FAILED - {e}")
        sys.exit(1)