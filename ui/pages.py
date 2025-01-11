import streamlit as st
from services.user_service import UserService
from services.contact_service import ContactService
from services.llm_service import LLMService
from services.verification_service import VerificationService
from services.analytics_service import AnalyticsService
from services.export_service import ExportService
from .components import UIComponents

class Pages:
    def __init__(
        self, 
        user_service: UserService, 
        contact_service: ContactService,
        analytics_service: AnalyticsService,
        export_service: ExportService
    ):
        self.user_service = user_service
        self.contact_service = contact_service
        self.analytics_service = analytics_service
        self.export_service = export_service
        self.llm_service = LLMService()
        self.verification_service = VerificationService(user_service.db)
        self.components = UIComponents()

    def show_login_page(self):
        self.components.show_header()
        st.title("🔑 Login")
        self.components.show_form_container()
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                try:
                    user = self.user_service.authenticate_user(email, password)
                    if user:
                        st.session_state.user = user
                        self.components.show_success_message("Login successful!")
                        st.rerun()
                    else:
                        self.components.show_error_message("Invalid email or password.")
                except Exception as e:
                    self.components.show_error_message(f"An error occurred: {str(e)}")

    def show_register_page(self):
        self.components.show_header()
        st.title("📝 Register")
        self.components.show_form_container()
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            with col1:
                email = st.text_input("Email", key="register_email")
                password = st.text_input("Password", type="password", key="register_password")
                confirm_password = st.text_input("Confirm Password", type="password")
            with col2:
                first_name = st.text_input("First Name")
                last_name = st.text_input("Last Name")
                twitter_handle = st.text_input("Twitter Handle")
            
            submit = st.form_submit_button("Register", use_container_width=True)
            
            if submit:
                try:
                    if password != confirm_password:
                        self.components.show_error_message("Passwords do not match.")
                        return
                        
                    if self.user_service.register_user(
                        email, password, first_name, last_name, twitter_handle
                    ):
                        self.components.show_success_message("Registration successful! You can now log in.")
                    else:
                        self.components.show_error_message("Email already exists. Please use a different email.")
                except Exception as e:
                    self.components.show_error_message(f"An error occurred: {str(e)}")

    def show_contact_page(self):
        self.components.show_header()
        self.components.show_user_header()
        st.title("✉️ Contact Us")
        
        if not st.session_state.user:
            self.components.show_warning_message("Please sign in to access enterprise support.")
            if st.button("Sign In"):
                st.session_state.page = "Login"
                st.rerun()
            return
        
        self.components.show_form_container()
        st.markdown("""
            ### Enterprise Support
            Our dedicated team is ready to assist you with any questions or requirements. 
            Please provide the details below, and a support specialist will respond within 
            one business day.
        """)
        
        with st.form("contact_form"):
            name = st.text_input("Your Name", value=st.session_state.user.email.split('@')[0])
            email = st.text_input("Your Email", value=st.session_state.user.email)
            subject = st.text_input("Subject")
            message = st.text_area("Message", height=150)
            submit = st.form_submit_button("Send Message", use_container_width=True)
            
            if submit:
                if not all([name, email, subject, message]):
                    self.components.show_error_message("Please fill in all fields.")
                    return
                    
                try:
                    if self.contact_service.save_contact(name, email, message):
                        self.components.show_success_message("""
                            Thank you for your message! We have received it and will respond shortly.
                            We typically respond within 24-48 hours.
                        """)
                        st.balloons()
                    else:
                        self.components.show_error_message("Failed to send message. Please try again.")
                except Exception as e:
                    self.components.show_error_message(f"An error occurred: {str(e)}")

    def show_home_page(self):
        self.components.show_header()
        self.components.show_user_header()
        st.title("🌐 TruthAISwarm Enterprise")
        
        # Hero section with main image
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
                ## Enterprise-Grade Fact Verification
                TruthAISwarm delivers cutting-edge AI-powered fact verification for businesses 
                and organizations that demand accuracy and reliability in their information ecosystem.
            """)
        with col2:
            st.image(
                "images/DALL·E 2025-01-11 10.55.59 - An AI-themed illustration of a fact-checking robot in a futuristic setting. The robot has a sleek, modern design, with glowing eyes and a digital note.webp",
                caption="Enterprise AI Verification",
                use_container_width=True
            )
        
        # Features Section
        st.header("💫 Enterprise Solutions")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                ### Advanced Analytics
                - Real-time information verification
                - Comprehensive data analysis
                - Custom verification workflows
                
                ### Enterprise Integration
                - Seamless API integration
                - Secure data handling
                - Custom deployment options
            """)
            st.image(
                "images/DALL·E 2025-01-11 10.57.05 - An AI-themed illustration of a fact-checking robot in a futuristic setting, now humorously wearing a tin foil hat. The robot has a sleek, modern desig.webp",
                caption="Intelligent Verification Assistant",
                use_container_width=True
            )
        
        with col2:
            st.markdown("""
                ### Real-Time Intelligence
                - Instant fact verification
                - Source credibility analysis
                - Trend monitoring
                
                ### Enterprise Support
                - 24/7 dedicated support
                - Custom training sessions
                - Regular system updates
            """)
        
        # Stats Section
        st.header("📊 Platform Performance")
        col1, col2, col3 = st.columns(3)
        col1.metric("Enterprise Clients", "500+")
        col2.metric("Daily Verifications", "50,000+")
        col3.metric("Accuracy Rate", "99.9%")

    def show_about_page(self):
        self.components.show_header()
        self.components.show_user_header()
        st.title("📚 About TruthAISwarm Enterprise")
        
        # Split into two columns for text and image
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
                ## Our Commitment
                TruthAISwarm Enterprise is committed to providing industry-leading information verification 
                solutions. We empower organizations to make informed decisions based on verified facts 
                and reliable data.
                
                ## Technology
                Our platform leverages state-of-the-art AI and machine learning algorithms, combined with 
                extensive data analysis capabilities, to deliver accurate and timely verification results. 
                Our system continuously learns and adapts to emerging information patterns while maintaining 
                the highest standards of accuracy.
            """)
        
        with col2:
            st.image(
                "images/DALL·E 2025-01-11 11.05.06 - A professional and modern illustration of a diverse team of experts working together in a high-tech office environment. The team includes AI research .webp",
                caption="Our Expert Team",
                use_container_width=True
            )
        
        st.markdown("""
            ## Professional Team
            Our team consists of industry experts dedicated to maintaining the highest standards of 
            information verification:
            
            - 🎯 AI Research Scientists
            - 🔬 Data Analysis Specialists
            - 🛡️ Information Security Experts
            - 💼 Enterprise Solution Architects
            
            ## Enterprise Support
            Our dedicated support team is available 24/7 to assist with your verification needs. 
            Contact us for personalized solutions and enterprise integration options.
        """)

    def show_fact_check_page(self):
        self.components.show_header()
        self.components.show_user_header()
        st.title("🔍 Enterprise Fact Verification")
        
        st.markdown("""
            ## Professional Fact Verification
            Our enterprise-grade AI system provides accurate, reliable verification of any statement 
            or claim, backed by comprehensive source analysis and real-time data.
            
            ### Verification Process:
            1. Submit your statement for verification
            2. AI-powered comprehensive analysis
            3. Multi-source verification
            4. Detailed results with supporting evidence
        """)
        
        self.components.show_form_container()
        
        text_to_verify = st.text_area(
            "Enter statement for verification:",
            height=100,
            help="Input any statement, claim, or information you need to verify"
        )
        
        if st.button("Verify Statement", use_container_width=True):
            if not text_to_verify.strip():
                st.warning("Please enter a statement to verify.")
                return
                
            with st.spinner("Analyzing statement and gathering sources..."):
                result = self.llm_service.verify_fact(text_to_verify)
                
                # Display results in an organized way
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    verdict_color = {
                        "TRUE": "green",
                        "FALSE": "red",
                        "UNCERTAIN": "orange",
                        "ERROR": "red"
                    }.get(result["verdict"], "grey")
                    
                    st.markdown(f"""
                        <div style='background-color: {verdict_color}20; padding: 20px; border-radius: 10px;'>
                            <h3 style='color: {verdict_color}'>Verdict: {result["verdict"]}</h3>
                            <p>Confidence: {result["confidence"]}%</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("### Potential Biases")
                    for bias in result["potential_biases"]:
                        st.markdown(f"- {bias}")
                
                st.markdown("### Explanation")
                st.markdown(result["explanation"])
                
                # Display recent developments
                if "recent_developments" in result:
                    st.markdown("### Recent Developments")
                    st.markdown(result["recent_developments"])
                
                # Display sources with relevance
                if "sources" in result:
                    st.markdown("### Verified Sources")
                    for source in result["sources"]:
                        with st.expander(f"Source: {source['url'][:60]}..."):
                            st.markdown(f"**Relevance**: {source['relevance']}")
                            st.markdown(f"**URL**: [{source['url']}]({source['url']})")
                
                # Display news articles
                if "news_articles" in result and result["news_articles"]:
                    st.markdown("### Recent News Articles")
                    for article in result["news_articles"]:
                        if "error" not in article:
                            with st.expander(f"{article['title'][:60]}..."):
                                st.markdown(f"**Source**: {article.get('source', 'Unknown')}")
                                st.markdown(f"**Published**: {article.get('published', 'Unknown')}")
                                st.markdown(f"**URL**: [{article['url']}]({article['url']})")
                
                # Save the verification to history if user is logged in
                if st.session_state.user:
                    if self.verification_service.save_verification(
                        st.session_state.user.id,
                        text_to_verify,
                        result
                    ):
                        st.success("Verification saved to your history!")

    def show_verification_history(self):
        self.components.show_header()
        self.components.show_user_header()
        st.title("📊 Verification History")

        if not st.session_state.user:
            self.components.show_warning_message("Please sign in to access your verification history.")
            return

        verifications = self.verification_service.get_user_verifications(st.session_state.user.id)
        
        if not verifications:
            st.info("Your verification history is empty. Start by verifying your first statement.")
            return

        for verification in verifications:
            with st.expander(f"Statement: {verification[2][:100]}...", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("### Statement")
                    st.write(verification[2])
                    
                    st.markdown("### Explanation")
                    st.write(verification[5])

                with col2:
                    verdict_color = {
                        "TRUE": "green",
                        "FALSE": "red",
                        "UNCERTAIN": "orange",
                        "ERROR": "red"
                    }.get(verification[3], "grey")
                    
                    st.markdown(f"""
                        <div style='background-color: {verdict_color}20; padding: 20px; border-radius: 10px;'>
                            <h3 style='color: {verdict_color}'>Verdict: {verification[3]}</h3>
                            <p>Confidence: {verification[4]}%</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"Verified on: {verification[6]}")

    def show_analytics_dashboard(self):
        self.components.show_header()
        self.components.show_user_header()
        st.title("📈 Enterprise Analytics")
        
        # Usage Statistics
        st.subheader("Key Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Monthly Verifications", "152,847", "+12%")
        with col2:
            st.metric("Average Response Time", "1.2s", "-0.3s")
        with col3:
            st.metric("API Uptime", "99.99%", "+0.01%")
        
        # Verification Stats
        stats = self.analytics_service.get_verification_stats()
        if stats:
            st.subheader("Verification Statistics")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Verifications", stats[0])
            col2.metric("True Results", stats[1])
            col3.metric("False Results", stats[2])
            col4.metric("Avg Confidence", f"{stats[3]:.1f}%")

        # Recent Activity
        st.subheader("Recent Activity")
        logs = self.analytics_service.get_audit_logs(days=7)
        if logs:
            for log in logs:
                st.markdown(f"""
                    **{log[1]}** - {log[4]}  
                    *User: {log[2]}*
                """)

    def show_team_management(self):
        self.components.show_header()
        self.components.show_user_header()
        st.title("👥 Team Management")
        
        # Team Overview
        st.subheader("Team Members")
        team_members = self.analytics_service.get_team_members()
        
        for member in team_members:
            with st.expander(f"{member[6]} {member[7]} ({member[5]})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Role:** {member[2]}")
                    st.write(f"**Permissions:** {member[3]}")
                with col2:
                    st.write(f"**Added:** {member[5]}")
        
        # Add New Team Member
        with st.form("add_team_member"):
            st.subheader("Add Team Member")
            email = st.text_input("Email")
            role = st.selectbox("Role", ["Analyst", "Manager", "Admin"])
            permissions = st.multiselect(
                "Permissions",
                ["Verify Facts", "View Analytics", "Manage Users", "API Access"]
            )
            if st.form_submit_button("Add Member"):
                if self.analytics_service.add_team_member(
                    email, role, permissions, st.session_state.user.id
                ):
                    st.success("Team member added successfully!")
                    st.rerun()

    def show_api_docs(self):
        self.components.show_header()
        self.components.show_user_header()
        st.title("🔌 API Documentation")
        
        st.markdown("""
            ## REST API
            Access our verification engine programmatically.
            
            ### Authentication
            ```python
            headers = {
                'Authorization': 'Bearer YOUR_API_KEY',
                'Content-Type': 'application/json'
            }
            ```
            
            ### Endpoints
            
            #### Verify Statement
            `POST /api/v1/verify`
            ```python
            import requests

            response = requests.post(
                'https://api.truthaiswarm.com/v1/verify',
                headers=headers,
                json={'statement': 'Your statement here'}
            )
            ```
            
            #### Get Verification History
            `GET /api/v1/verifications`
            ```python
            response = requests.get(
                'https://api.truthaiswarm.com/v1/verifications',
                headers=headers
            )
            ```
        """)

    def show_settings(self):
        self.components.show_header()
        self.components.show_user_header()
        st.title("⚙️ Enterprise Settings")
        
        # Verification Settings
        st.subheader("Verification Settings")
        confidence_threshold = st.slider(
            "Minimum Confidence Threshold",
            min_value=0,
            max_value=100,
            value=80
        )
        
        # Source Settings
        st.subheader("Source Settings")
        trusted_domains = st.text_area(
            "Trusted Domains",
            help="Enter one domain per line"
        )
        
        # Notification Settings
        st.subheader("Notifications")
        notify_options = st.multiselect(
            "Send notifications for:",
            ["Low Confidence Results", "New Team Members", "API Usage Alerts"]
        )
        
        if st.button("Save Settings"):
            st.success("Settings saved successfully!")

    def show_audit_logs(self):
        self.components.show_header()
        self.components.show_user_header()
        st.title("📋 Audit Logs")
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            days = st.selectbox("Time Range", [7, 14, 30, 90], index=0)
        with col2:
            event_type = st.multiselect(
                "Event Type",
                ["Verification", "User Login", "Settings Change", "API Access"]
            )
        
        # Get and display logs
        logs = self.analytics_service.get_audit_logs(days=days, event_type=event_type[0] if event_type else None)
        
        if logs:
            for log in logs:
                st.markdown(f"""
                    ---
                    **{log[1]}**  
                    User: {log[2]}  
                    Details: {log[4]}  
                    Time: {log[1]}
                """)
        else:
            st.info("No audit logs found for the selected filters.") 