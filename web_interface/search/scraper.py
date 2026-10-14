#!/usr/bin/env python3
"""
Web scraper for Doom-related content using BeautifulSoup and Scrapy
"""

import requests
from bs4 import BeautifulSoup
import scrapy
from elasticsearch import Elasticsearch
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, DATETIME, STORED
from whoosh.qparser import QueryParser
import json
import time
from datetime import datetime

class DoomContentScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Doom-Search-Engine/1.0'
        })
        
        # Initialize Elasticsearch client
        try:
            self.es = Elasticsearch(['localhost:9200'])
        except Exception as e:
            print(f"Warning: Elasticsearch not available: {e}")
            self.es = None
            
        # Setup Whoosh index
        self.setup_whoosh_index()
    
    def setup_whoosh_index(self):
        """Setup local search index with Whoosh"""
        schema = Schema(
            title=TEXT(stored=True),
            url=ID(stored=True),
            content=TEXT(stored=True),
            timestamp=DATETIME(stored=True)
        )
        
        try:
            # Try to open existing index
            self.ix = open_dir("doom_index")
        except:
            # Create new index if it doesn't exist
            import os
            if not os.path.exists("doom_index"):
                os.mkdir("doom_index")
            self.ix = create_in("doom_index", schema)
    
    def scrape_doom_wiki(self):
        """Scrape Doom Wiki content"""
        try:
            url = "https://doomwiki.org/wiki/Main_Page"
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract main content
            content = {
                'title': soup.title.string if soup.title else 'Doom Wiki',
                'url': url,
                'content': '',
                'timestamp': datetime.now()
            }
            
            # Get article text
            article = soup.find('div', {'id': 'mw-content-text'})
            if article:
                content['content'] = article.get_text()[:1000]  # First 1000 chars
                
            return content
            
        except Exception as e:
            print(f"Error scraping Doom Wiki: {e}")
            return None
    
    def scrape_doom_forum(self):
        """Scrape Doom community forums"""
        try:
            # Example forum URL - adjust as needed
            url = "https://www.doomworld.com/forum/"
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            content = {
                'title': soup.title.string if soup.title else 'Doom Forum',
                'url': url,
                'content': '',
                'timestamp': datetime.now()
            }
            
            # Extract forum posts or main content
            posts = soup.find_all('div', class_='post')
            if posts:
                content['content'] = ' '.join([post.get_text() for post in posts[:5]])[:1000]
                
            return content
            
        except Exception as e:
            print(f"Error scraping Doom Forum: {e}")
            return None
    
    def index_content(self, content):
        """Index content using Whoosh"""
        if not content:
            return
            
        writer = self.ix.writer()
        writer.add_document(
            title=content['title'],
            url=content['url'],
            content=content['content'],
            timestamp=content['timestamp']
        )
        writer.commit()
        
        # Also index to Elasticsearch if available
        if self.es:
            try:
                self.es.index(
                    index="doom_content",
                    document={
                        'title': content['title'],
                        'url': content['url'],
                        'content': content['content'],
                        'timestamp': content['timestamp']
                    }
                )
            except Exception as e:
                print(f"Error indexing to Elasticsearch: {e}")
    
    def search_index(self, query):
        """Search indexed content"""
        results = []
        
        # Search with Whoosh
        with self.ix.searcher() as searcher:
            parser = QueryParser("content", self.ix.schema)
            myquery = parser.parse(query)
            results = searcher.search(myquery, limit=10)
            
            return [{
                'title': hit['title'],
                'url': hit['url'],
                'content': hit['content'][:200] + '...',
                'score': hit.score
            } for hit in results]
    
    def crawl_doom_sites(self):
        """Crawl multiple Doom-related sites"""
        urls = [
            "https://doomwiki.org/wiki/Main_Page",
            "https://www.doomworld.com/",
            "https://www.gamersgate.com/category/103/doom"
        ]
        
        for url in urls:
            try:
                print(f"Scraping: {url}")
                response = self.session.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                content = {
                    'title': soup.title.string if soup.title else 'Unknown',
                    'url': url,
                    'content': soup.get_text()[:1000],
                    'timestamp': datetime.now()
                }
                
                self.index_content(content)
                time.sleep(1)  # Be respectful to servers
                
            except Exception as e:
                print(f"Error scraping {url}: {e}")
                continue

# Example usage
if __name__ == "__main__":
    scraper = DoomContentScraper()
    
    # Scrape some content
    wiki_content = scraper.scrape_doom_wiki()
    if wiki_content:
        scraper.index_content(wiki_content)
        print("Indexed Doom Wiki content")
    
    # Search example
    results = scraper.search_index("Doom weapon")
    print(f"Search results: {len(results)} found")
    
    for result in results[:3]:
        print(f"- {result['title']}: {result['content']}")