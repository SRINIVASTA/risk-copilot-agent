import streamlit as st
import subprocess
import sys
import os

# ─── 🛠️ EMERGENCY RUNTIME ENVIRONMENT INJECTION ───
# Forces installation of missing modules directly into the cloud node if requirements.txt was skipped
try:
    import langchain_google_genai
    import faiss
except ImportError:
    with st.spinner("🔧 Configuring application runtime dependencies... Please wait."):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "langchain-google-genai==1.0.8", "faiss-cpu>=1.8.0"])
    st.rerun()

# Set layout configurations directly
st.set_page_config(page_title="Risk & Fraud Copilot", page_icon="🛡️", layout="wide")

st.title("🛡️ Risk, Fraud, and Regulatory Intelligence Copilot (Gemini Edition)")
st.caption("Demonstrating Full Line-of-Custody: Signal Detection ➔ Evidence Gathering ➔ Audit Generation")

# ─── 🔑 AUTHENTICATION LAYER ───
st.sidebar.header("🔑 Authentication")
user_key = st.sidebar.text_input(
    "Enter Google API Key", 
    type="password", 
    help="Provide your Gemini API Key from Google AI Studio. It is safely isolated in session memory."
)

if user_key:
    os.environ["GOOGLE_API_KEY"] = user_key

# Prevent backend execution or crashes before key is populated
if not os.environ.get("GOOGLE_API_KEY"):
    st.info("💡 **Welcome!** Please enter your **Google API Key** in the sidebar panel to unlock the live Gemini data pipelines.")
    st.stop()

# Import the engine ONLY after dependencies are verified and the environment key is confirmed
from copilot_engine import FraudCopilotEngine

@st.cache_resource
def init_engine():
    return FraudCopilotEngine()

try:
    engine = init_engine()
except Exception as e:
    st.error(f"❌ Initialization Error: {e}")
    st.info("Please verify your API key is correct and valid inside Google AI Studio.")
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
        st.dataframe(signals, use_container_width=True)
        
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
