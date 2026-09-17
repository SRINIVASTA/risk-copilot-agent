import streamlit as st
from copilot_engine import FraudCopilotEngine

st.set_page_config(page_title="Risk & Fraud Copilot", page_icon="🛡️", layout="wide")

st.title("🛡️ Risk, Fraud, and Regulatory Intelligence Copilot")
st.caption("Demonstrating Full Line-of-Custody: Signal Detection ➔ Evidence Gathering ➔ Audit Generation")

@st.cache_resource
def init_engine():
    return FraudCopilotEngine()

try:
    engine = init_engine()
except Exception as e:
    st.error(f"Initialization Error: Please verify your OPENAI_API_KEY environment variable is set. Details: {e}")
    st.stop()

st.sidebar.header("🎛️ Control Panel")
min_threshold = st.sidebar.slider("Cross-Border Alert Threshold (₹)", 1000000, 10000000, 5000000, step=500000)

if st.sidebar.button("Run Compliance Audit Pipeline", type="primary"):
    
    # ─── STEP 1: SIGNAL DETECTION ───
    st.header("✅ Step 1: Signal Detection (Structured Data)")
    signals = engine.detect_signals(min_amount=min_threshold)
    
    if not signals:
        st.warning("No anomalies detected for this configuration threshold.")
    else:
        st.dataframe(signals, use_container_width=True)
        
        # ─── STEP 2: EVIDENCE GATHERING ───
        st.header("🔎 Step 2: Evidence Gathering (Vector Store / RAG)")
        evidence = engine.gather_evidence(signals)
        st.code(evidence, language="text")
        
        # ─── STEP 3: AUDIT REPORT GENERATION ───
        st.header("📝 Step 3: Audit-Ready Report Generation")
        report_markdown = engine.generate_audit_report(signals, evidence)
        st.markdown(report_markdown)
        
        st.download_button(
            label="💾 Export STR Markdown File",
            data=report_markdown,
            file_name="Suspicious_Transaction_Report.md",
            mime="text/markdown"
        )
