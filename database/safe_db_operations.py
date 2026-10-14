import sqlite3
import threading
import time
from datetime import datetime
from contextlib import contextmanager
from database.doom_sqldb import DoomSQLDB

class SafeDBOperations:
    """Sichere Datenbankoperationen mit Backup-Schutz"""
    
    def __init__(self, db_path='database/doom.db'):
        self.db = DoomSQLDB(db_path)
        self.backup_in_progress = False
        self.backup_lock = threading.Lock()
        self.operation_lock = threading.Lock()
    
    def acquire_backup_lock(self):
        """Acquire the backup lock to prevent backups during operations"""
        with self.backup_lock:
            if self.backup_in_progress:
                raise Exception("Backup läuft bereits - Operation abgebrochen")
            self.backup_in_progress = True
            return True
    
    def release_backup_lock(self):
        """Release the backup lock"""
        with self.backup_lock:
            self.backup_in_progress = False
    
    @contextmanager
    def safe_operation(self, operation_name="Operation"):
        """Sichere Operation mit Backup-Schutz"""
        try:
            # Acquire backup lock
            self.acquire_backup_lock()
            print(f"Starte sichere {operation_name}...")
            
            yield self.db
            
        except Exception as e:
            print(f"Fehler bei {operation_name}: {e}")
            raise
        finally:
            # Release backup lock
            self.release_backup_lock()
            print(f"{operation_name} abgeschlossen")
    
    def safe_crawl_and_save(self, url, data, version_id):
        """Sicheres Crawlen und Speichern mit Backup-Schutz"""
        with self.safe_operation("Crawling und Speichern") as db:
            try:
                # Setze Crawling-Status
                db.set_crawl_status(url, "processing", version_id)
                
                # Speichere indizierte Daten
                db.save_indexed_data(
                    url=url,
                    title=data.get('title', ''),
                    description=data.get('description', ''),
                    keywords=data.get('keywords', ''),
                    content=data.get('content', ''),
                    phone_numbers=data.get('phone_numbers', []),
                    email_addresses=data.get('email_addresses', []),
                    usernames=data.get('usernames', []),
                    version_id=version_id
                )
                
                # Setze Crawling-Status auf abgeschlossen
                db.set_crawl_status(url, "completed", version_id)
                
                return True
                
            except Exception as e:
                print(f"Fehler beim sicheren Speichern von {url}: {e}")
                db.set_crawl_status(url, "failed", version_id)
                raise
    
    def safe_create_version(self, version_number, description='', checksum=''):
        """Sicheres Erstellen einer neuen Version"""
        with self.safe_operation("Version erstellen") as db:
            return db.create_version(version_number, description, checksum)
    
    def get_all_indexed_data(self):
        """Holt alle indizierten Daten"""
        with self.safe_operation("Daten abrufen") as db:
            return db.get_all_indexed_data()
    
    def get_indexed_data(self, url):
        """Holt indizierte Daten für eine bestimmte URL"""
        with self.safe_operation("Daten abrufen") as db:
            return db.get_indexed_data(url)