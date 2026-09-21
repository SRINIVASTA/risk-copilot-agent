# ─── BLOCK 1: INITIALIZATION & ENVIRONMENT SYNC ───
import streamlit as st
import subprocess
import sys
import os

try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    import faiss
    import plotly.express as px
    import pandas as pd
    from langchain_core.prompts import PromptTemplate
except ImportError:
    with st.spinner("🔧 Synchronizing production environment layers..."):
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--quiet", 
            "langchain-google-genai>=1.0.0", "faiss-cpu>=1.8.0", "plotly>=5.20.0"
        ])
    st.rerun()

st.set_page_config(page_title="Risk & Fraud Copilot Workspace", page_icon="🛡️", layout="wide")

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

if not os.environ.get("GOOGLE_API_KEY"):
    st.title("🛡️ Risk, Fraud, and Regulatory Intelligence Copilot")
    st.info("💡 **Welcome to the Workspace!** Please enter your **Google API Key** in the sidebar panel to unlock the live Gemini data pipelines and conversational engines.")
    st.stop()

from copilot_engine import FraudCopilotEngine

@st.cache_resource
def init_engine():
    return FraudCopilotEngine()

try:
    engine = init_engine()
except Exception as e:
    st.error(f"❌ Initialization Error: {e}")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.header("🎛️ Control Panel")
min_threshold = st.sidebar.slider("Cross-Border Alert Threshold (₹)", 1000000, 10000000, 5000000, step=500000)

if "messages" not in st.session_state:
    st.session_state.messages = []

tab1, tab2, tab3 = st.tabs(["📊 Operational Dashboard", "💬 Conversational CoCo Copilot", "📁 Account Directory Lookup"])

# ─── BLOCK 2: TAB 1 — OPERATIONAL PIPELINE TERMINAL ───
with tab1:
    st.header("🛡️ Risk & Compliance Monitoring Terminal")
    st.caption("Demonstrating Full Line-of-Custody: Signal Detection ➔ Evidence Gathering ➔ Audit Generation")
    
    if st.button("Run Global Compliance Audit Pipeline", type="primary"):
        st.subheader("✅ Step 1: Signal Detection (Structured Data)")
        with st.spinner("Filtering analytical ledgers..."):
            signals_df = engine.detect_signals(min_amount=min_threshold)
        
        if signals_df.empty:
            st.warning("No anomalies detected for this configuration threshold.")
        else:
            total_incidents = len(signals_df)
            st.success(f"Detected {total_incidents} matching high-risk account profiles.")
            
            signals_df.columns = signals_df.columns.str.strip().str.upper()
            total_flagged_amt = int(signals_df["AMOUNT"].sum())
            avg_risk_score = float(signals_df["RISK_SCORE"].mean())
            
            col1, col2, col3 = st.columns(3)
            col1.metric(label="🚨 Flagged Incidents Count", value=f"{total_incidents} Signals")
            col2.metric(label="💰 Total Capital Exposure", value=f"₹{total_flagged_amt:,}")
            col3.metric(label="⚠️ Average Network Risk Factor", value=f"{avg_risk_score:.1f}%")
            
            st.markdown("### Active Anomalous System Payload (PEP & Velocity Monitored)")
            st.dataframe(signals_df, use_container_width=True)
            
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
            
            st.subheader("🔎 Step 2: Evidence Gathering (Vector Store / RAG)")
            with st.spinner("Querying unstructured regulatory policy frameworks..."):
                evidence = engine.gather_evidence(signals_df)
            st.info("Extracted Regulatory Violations & Compliance Snippets:")
            st.code(evidence, language="text")
            
            st.subheader("📝 Step 3: Audit-Ready Report Generation")
            with st.spinner("Compiling final markdown template via Gemini..."):
                report_markdown = engine.generate_audit_report(signals_df, evidence)
            st.markdown(report_markdown)
            
            st.download_button(
                label="💾 Export STR Markdown File",
                data=report_markdown,
                file_name="Suspicious_Transaction_Report.md",
                mime="text/markdown"
            )
