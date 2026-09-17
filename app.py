import streamlit as st
import subprocess
import sys
import os

# ─── 🛠️ RUNTIME ENVIRONMENT SYNC ───
try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    import faiss
except ImportError:
    with st.spinner("🔧 Synchronizing production environment layers..."):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "langchain-google-genai>=1.0.0", "faiss-cpu>=1.8.0"])
    st.rerun()

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
    # Force reset the cache if the key changes to prevent stale data
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
    st.info("If you still see a 404 error, click 'Manage app' and run a clean Reboot to wipe the old state cache.")
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
