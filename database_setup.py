'''
DATABASE SETUP
Initializes the centralized SQLite3 database and creates the SecurityEvents table
'''

import sqlite3

def initialize_db():
    # Connect to + create security_logs.db file to store logged security events
    con = sqlite3.connect('security_logs.db')
    cursor = con.cursor()

    '''
    Create the SecurityEvents table based on the project proposal schema

    Severity is scored 1-3 where:
        1 is the lowest severity that does not threaten system integrity
        2 is a medium severity and includes network or service-based threats that are contained
        3 is the highest severity and reflects scenarios where isolation is compromised, such as an adversary gaining host access

    '''
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SecurityEvents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            memberName TEXT,
            sourceIP TEXT,
            eventType TEXT,
            severity INTEGER,
            rawData TEXT
        )
    ''')
    
    con.commit()
    con.close()
    print("Database initialized. The SecurityEvents table is now ready.")

if __name__ == "__main__":
    initialize_db()
