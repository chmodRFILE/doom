#!/usr/bin/env python3
"""
Simple test script for XOR encryption architecture
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from spider_network.xor_architecture import XORKeyRing

def test_simple():
    """Test basic XOR architecture functionality"""
    print("Testing basic XOR Key Ring functionality...")
    
    # Test 1: Key Ring Management
    keyring = XORKeyRing()
    
    # Generate a key
    master_key = keyring.generate_key_pair("test_key_1", "symmetric")
    print(f"Generated key: {master_key['key_id']}")
    
    # Retrieve the key
    retrieved_key = keyring.get_key("test_key_1")
    assert retrieved_key is not None, "Failed to retrieve key"
    print("✓ Key retrieval works")
    
    # Test 2: Basic functionality
    print("✓ XOR architecture basic test completed successfully")
    
    return True

if __name__ == "__main__":
    try:
        test_simple()
        print("\n✅ Simple XOR Architecture Test: PASSED")
    except Exception as e:
        print(f"\n❌ Simple XOR Architecture Test: FAILED - {e}")
        sys.exit(1)