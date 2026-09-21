import streamlit as st
import subprocess
import sys
import os

# ─── 🛠️ RUNTIME ENVIRONMENT SYNC ───
try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    import faiss
    import plotly.express as px
    import pandas as pd
except ImportError:
    with st.spinner("🔧 Synchronizing production environment layers..."):
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--quiet", 
            "langchain-google-genai>=1.0.0", "faiss-cpu>=1.8.0", "plotly>=5.20.0"
        ])
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
    
    # Step 1: Signal Detection (DataFrame returned directly)
    st.header("✅ Step 1: Signal Detection (Structured Data)")
    with st.spinner("Filtering analytical ledgers..."):
        signals_df = engine.detect_signals(min_amount=min_threshold)
    
    if signals_df.empty:
        st.warning("No anomalies detected for this configuration threshold.")
    else:
        total_incidents = len(signals_df)
        st.success(f"Detected {total_incidents} matching high-risk account profiles.")
        
        # Force a safety alignment of column cases within the App execution context
        signals_df.columns = signals_df.columns.str.strip().str.upper()
        
        # Vectorized calculations mapped to explicit uppercase schema headers
        total_flagged_amt = int(signals_df["AMOUNT"].sum())
        avg_risk_score = float(signals_df["RISK_SCORE"].mean())
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label="🚨 Flagged Incidents Count", value=f"{total_incidents} Signals")
        col2.metric(label="💰 Total Capital Exposure", value=f"₹{total_flagged_amt:,}")
        col3.metric(label="⚠️ Average Network Risk Factor", value=f"{avg_risk_score:.1f}%")
        
        st.markdown("### Active Anomalous System Payload (PEP Monitored)")
        st.dataframe(signals_df, use_container_width=True)
        
        # ─── 📈 FIXED PLOTLY VISUALIZATION LAYER ───
        available_cols = list(signals_df.columns)
        hover_targets = [col for col in ["CUSTOMER_NAME", "COUNTRY_CODE", "KYC_STATUS", "IS_PEP"] if col in available_cols]
        
        try:
            fig = px.bar(
                signals_df, 
                x="TRANSACTION_ID" if "TRANSACTION_ID" in available_cols else available_cols, 
                y="AMOUNT" if "AMOUNT" in available_cols else available_cols, 
                color="RISK_SCORE" if "RISK_SCORE" in available_cols else None,
                hover_data=hover_targets,
                labels={"TRANSACTION_ID": "Transaction ID", "AMOUNT": "Amount (INR)", "RISK_SCORE": "Risk Level"},
                title="Anomalous Transaction Exposure & Associated Risk Index",
                color_continuous_scale="Reds"
            )
            fig.update_layout(template="plotly_dark", title_x=0.0)
            st.plotly_chart(fig, use_container_width=True)
        except Exception as chart_err:
            st.warning(f"📊 Visualization Layout Notice: {chart_err}. Renders default grid views instead.")
        
        # Step 2: Evidence Gathering
        st.header("🔎 Step 2: Evidence Gathering (Vector Store / RAG)")
        with st.spinner("Querying unstructured regulatory policy frameworks..."):
            evidence = engine.gather_evidence(signals_df)
        st.info("Extracted Regulatory Violations & Compliance Snippets:")
        st.code(evidence, language="text")
        
        # Step 3: Audit Report Generation
        st.header("📝 Step 3: Audit-Ready Report Generation")
        with st.spinner("Compiling final markdown template via Gemini..."):
            report_markdown = engine.generate_audit_report(signals_df, evidence)
        st.markdown(report_markdown)
        
        # 💾 Document Export Download Action
        st.download_button(
            label="💾 Export STR Markdown File",
            data=report_markdown,
            file_name="Suspicious_Transaction_Report.md",
            mime="text/markdown"
        )
