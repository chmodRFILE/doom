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

# Konfiguration des Loggings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RobustProxyWebCrawler:
    def __init__(self, config_file='config/crawler_config.json', max_workers=5):
        self.config = load_config(config_file)
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.config['user_agent']})
        self.max_workers = max_workers
        self.failed_urls = []
        self.successful_crawls = 0
        self.lock = threading.Lock()  # Für Thread-Sicherheit
        self.proxy_index = 0
        
        # Proxy-Konfiguration initialisieren
        if self.config.get('use_proxies', False) and self.config.get('proxy_list'):
            self.proxies = self.config['proxy_list']
            logger.info(f"Proxy-Unterstützung aktiviert mit {len(self.proxies)} Proxies")
        elif self.config.get('use_proxies', False):
            # Versuche, Proxy-Liste aus Datei zu laden
            if self.config.get('proxy_list_file'):
                try:
                    with open(self.config['proxy_list_file'], 'r') as f:
                        proxy_lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                    self.proxies = proxy_lines
                    logger.info(f"Proxy-Unterstützung aktiviert mit {len(self.proxies)} Proxies aus Datei")
                except Exception as e:
                    logger.error(f"Fehler beim Laden der Proxy-Liste: {e}")
                    self.proxies = []
            else:
                self.proxies = []
            logger.info(f"Proxy-Unterstützung aktiviert mit {len(self.proxies)} Proxies")
        else:
            self.proxies = []
            logger.info("Proxy-Unterstützung deaktiviert")
    
    def get_next_proxy(self):
        """Ruft den nächsten Proxy aus der Liste ab (Round-Robin)"""
        if not self.proxies:
            return None
            
        proxy = self.proxies[self.proxy_index]
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def fetch_page_with_proxy(self, url, proxy=None):
        """Holt eine Seite mit optionalem Proxy"""
        try:
            # Proxy-Konfiguration
            proxies_dict = None
            if proxy:
                proxies_dict = {'http': proxy, 'https': proxy}
                logger.info(f"Verwende Proxy: {proxy}")
            
            response = self.session.get(url, timeout=self.config['timeout'], proxies=proxies_dict)
            response.raise_for_status()
            
            # Prüfen der Content-Length
            if len(response.content) > self.config['max_content_length']:
                logger.warning(f"Seite zu groß: {url}")
                return None
                
            return response.text
            
        except requests.exceptions.ProxyError as e:
            logger.error(f"Proxy-Fehler beim Abrufen von {url}: {e}")
            return None
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Verbindungsfehler beim Abrufen von {url}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Fehler beim Abrufen der Seite {url}: {e}")
            return None
    
    def fetch_page(self, url):
        """Holt eine Seite und gibt den Inhalt zurück"""
        # Wenn keine Proxies verfügbar sind, einfach ohne Proxy abrufen
        if not self.proxies:
            try:
                response = self.session.get(url, timeout=self.config['timeout'])
                response.raise_for_status()
                
                if len(response.content) > self.config['max_content_length']:
                    logger.warning(f"Seite zu groß: {url}")
                    return None
                    
                return response.text
                
            except requests.RequestException as e:
                logger.error(f"Fehler beim Abrufen der Seite {url}: {e}")
                return None
        
        # Versuche mit Proxies
        for i in range(len(self.proxies) + 1):  # +1 für den Fall, dass kein Proxy funktioniert
            proxy = self.get_next_proxy()  # Hier wird proxy korrekt initialisiert
            
            html_content = self.fetch_page_with_proxy(url, proxy)
            if html_content is not None:
                return html_content
                
        # Falls alle Proxies fehlgeschlagen sind, versuche ohne Proxy
        logger.info(f"Alle Proxies fehlgeschlagen, versuche ohne Proxy für {url}")
        try:
            response = self.session.get(url, timeout=self.config['timeout'])
            response.raise_for_status()
            
            if len(response.content) > self.config['max_content_length']:
                logger.warning(f"Seite zu groß: {url}")
                return None
                
            return response.text
            
        except requests.RequestException as e:
            logger.error(f"Fehler beim Abrufen der Seite {url} (ohne Proxy): {e}")
            return None
    
    def extract_data(self, html_content, url):
        """Extrahiert Daten aus dem HTML-Inhalt"""
        if not html_content:
            return {}
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Titel extrahieren
        title = soup.title.string if soup.title else ''
        
        # Beschreibung extrahieren
        description = ''
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            description = meta_desc.get('content', '')
            
        # Keywords extrahieren
        keywords = ''
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            keywords = meta_keywords.get('content', '')
            
        # Inhalt extrahieren (ohne Script- und Style-Tags)
        for script in soup(["script", "style"]):
            script.decompose()
        content = soup.get_text()[:1000]  # Erste 1000 Zeichen
        
        # Telefonnummern extrahieren
        phone_numbers = self.extract_phone_numbers(content)
        
        # E-Mail-Adressen extrahieren
        email_addresses = self.extract_emails(content)
        
        # Benutzernamen extrahieren
        usernames = self.extract_usernames(content)
        
        return {
            'url': url,
            'title': title,
            'description': description,
            'keywords': keywords,
            'content': content,
            'crawl_date': datetime.now().isoformat(),
            'phone_numbers': phone_numbers,
            'email_addresses': email_addresses,
            'usernames': usernames
        }
    
    def extract_phone_numbers(self, text):
        """Extrahiert Telefonnummern aus Text"""
        import re
        # Einfache Regex für Telefonnummern (kann erweitert werden)
        phone_pattern = r'\b(?:\+?49[-.\s]?)?\(?0?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}\b'
        phones = re.findall(phone_pattern, text)
        return list(set(phones))  # Entferne Duplikate
    
    def extract_emails(self, text):
        """Extrahiert E-Mail-Adressen aus Text"""
        import re
        # Einfache Regex für E-Mail-Adressen (kann erweitert werden)
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return list(set(emails))  # Entferne Duplikate
    
    def extract_usernames(self, text):
        """Extrahiert Benutzernamen aus Text"""
        import re
        # Einfache Regex für Benutzernamen (kann erweitert werden)
        username_pattern = r'\b(?:@|user|username)\s*[A-Za-z0-9_]{3,}\b'
        usernames = re.findall(username_pattern, text)
        return list(set(usernames))  # Entferne Duplikate
    
    def save_to_database(self, data):
        """Speichert Daten in die Datenbank"""
        try:
            conn = sqlite3.connect('database/websites.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS websites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,
                    title TEXT,
                    description TEXT,
                    keywords TEXT,
                    content TEXT,
                    crawl_date TEXT,
                    phone_numbers TEXT,
                    email_addresses TEXT,
                    usernames TEXT
                )
            ''')
            
            cursor.execute('''
                INSERT OR REPLACE INTO websites 
                (url, title, description, keywords, content, crawl_date, phone_numbers, email_addresses, usernames)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['url'],
                data['title'],
                data['description'],
                data['keywords'],
                data['content'],
                data['crawl_date'],
                ','.join(data['phone_numbers']),
                ','.join(data['email_addresses']),
                ','.join(data['usernames'])
            ))
            
            conn.commit()
            conn.close()
            
        except sqlite3.Error as e:
            logger.error(f"Fehler beim Speichern in die Datenbank: {e}")
    
    def crawl_url(self, url):
        """Crawlt eine einzelne URL"""
        logger.info(f"Crawle URL: {url}")
        
        html_content = self.fetch_page(url)
        if html_content is None:
            with self.lock:
                self.failed_urls.append(url)
            return None
            
        data = self.extract_data(html_content, url)
        self.save_to_database(data)
        
        with self.lock:
            self.successful_crawls += 1
            logger.info(f"URL erfolgreich gecrawlt: {url} ({self.successful_crawls}/{len(self.urls)})")
        
        return data
    
    def crawl_urls_parallel(self, urls):
        """Crawlt mehrere URLs parallel"""
        self.urls = urls  # Für Fortschrittsanzeige
        self.failed_urls = []
        self.successful_crawls = 0
        
        results = []
        
        # Verwende ThreadPoolExecutor für paralleles Crawling
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submitte alle Tasks
            future_to_url = {executor.submit(self.crawl_url, url): url for url in urls}
            
            # Verarbeite Ergebnisse, sobald sie verfügbar sind
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    if result is not None:
                        results.append(result)
                except Exception as e:
                    logger.error(f"Fehler beim Crawlen von {url}: {e}")
                    with self.lock:
                        self.failed_urls.append(url)
        
        # Zusammenfassung
        logger.info(f"Parallel crawling abgeschlossen. {len(results)} URLs erfolgreich gecrawlt, {len(self.failed_urls)} fehlgeschlagen.")
        
        return results

# Beispiel für die Verwendung
if __name__ == "__main__":
    # Liste von URLs zum Crawlen
    urls = [
        'https://httpbin.org/html',
        'https://httpbin.org/delay/1',
        'https://httpbin.org/delay/2'
    ]
    
    # Erstelle Robust-Proxy-Crawler-Instanz
    crawler = RobustProxyWebCrawler(max_workers=3)
    
    # Crawle URLs parallel
    print(f"Starte paralleles Crawling von {len(urls)} URLs...")
    results = crawler.crawl_urls_parallel(urls)
    
    print(f"Crawling abgeschlossen. {len(results)} URLs bearbeitet.")