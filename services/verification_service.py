from database.database import DatabaseInterface
from datetime import datetime

class VerificationService:
    def __init__(self, database: DatabaseInterface):
        self.db = database
        self.create_table()

    def create_table(self):
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS verifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                statement TEXT NOT NULL,
                verdict TEXT NOT NULL,
                confidence INTEGER NOT NULL,
                explanation TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.db.commit()

    def save_verification(self, user_id: int, statement: str, result: dict) -> bool:
        try:
            self.db.execute('''
                INSERT INTO verifications 
                (user_id, statement, verdict, confidence, explanation) 
                VALUES (?, ?, ?, ?, ?)
            ''', (
                user_id,
                statement,
                result['verdict'],
                result['confidence'],
                result['explanation']
            ))
            self.db.commit()
            return True
        except Exception:
            return False

    def get_user_verifications(self, user_id: int):
        self.db.execute('''
            SELECT * FROM verifications 
            WHERE user_id = ? 
            ORDER BY created_at DESC
        ''', (user_id,))
        return self.db.fetch_all() 