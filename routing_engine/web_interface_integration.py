#!/usr/bin/env python3
"""
Web Interface Integration for Dynamic Routing Engine Management
"""

from flask import Blueprint, render_template, request, jsonify
from routing_engine.dynamic_routing_engine import DynamicRoutingEngine
import json

# Create blueprint for routing management routes
routing_management_bp = Blueprint('routing_management', __name__, url_prefix='/routing')

# Initialize the routing engine
routing_engine = DynamicRoutingEngine()

@routing_management_bp.route('/')
def routing_dashboard():
    """Display the routing dashboard"""
    stats = routing_engine.get_statistics()
    routes = routing_engine.get_all_routes()
    
    return render_template('routing_dashboard.html', 
                         stats=stats, 
                         routes=routes)

@routing_management_bp.route('/routes')
def get_routes():
    """Get all configured routes"""
    try:
        routes = routing_engine.get_all_routes()
        return jsonify({
            "success": True,
            "routes": routes
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@routing_management_bp.route('/routes', methods=['POST'])
def add_route():
    """Add a new route"""
    try:
        data = request.get_json()
        success = routing_engine.add_route(data)
        
        if success:
            return jsonify({
                "success": True,
                "message": "Route added successfully"
            })
        else:
            return jsonify({
                "success": False,
                "error": "Failed to add route"
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@routing_management_bp.route('/routes/<route_id>', methods=['PUT'])
def update_route(route_id):
    """Update an existing route"""
    try:
        data = request.get_json()
        success = routing_engine.update_route(route_id, data)
        
        if success:
            return jsonify({
                "success": True,
                "message": "Route updated successfully"
            })
        else:
            return jsonify({
                "success": False,
                "error": "Failed to update route"
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@routing_management_bp.route('/routes/<route_id>', methods=['DELETE'])
def delete_route(route_id):
    """Delete a route"""
    try:
        success = routing_engine.remove_route(route_id)
        
        if success:
            return jsonify({
                "success": True,
                "message": "Route deleted successfully"
            })
        else:
            return jsonify({
                "success": False,
                "error": "Failed to delete route"
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@routing_management_bp.route('/stats')
def get_stats():
    """Get routing engine statistics"""
    try:
        stats = routing_engine.get_statistics()
        return jsonify({
            "success": True,
            "stats": stats
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@routing_management_bp.route('/reload', methods=['POST'])
def reload_config():
    """Reload configuration from file"""
    try:
        success = routing_engine.hot_reload()
        
        if success:
            return jsonify({
                "success": True,
                "message": "Configuration reloaded successfully"
            })
        else:
            return jsonify({
                "success": False,
                "error": "Failed to reload configuration"
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

# Add the routing management routes to the main app
def register_routing_routes(app):
    """Register routing management routes with the Flask application"""
    app.register_blueprint(routing_management_bp)