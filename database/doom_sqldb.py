import sqlite3
import os
import threading
from datetime import datetime
from contextlib import contextmanager

class DoomSQLDB:
    """Doom SQL-Datenbank für Versionierung und Datenmanagement"""
    
    def __init__(self, db_path='database/doom.db'):
        self.db_path = db_path
        self.lock = threading.Lock()  # Thread-Sicherheit
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Erstellt eine thread-sichere Datenbankverbindung"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Um Spaltennamen als Dictionary zu erhalten
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def init_database(self):
        """Initialisiert die Datenbank und erstellt die Tabellen"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabelle für Versionen
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS versions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    version_number TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    description TEXT,
                    checksum TEXT
                )
            ''')
            
            # Tabelle für Crawling-Status
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS crawl_status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL,
                    status TEXT,
                    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    content_hash TEXT
                )
            ''')
            
            # Tabelle für indizierte Daten
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS indexed_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL,
                    title TEXT,
                    description TEXT,
                    content TEXT,
                    phone_numbers TEXT,
                    emails TEXT,
                    usernames TEXT,
                    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    content_hash TEXT
                )
            ''')
            
            # Tabelle für Backup-Informationen
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS backup_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    backup_name TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    version_number TEXT,
                    file_count INTEGER,
                    total_size INTEGER
                )
            ''')
            
            conn.commit()
    
    def insert_version(self, version_number, description='', checksum=''):
        """Fügt eine neue Version in die Datenbank ein"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO versions (version_number, description, checksum)
                    VALUES (?, ?, ?)
                ''', (version_number, description, checksum))
                conn.commit()
                return True
            except Exception as e:
                print(f"Fehler beim Einfügen der Version: {e}")
                return False
    
    def get_version(self, version_number):
        """Holt eine bestimmte Version aus der Datenbank"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM versions WHERE version_number = ?', (version_number,))
            return cursor.fetchone()
    
    def insert_crawl_status(self, url, status, content_hash=''):
        """Fügt den Crawling-Status einer URL in die Datenbank ein"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO crawl_status (url, status, content_hash)
                    VALUES (?, ?, ?)
                ''', (url, status, content_hash))
                conn.commit()
                return True
            except Exception as e:
                print(f"Fehler beim Einfügen des Crawling-Status: {e}")
                return False
    
    def get_crawl_status(self, url):
        """Holt den Crawling-Status einer URL"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM crawl_status WHERE url = ?', (url,))
            return cursor.fetchone()
    
    def insert_indexed_data(self, url, title, description, content, phone_numbers, emails, usernames):
        """Fügt indizierte Daten in die Datenbank ein"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO indexed_data 
                    (url, title, description, content, phone_numbers, emails, usernames)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (url, title, description, content, phone_numbers, emails, usernames))
                conn.commit()
                return True
            except Exception as e:
                print(f"Fehler beim Einfügen der indizierten Daten: {e}")
                return False
    
    def get_indexed_data(self, url):
        """Holt indizierte Daten für eine URL"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM indexed_data WHERE url = ?', (url,))
            return cursor.fetchone()
    
    def create_backup_info(self, backup_name, version_number, file_count, total_size):
        """Erstellt Backup-Informationen"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO backup_info (backup_name, version_number, file_count, total_size)
                    VALUES (?, ?, ?, ?)
                ''', (backup_name, version_number, file_count, total_size))
                conn.commit()
                return True
            except Exception as e:
                print(f"Fehler beim Erstellen der Backup-Informationen: {e}")
                return False

    def get_all_versions(self):
        """Holt alle Versionen aus der Datenbank"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM versions ORDER BY created_at DESC')
            return cursor.fetchall()

    def get_all_crawl_status(self):
        """Holt alle Crawling-Status aus der Datenbank"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM crawl_status ORDER BY crawled_at DESC')
            return cursor.fetchall()

    def get_all_indexed_data(self):
        """Holt alle indizierten Daten aus der Datenbank"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM indexed_data ORDER BY crawled_at DESC')
            return cursor.fetchall()