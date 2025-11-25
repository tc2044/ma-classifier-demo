"""
Streamlit Cloud Frontend for M&A Classifier
Connects to AWS Lambda/Bedrock Backend via API Gateway

Author: Alex Chen
Date: November 25, 2025
"""

import streamlit as st
import requests
import json
import base64
from typing import Dict, Optional

# ============================================================
# CONFIGURATION
# ============================================================

# API endpoint - will be set via Streamlit secrets in production
API_ENDPOINT = st.secrets.get("API_ENDPOINT", "https://b6svh4pxaw2nr5pr3ndcbnhche0pbtcl.lambda-url.us-east-1.on.aws/")

# ============================================================
# SAMPLE ANNOUNCEMENTS
# ============================================================

SAMPLE_ANNOUNCEMENTS = [
    {
        "title": "KKR Acquisition - Large PE Deal",
        "text": """KKR & Co. Inc. announces the acquisition of 80% stake in ABC Technology Ltd 
        for a total consideration of USD 200 million. The transaction represents a strategic 
        investment in the Southeast Asian technology sector. Goldman Sachs is acting as 
        financial adviser to KKR. The acquisition is expected to complete in Q1 2026."""
    },
    {
        "title": "Company XYZ - Quarterly Results (Should Reject)",
        "text": """Company XYZ Limited announces its unaudited financial results for Q3 2025. 
        Revenue increased 15% year-over-year to $50 million. Net profit was $8 million, 
        up from $6 million in the prior year quarter. The Board is pleased with the results."""
    },
    {
        "title": "Property Sale Announcement (Should Reject)",
        "text": """ABC Corporation announces the disposal of its commercial property located at 
        123 Main Street for a consideration of $12 million. The property sale is part of 
        the company's asset optimization strategy."""
    },
    {
        "title": "Strategic Investment - Mid-Size Deal",
        "text": """DEF Ltd announces a proposed strategic investment to acquire 65% of the issued 
        share capital of XYZ Pte Ltd for SGD 85 million in cash. The acquisition will expand 
        DEF's presence in the Asian market. HSBC is advising on the transaction."""
    },
    {
        "title": "Small Deal - Below Threshold (Should Reject)",
        "text": """Startup Inc. announces the acquisition of Tech Co. for a total consideration 
        of USD 3 million. The acquisition will strengthen Startup's product capabilities."""
    }
]

# ============================================================
# API FUNCTIONS
# ============================================================

