import sqlite3
from datetime import datetime

def init_database():
    """Initialisiert die Datenbank und erstellt die Tabellen"""
    try:
        conn = sqlite3.connect('database/websites.db')
        cursor = conn.cursor()
        
        # Tabelle erstellen
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
        
        # Indizes erstellen für bessere Abfragegeschwindigkeit
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_url ON websites(url)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_crawl_date ON websites(crawl_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_phone_numbers ON websites(phone_numbers)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_email_addresses ON websites(email_addresses)')
        
        conn.commit()
        conn.close()
        
        print("Datenbank erfolgreich initialisiert.")
        
    except sqlite3.Error as e:
        print(f"Fehler bei der Datenbankinitialisierung: {e}")

if __name__ == "__main__":
    init_database()