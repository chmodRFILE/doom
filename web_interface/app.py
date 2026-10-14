from flask import Flask, render_template
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the tool routes after setting up the path
from web_interface.tool_routes import tools_bp
from routing_engine.web_interface_integration import register_routing_routes
from routing_engine.xor_web_interface_integration import register_xor_routes

def create_app(safe_db=None, version_manager=None, crawler=None, routing_engine=None, xor_integration=None):
    """Factory function to create a Flask application"""
    app = Flask(__name__)
    
    # Store instances in app context
    app.safe_db = safe_db
    app.version_manager = version_manager
    app.crawler = crawler
    app.routing_engine = routing_engine
    app.xor_integration = xor_integration
    
    # Register blueprints
    app.register_blueprint(tools_bp, url_prefix='/tools')
    
    # Register routing management routes if available
    if routing_engine:
        register_routing_routes(app)
        
    # Register XOR encryption routes if available
    if xor_integration:
        register_xor_routes(app)
    
    # Add routes for the random crawler page
    @app.route('/tools/random-crawler')
    def random_crawler():
        return render_template('random_crawler.html')
    
    # Add a simple health check route
    @app.route('/')
    def index():
        return render_template('random_crawler.html')
    
    return app

# For direct execution (development)
if __name__ == '__main__':
    # Create a basic app for development
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)