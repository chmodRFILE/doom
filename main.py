#!/usr/bin/env python3
"""
Main-Datei für das Doom Web Crawling System
"""

import sys
import os
import logging

# Füge das aktuelle Verzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.doom_sqldb import DoomSQLDB
from database.safe_db_operations import SafeDBOperations
from database.version_manager import VersionManager
from crawler.improved_doom_crawler import ImprovedDoomCrawler
from web_interface.app import create_app
from routing_engine.dynamic_routing_engine import DynamicRoutingEngine
from routing_engine.xor_routing_integration import XORRoutingIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    print("Starting Doom Web Crawling System...")
    
    # Initialisiere die Komponenten
    db = DoomSQLDB('database/doom.db')
    safe_db = SafeDBOperations('database/doom.db')
    version_manager = VersionManager('database/doom.db')
    crawler = ImprovedDoomCrawler()
    
    # Initialize the dynamic routing engine
    try:
        routing_engine = DynamicRoutingEngine()
        logger.info("Dynamic Routing Engine initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize routing engine: {e}")
        routing_engine = None
    
    # Initialize XOR encryption system
    try:
        xor_integration = XORRoutingIntegration()
        logger.info("XOR Encryption System initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize XOR encryption system: {e}")
        xor_integration = None
    
    # Erstelle die Flask-Anwendung
    app = create_app(safe_db, version_manager, crawler, routing_engine, xor_integration)
    
    print("System initialized successfully!")
    print("Starting web interface on http://localhost:5000")
    
    # Starte die Web-Anwendung
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main()