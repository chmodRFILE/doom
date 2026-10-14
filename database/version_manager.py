import sqlite3
import hashlib
import os
from datetime import datetime
from database.doom_sqldb import DoomSQLDB

class VersionManager:
    """Verwaltung von Datenbankversionen"""
    
    def __init__(self, db_path='database/doom.db'):
        self.db = DoomSQLDB(db_path)
    
    def create_new_version(self, description='', checksum=''):
        """Erstellt eine neue Version mit automatisch generierter Versionsnummer"""
        # Hole die höchste bisherige Versionsnummer
        latest_version = self.db.get_latest_version()
        
        if latest_version:
            # Erhöhe die Versionsnummer um 1 (z.B. 1.0.0 -> 1.0.1)
            version_parts = latest_version['version_number'].split('.')
            if len(version_parts) >= 3:
                patch = int(version_parts[2]) + 1
                new_version = f"{version_parts[0]}.{version_parts[1]}.{patch}"
            else:
                new_version = "1.0.1"
        else:
            # Erste Version
            new_version = "1.0.0"
        
        # Erstelle die neue Version
        version_id = self.db.create_version(new_version, description, checksum)
        return new_version
    
    def list_all_versions(self):
        """Listet alle Versionen auf"""
        return self.db.get_all_versions()
    
    def get_version_info(self, version_number):
        """Holt Informationen über eine bestimmte Version"""
        return self.db.get_version_info(version_number)
    
    def search_data_by_keyword(self, keyword):
        """Sucht in den indizierten Daten nach einem Schlüsselwort"""
        return self.db.search_indexed_data(keyword)
    
    def search_data_by_url_pattern(self, pattern):
        """Sucht in den URLs nach einem Muster"""
        return self.db.search_urls(pattern)
    
    def get_version_statistics(self):
        """Holt Statistiken für alle Versionen"""
        versions = self.list_all_versions()
        stats = []
        
        for version in versions:
            # Hole die Anzahl der indizierten Daten für diese Version
            count = self.db.get_count_for_version(version['version_number'])
            stats.append({
                'version': version['version_number'],
                'created_at': version['created_at'],
                'description': version['description'],
                'count': count
            })
        
        return stats