from database.database import DatabaseInterface
from models.user import User
from utils.security import SecurityUtils
import streamlit as st

class UserService:
    def __init__(self, database: DatabaseInterface):
        self.db = database
        self.create_table()
        self.ensure_admin_exists()

    def create_table(self):
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                twitter_handle TEXT,
                is_admin INTEGER NOT NULL
            )
        ''')
        self.db.commit()

    def ensure_admin_exists(self):
        """Ensure admin user exists"""
        self.db.execute('SELECT * FROM users WHERE email = ?', ('henzardkruger@gmail.com',))
        if not self.db.fetch_one():
            hashed_password = SecurityUtils.hash_password("Alicia07")
            self.db.execute(
                '''INSERT INTO users 
                   (email, password, first_name, last_name, twitter_handle, is_admin) 
                   VALUES (?, ?, ?, ?, ?, ?)''',
                ('henzardkruger@gmail.com', hashed_password, 'Admin', 'User', '@admin', 1)
            )
            self.db.commit()

    def register_user(self, email: str, password: str, first_name: str, 
                     last_name: str, twitter_handle: str, is_admin: bool = False) -> bool:
        try:
            hashed_password = SecurityUtils.hash_password(password)
            self.db.execute(
                '''INSERT INTO users 
                   (email, password, first_name, last_name, twitter_handle, is_admin) 
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (email, hashed_password, first_name, last_name, twitter_handle, int(is_admin))
            )
            self.db.commit()
            return True
        except Exception:
            return False

    def authenticate_user(self, email: str, password: str) -> User:
        self.db.execute('SELECT * FROM users WHERE email = ?', (email,))
        user_data = self.db.fetch_one()
        if user_data and SecurityUtils.verify_password(password, user_data[2]):
            user = User(
                id=user_data[0],
                email=user_data[1],
                password=user_data[2],
                first_name=user_data[3],
                last_name=user_data[4],
                twitter_handle=user_data[5],
                is_admin=bool(user_data[6])
            )
            st.session_state.user = user
            st.session_state.authentication_status = True
            return user
        return None

    def get_all_users(self):
        self.db.execute('SELECT * FROM users')
        return self.db.fetch_all()

    def update_user(self, user_id: int, email: str, first_name: str, 
                   last_name: str, twitter_handle: str, is_admin: bool):
        self.db.execute(
            '''UPDATE users 
               SET email=?, first_name=?, last_name=?, twitter_handle=?, is_admin=? 
               WHERE id=?''',
            (email, first_name, last_name, twitter_handle, int(is_admin), user_id)
        )
        self.db.commit()

    def delete_user(self, user_id: int):
        self.db.execute('DELETE FROM users WHERE id = ?', (user_id,))
        self.db.commit()

    def reset_password(self, user_id: int, new_password: str):
        hashed_password = SecurityUtils.hash_password(new_password)
        self.db.execute(
            'UPDATE users SET password = ? WHERE id = ?',
            (hashed_password, user_id)
        )
        self.db.commit()

    def promote_to_admin(self, user_id: int):
        self.db.execute(
            'UPDATE users SET is_admin = 1 WHERE id = ?',
            (user_id,)
        )
        self.db.commit() 