import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
import sqlite3
from datetime import datetime
import logging

# Konfiguration des Loggings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleWebCrawler:
    def __init__(self):
        # Default configuration values
        self.config = {
            'timeout': 10,
            'max_retries': 3,
            'delay_between_requests': 1,
            'max_content_length': 1000000,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.config['user_agent']})
        
    def fetch_page(self, url):
        """Holt eine Seite und gibt den Inhalt zurück"""
        try:
            response = self.session.get(url, timeout=self.config['timeout'])
            response.raise_for_status()
            
            # Prüfen der Content-Length
            if len(response.content) > self.config['max_content_length']:
                logger.warning(f"Seite zu groß: {url}")
                return None
                
            return response.text
            
        except requests.RequestException as e:
            logger.error(f"Fehler beim Abrufen der Seite {url}: {e}")
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
        data = self.extract_data(html_content, url)
        self.save_to_database(data)
        
        # Delay zwischen Anfragen
        time.sleep(self.config['delay_between_requests'])
        
        return data
    
    def crawl_urls(self, urls):
        """Crawlt mehrere URLs"""
        results = []
        for url in urls:
            result = self.crawl_url(url)
            results.append(result)
        return results

# Beispiel für die Verwendung
if __name__ == "__main__":
    # Lade Konfiguration
    config = load_config('config/crawler_config.json')
    
    # Liste von URLs zum Crawlen
    urls = [
        'https://example.com',
        'https://httpbin.org/html'
    ]
    
    # Erstelle Crawler-Instanz
    crawler = SimpleWebCrawler()
    
    # Crawle URLs
    results = crawler.crawl_urls(urls)
    
    print(f"Crawling abgeschlossen. {len(results)} URLs bearbeitet.")