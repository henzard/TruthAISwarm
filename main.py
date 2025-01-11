import streamlit as st
from database.database import SQLiteDatabase
from services.user_service import UserService
from services.contact_service import ContactService
from ui.pages import Pages
from config import Config
from ui.admin import AdminPages
from services.analytics_service import AnalyticsService
from services.export_service import ExportService

def initialize_session_state():
    """Initialize session state variables."""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'authentication_status' not in st.session_state:
        st.session_state.authentication_status = None
    if 'page' not in st.session_state:
        st.session_state.page = "Home"

def main():
    # Initialize session state
    initialize_session_state()
    
    # Initialize services
    db = SQLiteDatabase(Config.DB_NAME)
    db.connect()

    try:
        user_service = UserService(db)
        
        # Initialize cookie manager and check authentication
        if not st.session_state.user:
            # Get cookie manager instance (this will initialize it if needed)
            cookie_manager = user_service.get_cookie_manager()
            # Check for cookie authentication
            user_service.check_cookie_auth()
        
        contact_service = ContactService(db)
        analytics_service = AnalyticsService(db)
        export_service = ExportService()
        
        pages = Pages(
            user_service, 
            contact_service, 
            analytics_service,
            export_service
        )
        admin_pages = AdminPages(user_service, analytics_service)

        # Sidebar navigation
        st.sidebar.title("Navigation")
        
        # Show logout button if user is logged in
        if st.session_state.user:
            st.sidebar.markdown(f"Welcome, {st.session_state.user.full_name}!")
            if st.session_state.user.is_admin:
                menu = st.sidebar.radio(
                    "Select a page:", 
                    [
                        "Home", "Fact Checker", "My Verifications",
                        "Analytics Dashboard", "Team Management",
                        "API Documentation", "Settings", "Audit Logs",
                        "About Us", "Contact Us", "User Management"
                    ]
                )
            else:
                menu = st.sidebar.radio(
                    "Select a page:", 
                    ["Home", "Fact Checker", "My Verifications", "About Us", "Contact Us"]
                )
            if st.sidebar.button("Logout"):
                user_service.logout()
                st.rerun()
        else:
            menu = st.sidebar.radio(
                "Select a page:", 
                ["Home", "About Us", "Login", "Register"]
            )

        # Route to appropriate page
        if menu == "Home":
            pages.show_home_page()
        elif menu == "About Us":
            pages.show_about_page()
        elif menu == "Login":
            pages.show_login_page()
        elif menu == "Register":
            pages.show_register_page()
        elif menu == "Contact Us":
            pages.show_contact_page()
        elif menu == "User Management" and st.session_state.user and st.session_state.user.is_admin:
            admin_pages.show_user_management()
        elif menu == "Fact Checker":
            pages.show_fact_check_page()
        elif menu == "My Verifications":
            pages.show_verification_history()
        elif menu == "Analytics Dashboard":
            pages.show_analytics_dashboard()
        elif menu == "Team Management":
            pages.show_team_management()
        elif menu == "API Documentation":
            pages.show_api_docs()
        elif menu == "Settings":
            pages.show_settings()
        elif menu == "Audit Logs":
            pages.show_audit_logs()

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
