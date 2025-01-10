import streamlit as st
import pandas as pd
import plotly.express as px

# Title and Introduction
st.title("🌐 TruthAISwarm: Safeguarding Truth in the Digital Age")
st.markdown("""
Welcome to *TruthAISwarm*, a decentralized AI-powered system designed to combat misinformation and ensure transparency. Explore dynamic truth bubbles, contribute to verified knowledge, and join our mission to protect the truth.
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
    user_input = st.text_area("Enter the information you wish to verify:")
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.success("Thank you for your contribution! Your submission is under review.")

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
