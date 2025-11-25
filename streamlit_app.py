"""
M&A Transaction Classifier - Main Page
Redirects to Introduction page

Author: Alex Chen
Date: November 25, 2025
"""

import streamlit as st

st.set_page_config(
    page_title="M&A Transaction Classifier",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Redirect message
st.info("👈 Please select **Introduction** or **Demo** from the sidebar to get started!")

st.markdown("### 🔍 M&A Transaction Classifier")
st.markdown("This app provides AI-powered classification of M&A transactions using AWS Lambda and Bedrock Claude.")
