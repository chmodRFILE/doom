from flask import Blueprint, render_template, request, jsonify
import json
import os

# Import crawler classes directly (absolute imports)
from crawler.improved_doom_crawler import ImprovedDoomCrawler
from database.version_manager import VersionManager
from database.safe_db_operations import SafeDBOperations
from enhanced_random_crawler_generator import EnhancedRandomCrawlerGenerator

# Initialize the blueprint
tools_bp = Blueprint('tools', __name__)

# Initialize database operations
db_ops = SafeDBOperations()
version_manager = VersionManager()

@tools_bp.route('/tools')
def tools_page():
    return render_template('tools.html')

@tools_bp.route('/tools/status')
def get_tool_status():
    # Return basic status information
    status = {
        'crawler': 'active',
        'database': 'connected',
        'proxy_support': True,
        'version': version_manager.get_current_version()
    }
    return jsonify(status)

@tools_bp.route('/tools/random-crawler')
def random_crawler_page():
    """Page for generating random crawlers"""
    return render_template('random_crawler.html')

@tools_bp.route('/tools/generate-random-config', methods=['GET'])
def generate_random_config():
    """Generate a random crawler configuration"""
    try:
        generator = EnhancedRandomCrawlerGenerator()
        config = generator.generate_random_crawler_config()
        return jsonify({
            'success': True,
            'config': config
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@tools_bp.route('/tools/create-random-crawler', methods=['POST'])
def create_random_crawler():
    """Create a new random crawler instance"""
    try:
        generator = EnhancedRandomCrawlerGenerator()
        crawler = generator.create_random_crawler()
        
        # Get the configuration for return
        config = generator.generate_random_crawler_config()
        
        return jsonify({
            'success': True,
            'message': 'Random crawler created successfully',
            'config': config
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@tools_bp.route('/tools/generate-recipe', methods=['GET'])
def generate_recipe():
    """Generate a random crawler recipe"""
    try:
        generator = EnhancedRandomCrawlerGenerator()
        recipe = generator.generate_crawler_recipe("random")
        return jsonify({
            'success': True,
            'recipe': recipe
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Additional tool routes can be added here