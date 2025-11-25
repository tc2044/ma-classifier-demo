"""
M&A Transaction Classifier - Introduction Page
Introduction, problem statement, and solution overview

Author: Alex Chen
Date: November 25, 2025
"""

import streamlit as st
import os
from pathlib import Path

st.set_page_config(
    page_title="M&A Transaction Classifier",
    page_icon="🔍",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.markdown("### 📍 Navigation")
    st.info("Use the navigation above to switch between pages")
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.caption("AI-powered M&A & corporate finance classifier")
    st.caption("**Tech Stack:** AWS Lambda + Bedrock Claude")
    st.caption("**Accuracy:** 95%+")
    st.caption("**Detects:** M&A, LBOs, Debt Financing")

st.title("🤖 AI-Powered Corporate Finance Intelligence")
st.markdown("**Automated M&A, LBO & Debt Transaction Classification**")

st.markdown("---")

# Problem Statement
st.header("📊 Problem Statement")
st.markdown("""
Corporate announcements flood the market daily, making it challenging for:
- **Investment professionals** to identify genuine M&A opportunities and financing transactions
- **Market analysts** to track deal flow and leverage finance activity in real-time
- **Corporate development teams** to monitor competitive M&A activity
- **News aggregators** to filter relevant corporate finance transactions

**The Challenge**: Manually reviewing hundreds of announcements daily is time-consuming 
and prone to missing critical deals hidden in complex corporate language.
""")

st.markdown("---")

# Solution
st.header("💡 Solution")
st.markdown("""
Our AI-powered classifier automatically analyzes corporate announcements and identifies 
genuine M&A transactions, leverage finance, debt issuances, and other corporate finance activities 
with **95%+ accuracy**, processing each announcement in under 3 seconds.

**How It Works**:
1. **Smart Pre-filters** - Reject 60-70% of non-relevant announcements instantly
2. **Feature Extraction** - Parse deal size, parties, transaction type, financing structure
3. **Rule-based Logic** - Apply domain expertise for clear-cut cases
4. **AI Fallback** - AWS Bedrock Claude handles edge cases and complex structures

**Technology Stack**:
- ⚡ **AWS Lambda** - Serverless compute
- 🤖 **Bedrock Claude 3 Haiku** - Advanced AI reasoning
- 📊 **Hybrid Approach** - Rules + AI for optimal accuracy
- 🔒 **Secure & Scalable** - Enterprise-grade AWS infrastructure
""")

st.markdown("---")

# Screenshots section
st.header("🖼️ Platform Features")

# Display screenshot
try:
    # Get the directory of the current file and go up one level
    current_dir = Path(__file__).parent.parent
    image_path = current_dir / "screenshot-dashboard.png"
    
    if image_path.exists():
        st.image(str(image_path), 
                 caption="M&A Classifier Dashboard", 
                 use_container_width=True)
        st.markdown("")  # Add spacing
    else:
        st.warning(f"Screenshot not available (looking for: {image_path})")
except Exception as e:
    st.warning(f"Screenshot not available: {str(e)}")

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
    st.caption("_Feature available in full platform_")

with col2:
    st.markdown("**📈 Live Dashboard**")
    st.info("""
    Monitor M&A activity in real-time:
    - Visual deal pipeline
    - Historical trends & analytics
    - Sector breakdown
    - Export to Excel/CSV
    """)
    st.caption("_Feature available in full platform_")

st.markdown("---")

# What Qualifies
st.header("✅ Classification Criteria")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Qualifies as M&A / Corporate Finance**:")
    st.success("""
    - Acquisitions, mergers, takeovers
    - Strategic investments >$5M
    - Change of control transactions
    - Joint ventures with equity stakes
    - Asset acquisitions (substantial)
    - Leverage finance / LBO transactions
    - Debt issuance for acquisitions
    - Corporate financing activities
    """)

with col2:
    st.markdown("**Does NOT qualify**:")
    st.warning("""
    - Financial results/earnings
    - Property transactions
    - General working capital debt
    - Small deals (<$5M)
    - Procedural/corporate updates
    - Refinancing only (no M&A component)
    """)

st.markdown("---")

# Call to action
st.header("🚀 Try It Now")
st.success("""
**Click on 'Demo' in the sidebar** to try the interactive classifier with:
- **Text Input** - Paste announcement text
- **PDF Upload** - Upload announcement PDFs
- **Try Samples** - Test with pre-loaded examples
""")

# Footer
st.markdown("---")
st.caption("Built with Streamlit Cloud + AWS Lambda + AWS Bedrock | November 2025")
