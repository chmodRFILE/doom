"""
Konfigurationsloader für das Web-Crawling-System
"""

import json
import os

def load_config(config_file='config/crawler_config.json'):
    """
    Lädt die Konfiguration aus einer JSON-Datei
    
    Args:
        config_file (str): Pfad zur Konfigurationsdatei
        
    Returns:
        dict: Konfigurationsdaten
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Erstelle eine Standard-Konfiguration
        default_config = {
            "max_workers": 5,
            "timeout": 30,
            "user_agent": "WebCrawler/1.0",
            "delay_between_requests": 1,
            "max_depth": 2,
            "allowed_domains": [],
            "proxy_rotation": True
        }
        # Speichere die Standard-Konfiguration
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4)
        return default_config

def load_proxy_list(proxy_file='config/proxy_list.txt'):
    """
    Lädt die Proxy-Liste aus einer Textdatei
    
    Args:
        proxy_file (str): Pfad zur Proxy-Liste
        
    Returns:
        list: Liste der Proxies
    """
    try:
        with open(proxy_file, 'r', encoding='utf-8') as f:
            proxies = [line.strip() for line in f if line.strip()]
            return proxies
    except FileNotFoundError:
        # Erstelle eine leere Proxy-Liste
        with open(proxy_file, 'w', encoding='utf-8') as f:
            pass  # Erstellt leere Datei
        return []