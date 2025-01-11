import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

class Config:
    # Database
    DB_NAME = st.secrets.get("database", {}).get("DB_NAME") or os.getenv('DB_NAME', 'app.db')
    
    # Admin User
    ADMIN_EMAIL = st.secrets.get("admin", {}).get("ADMIN_EMAIL") or os.getenv('ADMIN_EMAIL', 'admin@example.com')
    ADMIN_PASSWORD = st.secrets.get("admin", {}).get("ADMIN_PASSWORD") or os.getenv('ADMIN_PASSWORD', 'change_this_password')
    
    # Security
    SECRET_KEY = st.secrets.get("security", {}).get("SECRET_KEY") or os.getenv('SECRET_KEY', 'your_secret_key_here')
    
    # OpenAI
    OPENAI_API_KEY = st.secrets.get("openai", {}).get("OPENAI_API_KEY") or os.getenv('OPENAI_API_KEY') 