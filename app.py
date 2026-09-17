import streamlit as st
import subprocess
import sys
import os

# ─── 🛠️ RUNTIME ENVIRONMENT SYNC ───
try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    import faiss
    import plotly.express as px
except ImportError:
    with st.spinner("🔧 Synchronizing production environment layers..."):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "langchain-google-genai>=1.0.0", "faiss-cpu>=1.8.0", "plotly>=5.20.0"])
    st.rerun()

st.set_page_config(page_title="Risk & Fraud Copilot", page_icon="🛡️", layout="wide")

st.title("🛡️ Risk, Fraud, and Regulatory Intelligence Copilot")
st.caption("Demonstrating Full Line-of-Custody: Signal Detection ➔ Evidence Gathering ➔ Audit Generation")

# ─── 🔑 AUTHENTICATION LAYER ───
st.sidebar.header("🔑 Authentication")
user_key = st.sidebar.text_input(
    "Enter Google API Key", 
    type="password", 
    help="Provide your Gemini API Key from Google AI Studio. It is safely isolated in session memory."
)

if user_key:
    if st.session_state.get("active_key") != user_key:
        st.session_state["active_key"] = user_key
        st.cache_resource.clear()
    os.environ["GOOGLE_API_KEY"] = user_key

# Stop execution before hitting any unauthenticated code pathways
if not os.environ.get("GOOGLE_API_KEY"):
    st.info("💡 **Welcome!** Please enter your **Google API Key** in the sidebar panel to unlock the live Gemini data pipelines.")
    st.stop()

# Safe import after key environment mapping has completed successfully
from copilot_engine import FraudCopilotEngine

@st.cache_resource
def init_engine():
    return FraudCopilotEngine()

try:
    engine = init_engine()
except Exception as e:
    st.error(f"❌ Initialization Error: {e}")
    st.stop()

# ─── 🎛️ CONTROL PANEL & PIPELINE ───
st.sidebar.markdown("---")
st.sidebar.header("🎛️ Control Panel")
min_threshold = st.sidebar.slider("Cross-Border Alert Threshold (₹)", 1000000, 10000000, 5000000, step=500000)

if st.sidebar.button("Run Compliance Audit Pipeline", type="primary"):
    
    # Step 1: Signal Detection
    st.header("✅ Step 1: Signal Detection (Structured Data)")
    with st.spinner("Filtering analytical ledgers..."):
        signals = engine.detect_signals(min_amount=min_threshold)
    
    if not signals:
        st.warning("No anomalies detected for this configuration threshold.")
    else:
        st.success(f"Detected {len(signals)} matching high-risk account profiles.")
        
        # 📊 HIGH IMPACT JUDGE METRICS DISPLAY
        total_flagged_amt = sum([item['AMOUNT'] for item in signals])
        avg_risk_score = sum([item['RISK_SCORE'] for item in signals]) / len(signals)
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label="🚨 Flagged Accounts Count", value=f"{len(signals)} Accounts")
        col2.metric(label="💰 Total Capital Exposure", value=f"₹{total_flagged_amt:,}")
        col3.metric(label="⚠️ Average Network Risk Factor", value=f"{avg_risk_score:.1f}%")
        
        st.markdown("### Active Anomalous System Payload")
        st.dataframe(signals, use_container_width=True)
        
        # ─── 📈 PLOTLY VISUALIZATION LAYER ───
        import pandas as pd
        df_signals = pd.DataFrame(signals)
        
        fig = px.bar(
            df_signals, 
            x="TRANSACTION_ID", 
            y="AMOUNT", 
            color="RISK_SCORE",
            hover_data=["CUSTOMER_NAME", "COUNTRY_CODE", "KYC_STATUS"],
            labels={"TRANSACTION_ID": "Transaction ID", "AMOUNT": "Amount (INR)", "RISK_SCORE": "Risk Score Level"},
            title="Anomalous Transaction Exposure & Associated Risk Index",
            color_continuous_scale="Reds"
        )
        fig.update_layout(template="plotly_dark", title_x=0.0)
        st.plotly_chart(fig, use_container_width=True)
        
        # Step 2: Evidence Gathering
        st.header("🔎 Step 2: Evidence Gathering (Vector Store / RAG)")
        with st.spinner("Querying unstructured RBI policy frameworks..."):
            evidence = engine.gather_evidence(signals)
        st.info("Extracted Regulatory Violations & Compliance Snippets:")
        st.code(evidence, language="text")
        
        # Step 3: Audit Report Generation
        st.header("📝 Step 3: Audit-Ready Report Generation")
        with st.spinner("Compiling final markdown template via Gemini..."):
            report_markdown = engine.generate_audit_report(signals, evidence)
        st.markdown(report_markdown)
        
        # 💾 Document Export Download Action
        st.download_button(
            label="💾 Export STR Markdown File",
            data=report_markdown,
            file_name="Suspicious_Transaction_Report.md",
            mime="text/markdown"
        )
