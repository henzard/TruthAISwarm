import hashlib
import os
import bcrypt
from cryptography.fernet import Fernet
from config import Config

class SecurityUtils:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()

    @staticmethod
    def verify_password(password: str, stored_password: str) -> bool:
        """Verify a password against its hash."""
        try:
            return bcrypt.checkpw(password.encode(), stored_password.encode())
        except Exception:
            return False

    @staticmethod
    def generate_secret_key() -> bytes:
        """Generate a secure secret key."""
        return Fernet.generate_key()

    @staticmethod
    def encrypt_data(data: str) -> str:
        """Encrypt sensitive data."""
        f = Fernet(Config.SECRET_KEY.encode())
        return f.encrypt(data.encode()).decode()

    @staticmethod
    def decrypt_data(encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        f = Fernet(Config.SECRET_KEY.encode())
        return f.decrypt(encrypted_data.encode()).decode() 