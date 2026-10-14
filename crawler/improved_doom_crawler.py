#!/usr/bin/env python3
"""
Verbesserter Crawler für das Doom-Projekt
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
import sqlite3
from datetime import datetime
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from config.config_loader import load_config
from typing import List, Optional, Dict, Any

# Konfiguration des Loggings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImprovedDoomCrawler:
    def __init__(self, max_workers: int = 5):
        """Initialisiert den Crawler mit maximaler Anzahl an Worker-Threads"""
        self.config = load_config()
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.config['user_agent']})
        self.max_workers = max_workers
        self.failed_urls = []
        self.successful_crawls = 0
        self.lock = threading.Lock()  # Für Thread-Sicherheit
        self.proxy_index = 0
        
        # Proxy-Konfiguration initialisieren
        if self.config.get('proxy_rotation', False):
            self.proxies = self.load_proxy_list()
        else:
            self.proxies = []

    def load_proxy_list(self) -> List[str]:
        """Lädt die Proxy-Liste aus der Konfiguration"""
        try:
            from config.config_loader import load_proxy_list
            return load_proxy_list()
        except Exception as e:
            logger.warning(f"Proxy-Liste konnte nicht geladen werden: {e}")
            return []

    def get_next_proxy(self) -> Optional[str]:
        """Gibt den nächsten Proxy aus der Liste zurück"""
        if not self.proxies:
            return None
            
        # Thread-safe proxy rotation
        with self.lock:
            proxy = self.proxies[self.proxy_index]
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy

    def fetch_page(self, url: str, timeout: int = 30) -> Optional[Dict[str, Any]]:
        """Holt eine Seite und gibt deren Inhalt zurück"""
        try:
            # Proxy auswählen
            proxy = self.get_next_proxy() if self.proxies else None
            
            # Anfrage senden
            response = self.session.get(
                url, 
                timeout=timeout,
                proxies={'http': proxy, 'https': proxy} if proxy else None
            )
            
            # Status-Code prüfen
            response.raise_for_status()
            
            # HTML parsen
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Daten extrahieren
            title = soup.title.string if soup.title else ""
            description = ""
            for meta in soup.find_all('meta', attrs={'name': 'description'}):
                description = meta.get('content', '')
                break
            
            # Textinhalt extrahieren
            text_content = soup.get_text()
            
            # Telefonnummern extrahieren
            phone_numbers = self.extract_phone_numbers(text_content)
            
            # E-Mail-Adressen extrahieren
            emails = self.extract_emails(text_content)
            
            # Benutzernamen extrahieren
            usernames = self.extract_usernames(text_content)
            
            return {
                'url': url,
                'title': title,
                'description': description,
                'content': text_content,
                'phone_numbers': phone_numbers,
                'emails': emails,
                'usernames': usernames,
                'status_code': response.status_code,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Fehler beim Abrufen von {url}: {e}")
            self.failed_urls.append(url)
            return None

    def extract_phone_numbers(self, text: str) -> List[str]:
        """Extrahiert Telefonnummern aus Text"""
        import re
        phone_pattern = r'\b(?:\+?49[-.\s]?)?\(?0?\d{1,4}[-.\s]?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}\b'
        return re.findall(phone_pattern, text)

    def extract_emails(self, text: str) -> List[str]:
        """Extrahiert E-Mail-Adressen aus Text"""
        import re
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)

    def extract_usernames(self, text: str) -> List[str]:
        """Extrahiert Benutzernamen aus Text"""
        import re
        # Sucht nach möglichen Benutzernamen (z.B. @username)
        username_pattern = r'@([A-Za-z0-9_]{3,20})'
        return re.findall(username_pattern, text)

    def crawl_urls(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Crawlt eine Liste von URLs"""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit tasks
            future_to_url = {executor.submit(self.crawl_single_url, url): url for url in urls}
            
            # Collect results
            for future in as_completed(future_to_url):
                result = future.result()
                if result:
                    results.append(result)
                    self.successful_crawls += 1
                    
        return results

    def crawl_single_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Crawlt eine einzelne URL"""
        try:
            # Wartezeit zwischen Anfragen
            time.sleep(self.config.get('delay_between_requests', 1))
            
            # Seite abrufen
            result = self.fetch_page(url)
            
            return result
        except Exception as e:
            logger.error(f"Fehler beim Crawlen von {url}: {e}")
            return None

    def get_crawling_stats(self) -> Dict[str, Any]:
        """Gibt Statistiken über das Crawling zurück"""
        return {
            'successful_crawls': self.successful_crawls,
            'failed_urls': len(self.failed_urls),
            'failed_urls_list': self.failed_urls
        }