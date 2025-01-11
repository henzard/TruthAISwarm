from database.database import DatabaseInterface

class ContactService:
    def __init__(self, database: DatabaseInterface):
        self.db = database
        self.create_table()

    def create_table(self):
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.db.commit()

    def save_contact(self, name: str, email: str, subject: str, message: str) -> bool:
        try:
            self.db.execute(
                'INSERT INTO contacts (name, email, subject, message) VALUES (?, ?, ?, ?)',
                (name, email, subject, message)
            )
            self.db.commit()
            return True
        except Exception:
            return False 