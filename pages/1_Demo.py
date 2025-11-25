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
        "title": "Vista Equity Partners to Acquire Finastra - $8.4 Billion LBO",
        "text": """Vista Equity Partners has entered into a definitive agreement to acquire Finastra, 
        a leading global provider of financial software, from existing shareholders including Thoma Bravo 
        and funds managed by BC Partners. The transaction values Finastra at approximately $8.4 billion 
        enterprise value. The acquisition will be financed through a combination of equity from Vista Equity 
        Partners funds and committed debt financing arranged by Bank of America, Goldman Sachs, and JPMorgan. 
        Kirkland & Ellis LLP is serving as legal advisor to Vista Equity Partners. The transaction is expected 
        to close in Q2 2026, subject to customary regulatory approvals."""
    },
    {
        "title": "Microsoft Reports Strong Q4 Earnings - $65B Revenue (Should Reject)",
        "text": """Microsoft Corporation today announced financial results for the fourth quarter ended 
        June 30, 2025. Revenue was $65.0 billion and increased 15% (up 16% in constant currency). 
        Operating income was $29.2 billion and increased 18%. Net income was $23.9 billion and 
        increased 19%. Diluted earnings per share was $3.25 and increased 20%. "We delivered strong 
        results in the fourth quarter," said Satya Nadella, chairman and chief executive officer of Microsoft. 
        The Board of Directors declared a quarterly dividend of $0.75 per share."""
    },
    {
        "title": "REA Group Issues $500M Senior Notes - Refinancing (Should Reject)",
        "text": """REA Group Limited announced today the successful pricing of A$500 million 
        aggregate principal amount of 5.25% senior unsecured notes due 2030. The notes were priced 
        at par and the proceeds will be used primarily to refinance existing debt facilities and 
        for general corporate purposes. The offering is expected to settle on November 30, 2025. 
        Macquarie Capital and UBS acted as joint lead managers for the offering. The notes have been 
        rated BBB+ by S&P Global Ratings."""
    },
    {
        "title": "Apollo Leads $1.2B Buyout of Global Healthcare IT Provider",
        "text": """Apollo Global Management, Inc. announced today that funds managed by its affiliates 
        have entered into a definitive agreement to acquire Syntellis Performance Solutions, a leading 
        provider of enterprise performance management software for healthcare organizations, from 
        private equity firm Charlesbank Capital Partners. The transaction values Syntellis at 
        approximately $1.2 billion. The acquisition will be financed through Apollo funds' equity 
        commitments and $750 million in senior secured credit facilities provided by Morgan Stanley 
        and Credit Suisse. Cleary Gottlieb Steen & Hamilton LLP is legal counsel to Apollo. 
        Closing is expected in Q1 2026, subject to regulatory approvals and customary closing conditions."""
    },
    {
        "title": "Blackstone Acquires Industrial Portfolio - Real Estate (Should Reject)",
        "text": """Blackstone Real Estate Income Trust, Inc. (BREIT) today announced the acquisition 
        of a 2.5 million square foot industrial portfolio in the Sun Belt region for approximately 
        $425 million. The portfolio consists of 12 state-of-the-art logistics facilities across 
        Texas and Arizona, with an average occupancy rate of 97%. The properties are strategically 
        located near major transportation hubs. Wells Fargo Securities acted as financial advisor. 
        This acquisition enhances BREIT's industrial real estate portfolio."""
    },
    {
        "title": "Brookfield Infrastructure Closes $850M Acquisition of Data Center Assets",
        "text": """Brookfield Infrastructure Partners L.P. announced today the completion of its acquisition 
        of a portfolio of hyperscale data center assets from Digital Realty Trust for total consideration 
        of $850 million. The transaction includes four facilities totaling 450,000 square feet across 
        key markets in Northern Virginia and Silicon Valley. The acquisition was financed through 
        $300 million of equity from Brookfield's infrastructure funds and $550 million in project-level 
        debt provided by a syndicate led by HSBC and Citi. Paul Hastings LLP served as legal advisor. 
        This strategic acquisition expands Brookfield's digital infrastructure platform."""
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
    tab1, tab2, tab3 = st.tabs(["� Try Samples", "�📝 Text Input", "📄 PDF Upload"])
    
    # Tab 1: Try Samples
    with tab1:
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
    
    # Tab 2: Text Input
    with tab2:
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
    
    # Tab 3: PDF Upload
    with tab3:
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
    
    # Footer
    st.markdown("---")
    st.caption("Built with Streamlit Cloud + AWS Lambda + AWS Bedrock | November 2025")


if __name__ == "__main__":
    main()
