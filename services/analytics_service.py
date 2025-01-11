from database.database import DatabaseInterface
from datetime import datetime, timedelta
import pandas as pd

class AnalyticsService:
    def __init__(self, database: DatabaseInterface):
        self.db = database
        self.create_tables()

    def create_tables(self):
        # Create audit logs table
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                event_type TEXT NOT NULL,
                user_id INTEGER,
                details TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Create team members table
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS team_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                permissions TEXT NOT NULL,
                added_by INTEGER NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (added_by) REFERENCES users (id)
            )
        ''')

        self.db.commit()

    def log_event(self, event_type: str, user_id: int, details: str):
        self.db.execute(
            'INSERT INTO audit_logs (event_type, user_id, details) VALUES (?, ?, ?)',
            (event_type, user_id, details)
        )
        self.db.commit()

    def get_verification_stats(self, days: int = 30):
        self.db.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN verdict = 'TRUE' THEN 1 ELSE 0 END) as true_count,
                SUM(CASE WHEN verdict = 'FALSE' THEN 1 ELSE 0 END) as false_count,
                AVG(confidence) as avg_confidence
            FROM verifications
            WHERE created_at >= datetime('now', ?)
        ''', (f'-{days} days',))
        return self.db.fetch_one()

    def get_audit_logs(self, user_id: int = None, event_type: str = None, days: int = 7):
        query = '''
            SELECT l.*, u.email 
            FROM audit_logs l
            JOIN users u ON l.user_id = u.id
            WHERE l.timestamp >= datetime('now', ?)
        '''
        params = [f'-{days} days']
        
        if user_id:
            query += ' AND l.user_id = ?'
            params.append(user_id)
        if event_type:
            query += ' AND l.event_type = ?'
            params.append(event_type)
            
        query += ' ORDER BY l.timestamp DESC'
        
        self.db.execute(query, tuple(params))
        return self.db.fetch_all()

    def add_team_member(self, user_id: int, role: str, permissions: list, added_by: int):
        try:
            self.db.execute(
                'INSERT INTO team_members (user_id, role, permissions, added_by) VALUES (?, ?, ?, ?)',
                (user_id, role, ','.join(permissions), added_by)
            )
            self.db.commit()
            return True
        except Exception:
            return False

    def get_team_members(self):
        self.db.execute('''
            SELECT t.*, u.email, u.first_name, u.last_name
            FROM team_members t
            JOIN users u ON t.user_id = u.id
            ORDER BY t.added_at DESC
        ''')
        return self.db.fetch_all() 