# ─── BLOCK 3: TAB 2 — CONVERSATIONAL CORTEX COPILOT (FIXED) ───
with tab2:
    st.header("💬 Conversational Cortex Copilot Room")
    st.caption("Ask natural language compliance questions about yesterday's anomalies or regulatory requirements.")
    
    st.markdown("### 💡 Quick Suggestion Queries")
    col_q1, col_q2 = st.columns(2)
    
    q1_text = "Show me high-risk customers with Politically Exposed Person (PEP) flags."
    q2_text = "Are there any velocity alerts or potential layering attempts in the last 48 hours?"
    
    prompt_click = None
    if col_q1.button(f"🔍 {q1_text}", use_container_width=True):
        prompt_click = q1_text
    if col_q2.button(f"🚨 {q2_text}", use_container_width=True):
        prompt_click = q2_text
        
    st.markdown("---")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    user_prompt = st.chat_input("Ask CoCo about transactions, accounts, or RBI compliance playbooks...")
    
    if prompt_click:
        user_prompt = prompt_click

    if user_prompt:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("CoCo processing analytical frameworks..."):
                # Fetch a reference baseline dataset to answer conversational prompts accurately
                reference_df = engine.detect_signals(min_amount=min_threshold)
                
                # Self-healing safety layer: Force all column variations to strict uppercase strings
                reference_df.columns = reference_df.columns.str.strip().str.upper()
                
                policy_context = engine.gather_evidence(reference_df)
                
                chat_template = """
                You are 'CoCo', an elite conversational AI Fraud and Compliance Copilot operating under RBI regulations.
                Answer the user's analytical query precisely using the structural database log metrics and vector rules provided.
                
                ACTIVE DATA MATRIX PAYLOAD:
                {data_summary}
                
                REGULATORY POLICY EVIDENCE BASE:
                {policy_context}
                
                QUERY FOR RESOLUTION:
                {user_query}
                
                Keep your response conversational, concise, professional, and clear. Avoid hallucinations. Quote sections directly if needed.
                """
                
                # Dynamic column intersection builder to completely prevent KeyError crashes
                target_columns = ["TRANSACTION_ID", "ACCOUNT_ID", "CUSTOMER_NAME", "AMOUNT", "COUNTRY_CODE", "RISK_SCORE", "KYC_STATUS", "IS_PEP"]
                existing_columns = [col for col in target_columns if col in reference_df.columns]
                
                # If target columns match, slice them safely; otherwise fall back to all available fields
                if len(existing_columns) > 0:
                    data_summary = reference_df[existing_columns].to_string()
                else:
                    data_summary = reference_df.to_string()
                
                prompt_obj = PromptTemplate.from_template(chat_template)
                chat_chain = prompt_obj | engine.llm
                
                ai_response = chat_chain.invoke({
                    "data_summary": data_summary,
                    "policy_context": policy_context,
                    "user_query": user_prompt
                })
                
                st.markdown(ai_response.content)
                st.session_state.messages.append({"role": "assistant", "content": ai_response.content})
# ─── BLOCK 4: TAB 3 — CUSTOMER 360 DIRECTORY LOOKUP (VERIFIED) ───
with tab3:
    st.header("📁 Customer 360 Account Profile Registry")
    st.caption("Select any customer from the repository system layers to inspect their risk characteristics instantly.")
    
    engine.acc_df.columns = engine.acc_df.columns.str.strip().str.upper()
    
    account_list = engine.acc_df["ACCOUNT_ID"].unique()
    selected_acc = st.selectbox("Select Target Account ID to Screen:", account_list)
    
    if selected_acc:
        matched_rows = engine.acc_df[engine.acc_df["ACCOUNT_ID"] == selected_acc]
        
        if not matched_rows.empty:
            # Safely grab the first row item entry as a clean Python dictionary list series
            profile = matched_rows.iloc[0].to_dict()
            
            engine.tx_df.columns = engine.tx_df.columns.str.strip().str.upper()
            related_tx = engine.tx_df[engine.tx_df["ACCOUNT_ID"] == selected_acc]
            
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"**Customer Name:**\n\n{profile.get('CUSTOMER_NAME', 'N/A')}")
            
            status = str(profile.get('KYC_STATUS', '')).strip()
            status_color = "🔴" if status == "Suspended" else "🟡" if status == "Pending" else "🟢"
            c2.markdown(f"**KYC Onboarding Status:**\n\n{status_color} {status}")
            
            is_pep_val = str(profile.get('IS_PEP', '')).strip().lower() == 'true'
            pep_badge = "🚨 POLITICALLY EXPOSED PERSON (HIGH RISK)" if is_pep_val else "🟢 Standard Client Profile"
            c3.markdown(f"**Political Profile Matrix:**\n\n{pep_badge}")
            c4.markdown(f"**Entity Classification:**\n\n{profile.get('CUSTOMER_TYPE', 'N/A')}")
            
            st.markdown("#### Historical Transaction Ledger Matrix for this Profile")
            if related_tx.empty:
                st.info("No transaction telemetry logs found on file for this specific profile line.")
            else:
                st.dataframe(related_tx, use_container_width=True)
        else:
            st.error("❌ The selected Account ID profile could not be found within active datasets.")
