import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

# Function to save contributions to a file
def save_contribution(contribution):
    if not os.path.exists('contributions.json'):
        with open('contributions.json', 'w') as f:
            json.dump([], f)
    with open('contributions.json', 'r+') as f:
        data = json.load(f)
        data.append(contribution)
        f.seek(0)
        json.dump(data, f)

# Sidebar for navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Select a page:", ["Home", "About Us", "Contact Us"])

# Title and Introduction
if menu == "Home":
    st.title("🌐 TruthAISwarm: Safeguarding Truth in the Digital Age")
    st.markdown("""
    Welcome to *TruthAISwarm*, a decentralized AI-powered system designed to combat misinformation and ensure transparency. Explore dynamic truth bubbles, contribute to verified knowledge, and join our mission to protect the truth.
    """)

    # Explanation Section
    st.header("📖 What is TruthAISwarm?")
    st.markdown("""
    TruthAISwarm is an innovative platform that leverages AI to verify information and combat misinformation. By contributing verified knowledge, users can help create a more informed society. The platform features:
    - **Truth Bubbles**: Visual representations of verified knowledge.
    - **Contribute Section**: Users can submit facts and insights.
    - **Live Feed**: Real-time updates on verified posts.
    - **User Profile**: Track contributions and rewards.
    - **TruthAI Assistant**: Chat with an AI ambassador for assistance.
    """)

    # How-To Guide
    st.header("🛠️ How to Use TruthAISwarm")
    st.markdown("""
    1. **Explore Truth Bubbles**: View dynamic visualizations of verified knowledge.
    2. **Contribute**: Use the form to submit information you wish to verify.
    3. **Check Live Feed**: Stay updated with real-time information.
    4. **Interact with TruthAI**: Ask questions and get assistance.
    """)

    # Truth Bubble Visualization
    st.header("🌀 Explore Truth Bubbles")
    st.markdown("Dive into verified knowledge represented as dynamic truth bubbles.")

    # Example Data for Truth Bubbles
    data = {
        "Topic": ["Climate Change", "Vaccines", "AI Ethics", "Cryptocurrencies"],
        "Verified Sources": [150, 200, 100, 80],
        "Controversy Level": [4, 3, 5, 2],
    }

    df = pd.DataFrame(data)
    fig = px.scatter(
        df,
        x="Verified Sources",
        y="Controversy Level",
        size="Verified Sources",
        color="Topic",
        hover_name="Topic",
        title="Truth Bubbles",
    )
    st.plotly_chart(fig)

    # Contribute Section
    st.header("🌟 Contribute to the Swarm")
    st.markdown("Submit facts, verify information, or provide insights to earn Swarm Tokens.")

    with st.form("contribute_form"):
        user_input = st.text_area("Enter the information you wish to verify:", help="Please provide clear and concise information.")
        submitted = st.form_submit_button("Submit")
        if submitted:
            save_contribution(user_input)
            st.success("Thank you for your contribution! Your submission has been saved and is under review.")

    # Live Feed (Mockup)
    st.header("🔴 Live Feed")
    st.markdown("Real-time updates from X.com.")
    st.text("🚀 'Post 1234' verified as TRUE by Trust Nodes (95% consensus).")
    st.text("⚠️ 'Post 5678' flagged as DECEPTIVE. Sources: [Link 1, Link 2].")

    # User Profile Section
    st.header("👤 Your Profile")
    st.markdown("Track your contributions and rewards.")
    profile_data = {
        "Metric": ["Contributions", "Verified Posts", "Swarm Tokens"],
        "Value": [12, 8, 240],
    }
    profile_df = pd.DataFrame(profile_data)
    st.table(profile_df)

    # TruthAI Assistant
    st.header("🤖 Meet TruthAI")
    st.markdown("Chat with our humanoid AI ambassador to learn more.")
    if st.button("Chat with TruthAI"):
        st.text("TruthAI: Hello! How can I assist you today?")

# About Us Section
elif menu == "About Us":
    st.title("📚 About Us")
    st.markdown("""
    TruthAISwarm is a project dedicated to restoring trust in information. Our mission is to combat misinformation through a decentralized AI system that verifies facts and promotes transparency. We believe in the power of collective intelligence and the importance of truth in the digital age.
    """)

# Contact Us Section
elif menu == "Contact Us":
    st.title("✉️ Contact Us")
    st.markdown("We would love to hear from you! Please fill out the form below to get in touch.")
    
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")
        submitted = st.form_submit_button("Send")
        if submitted:
            st.success("Thank you for your message! We will get back to you soon.")