def classify_text(title: str, text: str) -> Optional[Dict]:
    """Call Lambda backend to classify announcement text"""
    try:
        response = requests.post(
            API_ENDPOINT,
            json={
                "title": title,
                "text": text
            },
            headers={
                "Content-Type": "application/json"
            },
            timeout=35  # Lambda timeout is 30s
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            st.error(response.text)
            return None
            
    except requests.exceptions.Timeout:
        st.error("Request timed out. The document may be too complex.")
        return None
    except Exception as e:
        st.error(f"API call failed: {str(e)}")
        return None


def classify_pdf(title: str, pdf_file) -> Optional[Dict]:
    """Call Lambda backend to classify PDF file"""
    try:
        # Read PDF and encode to base64
        pdf_bytes = pdf_file.read()
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        
        # Reset file pointer for potential re-use
        pdf_file.seek(0)
        
        response = requests.post(
            API_ENDPOINT,
            json={
                "title": title,
                "pdf_base64": pdf_base64
            },
            headers={
                "Content-Type": "application/json"
            },
            timeout=35
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            st.error(response.text)
            return None
            
    except requests.exceptions.Timeout:
        st.error("Request timed out. The PDF may be too large or complex.")
        return None
    except Exception as e:
        st.error(f"PDF processing failed: {str(e)}")
        return None


# ============================================================
# UI COMPONENTS
# ============================================================

def render_result(result: Dict):
    """Render classification result"""
    
    if result.get("qualified"):
        st.success("✅ **M&A Transaction Detected**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            confidence = result.get("confidence", 0)
            st.metric("Confidence", f"{confidence:.0%}")
        
        with col2:
            theme = result.get("theme", "N/A")
            st.metric("Transaction Type", theme)
        
        # Show reasoning if available
        reasoning = result.get("reasoning")
        if reasoning:
            st.info(f"**Analysis**: {reasoning}")
        
        # Show processing stage
        stage = result.get("stage", "unknown")
        bedrock_called = result.get("bedrock_called", False)
        
        if bedrock_called:
            st.caption(f"🤖 AWS Bedrock Claude used (Stage: {stage})")
        else:
            st.caption(f"⚡ Pre-filter/Rule-based classification (Stage: {stage})")
    
    else:
        st.warning("❌ **Not an M&A Transaction**")
        
        reason = result.get("reason", "Does not meet M&A criteria")
        st.info(f"**Reason**: {reason}")
        
        filter_name = result.get("filter")
        if filter_name:
            st.caption(f"🔍 Filtered by: {filter_name}")
        
        stage = result.get("stage", "unknown")
        st.caption(f"Processing stage: {stage}")


# ============================================================
# MAIN APP
# ============================================================

def main():
    st.set_page_config(
        page_title="M&A Transaction Classifier",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 M&A Transaction Classifier")
    st.markdown("**Powered by AWS Lambda + Bedrock Claude**")
    
    st.markdown("---")
    
    # Sidebar - Information
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This tool classifies corporate announcements as M&A transactions or not.
        
        **Processing Flow**:
        1. Pre-filters (60-70% rejected)
        2. Feature extraction
        3. Rule-based decisions
        4. AI fallback (Bedrock Claude)
        
        **Qualifies as M&A**:
        - Acquisitions, mergers, takeovers
        - Strategic investments >$5M
        - Change of control transactions
        - Joint ventures
        
        **Does NOT qualify**:
        - Financial results
        - Property transactions
        - Debt issuance
        - Small deals (<$5M)
        - Procedural updates
        """)
        
        st.markdown("---")
        st.caption("Backend: AWS Lambda + Bedrock")
        st.caption("Response time: 0.5-3 seconds")
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📝 Text Input", "📄 PDF Upload", "📚 Try Samples"])
    
    # Tab 1: Text Input
    with tab1:
        st.subheader("Enter Announcement Text")
        
        title_text = st.text_input(
            "Announcement Title",
            placeholder="e.g., ABC Corp - Proposed Acquisition of XYZ Ltd"
        )
        
        text_input = st.text_area(
            "Announcement Text",
            height=300,
            placeholder="Paste the full announcement text here..."
        )
        
        if st.button("🔍 Classify Text", type="primary", key="classify_text"):
            if not title_text or not text_input:
                st.error("Please provide both title and text")
            else:
                with st.spinner("Analyzing announcement... (may take 2-5 seconds)"):
                    result = classify_text(title_text, text_input)
                
                if result:
                    st.markdown("---")
                    render_result(result)
    
    # Tab 2: PDF Upload
    with tab2:
        st.subheader("Upload PDF Announcement")
        
        title_pdf = st.text_input(
            "Announcement Title",
            placeholder="e.g., ABC Corp - Proposed Acquisition",
            key="pdf_title"
        )
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload a corporate announcement PDF (max 7 MB)"
        )
        
        if uploaded_file:
            st.info(f"📄 File uploaded: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
        
        if st.button("🔍 Classify PDF", type="primary", key="classify_pdf"):
            if not title_pdf:
                st.error("Please provide an announcement title")
            elif not uploaded_file:
                st.error("Please upload a PDF file")
            else:
                with st.spinner("Extracting text from PDF and analyzing... (may take 3-7 seconds)"):
                    result = classify_pdf(title_pdf, uploaded_file)
                
                if result:
                    st.markdown("---")
                    render_result(result)
    
    # Tab 3: Try Samples
    with tab3:
        st.subheader("Try Sample Announcements")
        st.markdown("Select a pre-loaded sample to see how the classifier works:")
        
        sample = st.selectbox(
            "Choose a sample announcement",
            options=range(len(SAMPLE_ANNOUNCEMENTS)),
            format_func=lambda i: SAMPLE_ANNOUNCEMENTS[i]["title"]
        )
        
        selected = SAMPLE_ANNOUNCEMENTS[sample]
        
        st.text_input("Title", value=selected["title"], disabled=True)
        st.text_area("Text", value=selected["text"], height=200, disabled=True)
        
        if st.button("🔍 Classify Sample", type="primary", key="classify_sample"):
            with st.spinner("Analyzing announcement... (may take 2-5 seconds)"):
                result = classify_text(selected["title"], selected["text"])
            
            if result:
                st.markdown("---")
                render_result(result)
    
    # Footer
    st.markdown("---")
    st.caption("Built with Streamlit Cloud + AWS Lambda + AWS Bedrock | November 2025")


if __name__ == "__main__":
    main()
