import streamlit as st
from services.user_service import UserService
from services.analytics_service import AnalyticsService
from .components import UIComponents

class AdminPages:
    def __init__(self, user_service: UserService, analytics_service: AnalyticsService):
        self.user_service = user_service
        self.analytics_service = analytics_service
        self.components = UIComponents()

    def show_user_management(self):
        self.components.show_header()
        self.components.show_user_header()
        st.title("👥 User Management")

        # List all users
        users = self.user_service.get_all_users()
        st.subheader("Existing Users")
        
        for user in users:
            with st.expander(f"User: {user[3]} {user[4]} ({user[1]})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Name:** {user[3]} {user[4]}")
                    st.write(f"**Email:** {user[1]}")
                    st.write(f"**Twitter:** {user[5]}")
                    st.write(f"**Admin:** {'Yes' if user[6] else 'No'}")
                
                with col2:
                    if st.button("Promote to Admin", key=f"promote_{user[0]}"):
                        self.user_service.promote_to_admin(user[0])
                        st.success(f"Promoted {user[1]} to admin!")
                        st.rerun()
                    
                    if st.button("Reset Password", key=f"reset_{user[0]}"):
                        new_password = "TempPass123!"  # You might want to generate this
                        self.user_service.reset_password(user[0], new_password)
                        st.success(f"Password reset! Temporary password: {new_password}")
                
                with col3:
                    if st.button("Delete User", key=f"delete_{user[0]}"):
                        if user[1] != "henzardkruger@gmail.com":  # Prevent admin deletion
                            self.user_service.delete_user(user[0])
                            st.success(f"Deleted user {user[1]}")
                            st.rerun()
                        else:
                            st.error("Cannot delete main admin user!")

        # Add new user form
        st.subheader("Add New User")
        with st.form("add_user_form"):
            col1, col2 = st.columns(2)
            with col1:
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                first_name = st.text_input("First Name")
            with col2:
                last_name = st.text_input("Last Name")
                twitter_handle = st.text_input("Twitter Handle")
                is_admin = st.checkbox("Is Admin")
            
            if st.form_submit_button("Add User"):
                if self.user_service.register_user(
                    email, password, first_name, last_name, twitter_handle, is_admin
                ):
                    st.success("User added successfully!")
                    st.rerun()
                else:
                    st.error("Failed to add user. Email might already exist.") 