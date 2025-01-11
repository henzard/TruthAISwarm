import streamlit as st

class UIComponents:
    @staticmethod
    def show_header():
        theme = """
            <style>
                .main {
                    padding: 20px;
                    border-radius: 5px;
                }

                .btn {
                    padding: 10px 20px;
                    border-radius: 5px;
                    cursor: pointer;
                    margin: 10px 0;
                }

                .user-info {
                    padding: 10px;
                    border-radius: 5px;
                    margin: 10px 0;
                }

                .form-container {
                    padding: 20px;
                    border-radius: 10px;
                    margin: 10px 0;
                }
            </style>
        """
        st.markdown(theme, unsafe_allow_html=True)

    @staticmethod
    def show_user_header():
        if st.session_state.user:
            st.markdown("""
                <div class="user-info">
                    👤 Logged in as: {st.session_state.user.email}
                </div>
            """, unsafe_allow_html=True)

    @staticmethod
    def show_success_message(message: str):
        st.success(message)

    @staticmethod
    def show_error_message(message: str):
        st.error(message)

    @staticmethod
    def show_warning_message(message: str):
        st.warning(message)

    @staticmethod
    def show_info_message(message: str):
        st.info(message)

    @staticmethod
    def show_form_container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True) 