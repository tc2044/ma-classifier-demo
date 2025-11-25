"""
M&A Transaction Classifier - Introduction Page
Overview, problem statement, solution, and platform features

Author: Alex Chen
Date: November 25, 2025
"""

import streamlit as st

# ============================================================
# MAIN PAGE
# ============================================================

def main():
    st.set_page_config(
        page_title="M&A Transaction Classifier",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 M&A Transaction Classifier")
    st.markdown("**AI-Powered Deal Flow Intelligence**")
    
    st.markdown("---")
    
    # Problem Statement
    st.header("📊 Problem Statement")
    st.markdown("""
    Corporate announcements flood the market daily, making it challenging for:
    - **Investment professionals** to identify genuine M&A opportunities
    - **Market analysts** to track deal flow in real-time
    - **Corporate development teams** to monitor competitive M&A activity
    - **News aggregators** to filter relevant transactions
    
    **The Challenge**: Manually reviewing hundreds of announcements daily is time-consuming 
    and prone to missing critical deals hidden in complex corporate language.
    """)
    
    st.markdown("---")
    
    # Solution
    st.header("💡 Solution")
    st.markdown("""
    Our AI-powered classifier automatically analyzes corporate announcements and identifies 
    genuine M&A transactions with **95%+ accuracy**, processing each announcement in under 3 seconds.
    
    **How It Works**:
    1. **Smart Pre-filters** - Reject 60-70% of non-M&A announcements instantly
    2. **Feature Extraction** - Parse deal size, parties, transaction type
    3. **Rule-based Logic** - Apply domain expertise for clear-cut cases
    4. **AI Fallback** - AWS Bedrock Claude handles edge cases
    
    **Technology Stack**:
    - ⚡ **AWS Lambda** - Serverless compute
    - 🤖 **Bedrock Claude 3 Haiku** - Advanced AI reasoning
    - 📊 **Hybrid Approach** - Rules + AI for optimal accuracy
    - 🔒 **Secure & Scalable** - Enterprise-grade AWS infrastructure
    """)
    
    st.markdown("---")
    
    # Screenshots section
    st.header("🖼️ Platform Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📧 Email Notifications**")
        st.info("""
        Get instant alerts when new M&A transactions are detected:
        - Daily digest of qualified deals
        - Deal details: parties, size, type
        - Direct links to announcements
        - Customizable filters by sector/size
        """)
        # Placeholder for screenshot
        st.caption("_Screenshot: Email notification feature available in full platform_")
    
    with col2:
        st.markdown("**📈 Live Dashboard**")
        st.info("""
        Monitor M&A activity in real-time:
        - Visual deal pipeline
        - Historical trends & analytics
        - Sector breakdown
        - Export to Excel/CSV
        """)
        # Placeholder for screenshot
        st.caption("_Screenshot: Dashboard feature available in full platform_")
    
    st.markdown("---")
    
    # What Qualifies
    st.header("✅ Classification Criteria")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Qualifies as M&A**:")
        st.success("""
        - Acquisitions, mergers, takeovers
        - Strategic investments >$5M
        - Change of control transactions
        - Joint ventures with equity stakes
        - Asset acquisitions (substantial)
        """)
    
    with col2:
        st.markdown("**Does NOT qualify**:")
        st.warning("""
        - Financial results/earnings
        - Property transactions
        - Debt/bond issuance
        - Small deals (<$5M)
        - Procedural/corporate updates
        """)
    
    st.markdown("---")
    
    # Call to action
    st.header("� Try It Now")
    st.markdown("""
    Ready to experience the classifier? Use the **Interactive Demo** in the sidebar to:
    - Test with your own announcement text
    - Upload PDF announcements
    - Try pre-loaded sample scenarios
    
    Experience how AI can streamline your M&A research workflow!
    """)
    
    st.info("� **Navigate to 'Interactive Demo' using the sidebar to get started**")
    
    # Footer
    st.markdown("---")
    st.caption("Built with Streamlit Cloud + AWS Lambda + AWS Bedrock | November 2025")


if __name__ == "__main__":
    main()
