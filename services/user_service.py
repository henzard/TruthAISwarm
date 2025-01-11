from database.database import DatabaseInterface
from models.user import User
from utils.security import SecurityUtils
import streamlit as st
import extra_streamlit_components as stx
import json
from datetime import datetime, timedelta
from utils.logger import Logger

class UserService:
    def __init__(self, database: DatabaseInterface):
        self.db = database
        self.create_table()
        self.ensure_admin_exists()
        self.cookie_manager = self.get_cookie_manager()
        self.logger = Logger.get_logger()
        self.logger.info("UserService initialized")

    @staticmethod
    def get_cookie_manager():
        """Get or create cookie manager instance"""
        logger = Logger.get_logger()
        try:
            if 'cookie_manager' not in st.session_state:
                logger.debug("Creating new cookie manager")
                cookie_manager = stx.CookieManager()
                st.session_state.cookie_manager = cookie_manager
                
                # Initialize the cookie manager in the page
                cookie_manager.get_all()
                logger.debug("Cookie manager initialized with existing cookies")
                
            return st.session_state.cookie_manager
        except Exception as e:
            logger.error(f"Error creating cookie manager: {str(e)}")
            raise

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
        admin_email = 'henzardkruger@gmail.com'.lower()
        self.db.execute('SELECT * FROM users WHERE LOWER(email) = ?', (admin_email,))
        if not self.db.fetch_one():
            hashed_password = SecurityUtils.hash_password("Alicia07")
            self.db.execute(
                '''INSERT INTO users 
                   (email, password, first_name, last_name, twitter_handle, is_admin) 
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (admin_email, hashed_password, 'Admin', 'User', '@admin', 1)
            )
            self.db.commit()

    def register_user(self, email: str, password: str, first_name: str, 
                     last_name: str, twitter_handle: str, is_admin: bool = False) -> bool:
        try:
            # Convert email to lowercase before saving
            email = email.lower()
            
            # Check if email already exists (case insensitive)
            self.db.execute('SELECT * FROM users WHERE LOWER(email) = ?', (email,))
            if self.db.fetch_one():
                return False
            
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
        self.logger.debug(f"Attempting to authenticate user: {email}")
        email = email.lower()
        
        try:
            self.db.execute('SELECT * FROM users WHERE LOWER(email) = ?', (email,))
            user_data = self.db.fetch_one()
            
            if user_data and SecurityUtils.verify_password(password, user_data[2]):
                self.logger.info(f"User authenticated successfully: {email}")
                user = User(
                    id=user_data[0],
                    email=user_data[1],
                    password=user_data[2],
                    first_name=user_data[3],
                    last_name=user_data[4],
                    twitter_handle=user_data[5],
                    is_admin=bool(user_data[6])
                )
                
                # Save user data in cookie (exclude sensitive info)
                user_cookie = {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "twitter_handle": user.twitter_handle,
                    "is_admin": user.is_admin
                }
                
                try:
                    # Set cookie with explicit parameters
                    self.logger.debug("Attempting to set authentication cookie")
                    
                    # Initialize cookie manager
                    self.cookie_manager.get_all()
                    
                    # Set cookie with domain and path
                    self.cookie_manager.set(
                        cookie="user_auth",
                        val=json.dumps(user_cookie),
                        expires_at=datetime.now() + timedelta(days=7),
                        key="user_auth",
                        path="/",
                    )
                    self.logger.info("Authentication cookie set successfully")
                    
                    # Set session state after cookie is set
                    st.session_state.user = user
                    st.session_state.authentication_status = True
                    
                except Exception as e:
                    self.logger.error(f"Failed to set authentication cookie: {str(e)}")
                
                return user
            else:
                self.logger.warning(f"Authentication failed for user: {email}")
                return None
        except Exception as e:
            self.logger.error(f"Error during authentication: {str(e)}")
            return None

    def check_cookie_auth(self):
        """Check if user is authenticated via cookie"""
        self.logger.debug("Checking cookie authentication")
        try:
            if not st.session_state.user:
                self.logger.debug("No user in session, checking cookies")
                user_cookie = self.cookie_manager.get(cookie="user_auth")
                
                if user_cookie:
                    self.logger.debug(f"Found user cookie: {user_cookie}")
                    try:
                        user_data = json.loads(user_cookie)
                        # Verify user still exists in database
                        self.db.execute('SELECT * FROM users WHERE id = ?', (user_data["id"],))
                        db_user = self.db.fetch_one()
                        
                        if db_user:
                            self.logger.info(f"Restoring user session for: {user_data['email']}")
                            user = User(
                                id=user_data["id"],
                                email=user_data["email"],
                                password="",  # Password not stored in cookie
                                first_name=user_data["first_name"],
                                last_name=user_data["last_name"],
                                twitter_handle=user_data["twitter_handle"],
                                is_admin=user_data["is_admin"]
                            )
                            st.session_state.user = user
                            st.session_state.authentication_status = True
                            return True
                        else:
                            self.logger.warning(f"User from cookie not found in database: {user_data['email']}")
                    except Exception as e:
                        self.logger.error(f"Error processing user cookie: {str(e)}")
                        self.cookie_manager.delete(cookie="user_auth")
                else:
                    self.logger.debug("No authentication cookie found")
            return False
        except Exception as e:
            self.logger.error(f"Cookie authentication check failed: {str(e)}")
            return False

    def logout(self):
        """Logout user and clear cookies"""
        try:
            if st.session_state.user:
                self.logger.info(f"Logging out user: {st.session_state.user.email}")
                st.session_state.user = None
                st.session_state.authentication_status = None
                self.cookie_manager.delete(cookie="user_auth", key="user_auth")
                self.logger.debug("User session and cookies cleared")
        except Exception as e:
            self.logger.error(f"Error during logout: {str(e)}")

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