#!/usr/bin/env python3
"""
Web interface routes for XOR encryption system
"""

from flask import Blueprint, render_template, request, jsonify
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

xor_bp = Blueprint('xor', __name__, url_prefix='/xor')

@xor_bp.route('/')
def xor_dashboard():
    """XOR encryption dashboard"""
    return render_template('xor_dashboard.html')

@xor_bp.route('/status')
def xor_status():
    """Get XOR encryption system status"""
    try:
        # Get the XOR integration from app context
        xor_integration = None
        if hasattr(xor_bp, 'app'):
            xor_integration = getattr(xor_bp.app, 'xor_integration', None)
        
        if not xor_integration:
            return jsonify({'error': 'XOR integration not initialized'}), 400
        
        status = xor_integration.get_encryption_status()
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"Error getting XOR status: {e}")
        return jsonify({'error': str(e)}), 500

@xor_bp.route('/keys/generate', methods=['POST'])
def generate_key():
    """Generate a new encryption key"""
    try:
        # Get the XOR integration from app context
        xor_integration = None
        if hasattr(xor_bp, 'app'):
            xor_integration = getattr(xor_bp.app, 'xor_integration', None)
        
        if not xor_integration:
            return jsonify({'error': 'XOR integration not initialized'}), 400
        
        data = request.get_json()
        key_id = data.get('key_id')
        key_type = data.get('key_type', 'symmetric')
        
        if not key_id:
            return jsonify({'error': 'Key ID is required'}), 400
            
        key_data = xor_integration.keyring.generate_key_pair(key_id, key_type)
        return jsonify(key_data)
        
    except Exception as e:
        logger.error(f"Error generating key: {e}")
        return jsonify({'error': str(e)}), 500

@xor_bp.route('/keys/<key_id>', methods=['GET'])
def get_key(key_id):
    """Get a specific encryption key"""
    try:
        # Get the XOR integration from app context
        xor_integration = None
        if hasattr(xor_bp, 'app'):
            xor_integration = getattr(xor_bp.app, 'xor_integration', None)
        
        if not xor_integration:
            return jsonify({'error': 'XOR integration not initialized'}), 400
        
        key_data = xor_integration.keyring.get_key(key_id)
        if not key_data:
            return jsonify({'error': 'Key not found'}), 404
            
        return jsonify(key_data)
        
    except Exception as e:
        logger.error(f"Error getting key: {e}")
        return jsonify({'error': str(e)}), 500

@xor_bp.route('/rolls/create', methods=['POST'])
def create_roll():
    """Create a new encryption roll"""
    try:
        # Get the XOR integration from app context
        xor_integration = None
        if hasattr(xor_bp, 'app'):
            xor_integration = getattr(xor_bp.app, 'xor_integration', None)
        
        if not xor_integration:
            return jsonify({'error': 'XOR integration not initialized'}), 400
        
        data = request.get_json()
        target_id = data.get('target_id')
        key_id = data.get('key_id')
        
        if not target_id or not key_id:
            return jsonify({'error': 'Target ID and Key ID are required'}), 400
            
        roll = xor_integration.roll_architecture.create_roll(target_id, key_id)
        return jsonify(roll)
        
    except Exception as e:
        logger.error(f"Error creating roll: {e}")
        return jsonify({'error': str(e)}), 500

@xor_bp.route('/rolls/<roll_id>', methods=['GET'])
def get_roll(roll_id):
    """Get a specific encryption roll"""
    try:
        # Get the XOR integration from app context
        xor_integration = None
        if hasattr(xor_bp, 'app'):
            xor_integration = getattr(xor_bp.app, 'xor_integration', None)
        
        if not xor_integration:
            return jsonify({'error': 'XOR integration not initialized'}), 400
        
        roll = xor_integration.roll_architecture.get_roll(roll_id)
        if not roll:
            return jsonify({'error': 'Roll not found'}), 404
            
        return jsonify(roll)
        
    except Exception as e:
        logger.error(f"Error getting roll: {e}")
        return jsonify({'error': str(e)}), 500

@xor_bp.route('/encrypt', methods=['POST'])
def encrypt_data():
    """Encrypt data using XOR salting"""
    try:
        # Get the XOR integration from app context
        xor_integration = None
        if hasattr(xor_bp, 'app'):
            xor_integration = getattr(xor_bp.app, 'xor_integration', None)
        
        if not xor_integration:
            return jsonify({'error': 'XOR integration not initialized'}), 400
        
        data = request.get_json()
        plaintext = data.get('data')
        salt = data.get('salt')
        key_id = data.get('key_id')
        
        if not plaintext:
            return jsonify({'error': 'Data to encrypt is required'}), 400
            
        # For simplicity, we'll use the default encryption method
        encrypted = xor_integration.encryption_system.encrypt_data(plaintext, salt)
        return jsonify({'encrypted_data': encrypted})
        
    except Exception as e:
        logger.error(f"Error encrypting data: {e}")
        return jsonify({'error': str(e)}), 500

@xor_bp.route('/decrypt', methods=['POST'])
def decrypt_data():
    """Decrypt data using XOR salting"""
    try:
        # Get the XOR integration from app context
        xor_integration = None
        if hasattr(xor_bp, 'app'):
            xor_integration = getattr(xor_bp.app, 'xor_integration', None)
        
        if not xor_integration:
            return jsonify({'error': 'XOR integration not initialized'}), 400
        
        data = request.get_json()
        encrypted_data = data.get('data')
        salt = data.get('salt')
        
        if not encrypted_data:
            return jsonify({'error': 'Encrypted data is required'}), 400
            
        # For simplicity, we'll use the default decryption method
        decrypted = xor_integration.encryption_system.decrypt_data(encrypted_data, salt)
        return jsonify({'decrypted_data': decrypted})
        
    except Exception as e:
        logger.error(f"Error decrypting data: {e}")
        return jsonify({'error': str(e)}), 500

def register_xor_routes(app):
    """Register XOR routes with the Flask app"""
    app.register_blueprint(xor_bp)