# XOR-Salted Encryption Architecture

This module implements the XOR-salted encryption system for the Doom Spider Network, providing secure communication between spiders and C2 systems.

## Architecture Overview

The XOR encryption system is built on three core components:

1. **XORKeyRing**: Manages encryption keys with lifecycle management
2. **XORRollArchitecture**: Implements rolling encryption mechanism with version control
3. **XORSaltingEncryption**: Core XOR encryption/decryption functionality

## Key Features

### 1. Key Management (XORKeyRing)
- Secure key storage and retrieval
- Key rotation capabilities
- Support for symmetric and asymmetric keys
- Persistent storage using JSON files
- Thread-safe operations

### 2. Roll Architecture (XORRollArchitecture)
- Dynamic roll creation for each target
- Salt management for enhanced security
- Version control for encryption keys
- Roll expiration and history tracking
- Integration with keyring system

### 3. Encryption System (XORSaltingEncryption)
- XOR-based salting encryption algorithm
- Secure data encryption/decryption
- Command-level encryption for spider communication
- Integration with routing engine configurations

## Usage Examples

### Basic Encryption/Decryption
```python
# Initialize the system
keyring = XORKeyRing()
roll_architecture = XORRollArchitecture(keyring)
encryption_system = XORSaltingEncryption(keyring, roll_architecture)

# Encrypt data
salt = encryption_system.generate_salt()
encrypted_data = encryption_system.encrypt_data("Secret message", salt)

# Decrypt data  
decrypted_data = encryption_system.decrypt_data(encrypted_data, salt)
```

### Route Configuration Encryption
```python
# Integrate with routing engine
integration = XORRoutingIntegration()

# Encrypt route configuration
route_config = {
    "id": "route_001",
    "target_domains": ["example.com"],
    "user_agent": "CustomSpider/1.0"
}

encrypted_route = integration.encrypt_route_config(route_config, "example.com")
```

## Security Features

- **Salt-based XOR encryption**: Each encryption operation uses a unique salt
- **Roll-based key management**: Keys rotate automatically for enhanced security
- **Thread-safe operations**: All components are thread-safe for concurrent access
- **Persistent storage**: Keyring and roll history stored in JSON files
- **Audit logging**: Comprehensive logging of all encryption operations

## Integration with Routing Engine

The XOR system integrates seamlessly with the routing engine to:
- Secure route configurations before transmission
- Encrypt communication between spiders and C2 systems
- Maintain secure key management for different spider targets