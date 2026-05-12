'''
LOGGER
Provides a standardized function to log security events and alerts into the shared database
'''

import sqlite3
from datetime import datetime

# Standardized logging function for usage across individual monitoring scenarios
def log_event(member_name, source_ip, event_type, severity, raw_data):
    try:
        con = sqlite3.connect('security_logs.db')
        cursor = con.cursor()

        # Generates exact second the event happened for postmortem forensic analysis
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO SecurityEvents (timestamp, memberName, sourceIP, eventType, severity, rawData)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, member_name, source_ip, event_type, severity, raw_data))

        con.commit()
        con.close()

    except Exception as e:
        print(f"Error logging event: {e}")
