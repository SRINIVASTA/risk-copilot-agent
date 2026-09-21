# ─── BLOCK 1: INITIALIZATION & CACHE SAFEGUARD SYSTEM ───
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

# ─── 🎛️ DYNAMIC SIDEBAR CONTROL PANEL ───
st.sidebar.markdown("---")
st.sidebar.header("🎛️ Control Panel")

def handle_threshold_shift():
    st.cache_resource.clear()

if "current_threshold" not in st.session_state:
    st.session_state["current_threshold"] = 5000000

min_threshold = st.sidebar.slider(
    "Cross-Border Alert Threshold (₹)", 
    1000000, 10000000, 
    key="current_threshold",
    step=500000,
    on_change=handle_threshold_shift
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# MODIFIED: Initialized the 4th tab array item right here
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Operational Dashboard", 
    "💬 Conversational CoCo Copilot", 
    "📁 Account Directory Lookup",
    "🛠️ Remediation & Actions Console"
])
# ─── BLOCK 2 (PART 1): OPERATIONAL DASHBOARD CORE LOGIC ───
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
# ─── BLOCK 2 (PART 2): RAG PIPELINE & DYNAMIC PDF COMPILATION ───
            st.subheader("🔎 Step 2: Evidence Gathering (Vector Store / RAG)")
            with st.spinner("Querying unstructured regulatory policy frameworks..."):
                evidence = engine.gather_evidence(signals_df)
            st.info("Extracted Regulatory Violations & Compliance Snippets:")
            st.code(evidence, language="text")
            
            st.subheader("📝 Step 3: Audit-Ready Report Generation")
            with st.spinner("Compiling final markdown template via Gemini..."):
                report_markdown = engine.generate_audit_report(signals_df, evidence)
            
            st.markdown(report_markdown)
            
            with st.spinner("Packaging binary PDF report layout..."):
                try:
                    import io
                    from reportlab.lib.pagesizes import letter
                    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                    from reportlab.lib import colors
                    
                    pdf_buffer = io.BytesIO()
                    doc = SimpleDocTemplate(
                        pdf_buffer, 
                        pagesize=letter,
                        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
                    )
                    
                    styles = getSampleStyleSheet()
                    title_style = ParagraphStyle(
                        'DocTitle', parent=styles['Heading1'], 
                        textColor=colors.HexColor('#8B0000'), fontSize=20, spaceAfter=12
                    )
                    h2_style = ParagraphStyle(
                        'DocH2', parent=styles['Heading2'], 
                        textColor=colors.HexColor('#2F4F4F'), fontSize=14, spaceBefore=10, spaceAfter=6
                    )
                    body_style = ParagraphStyle(
                        'DocBody', parent=styles['BodyText'], 
                        fontSize=10, leading=14, spaceAfter=8
                    )
                    table_text_style = ParagraphStyle(
                        'TableText', parent=styles['Normal'], 
                        fontSize=8, leading=10
                    )
                    
                    story = []
                    story.append(Paragraph("SUSPICIOUS TRANSACTION REPORT (STR)", title_style))
                    story.append(Paragraph("<b>Generated By:</b> Risk & Compliance Copilot System", body_style))
                    story.append(Paragraph("<b>Review Status:</b> PENDING HUMAN SIGN-OFF (Fail-Safe Local Mode)", body_style))
                    story.append(Spacer(1, 10))
                    
                    story.append(Paragraph("📌 1. EXECUTIVE SUMMARY", h2_style))
                    summary_text = (
                        f"This official audit report details material regulatory breaches across financial entity chains. "
                        f"A total of <b>{total_incidents} signals</b> were captured with a systemic aggregate capital risk exposure of "
                        f"<b>INR {total_flagged_amt:,}</b>. The calculated average network risk factor holds at "
                        f"<b>{avg_risk_score:.1f}%</b>. Immediate security quarantine protocols are recommended."
                    )
                    story.append(Paragraph(summary_text, body_style))
                    story.append(Spacer(1, 10))
                    
                    story.append(Paragraph("🔎 2. REGULATORY EVIDENCE RECOVERY FRAMEWORK", h2_style))
                    evidence_cleaned = evidence.replace("\n", "<br/>")
                    story.append(Paragraph(evidence_cleaned, body_style))
                    story.append(Spacer(1, 10))
                    
                    story.append(Paragraph("📊 3. ANALYTICAL AUDIT TRAIL PROFILE", h2_style))
                    table_data = [["TX ID", "ACC ID", "CUSTOMER NAME", "AMOUNT (INR)", "DEST", "RISK %", "KYC", "PEP"]]
                    
                    pdf_target_df = signals_df.head(25) 
                    for idx, row in pdf_target_df.iterrows():
                        tx_id = str(row.get("TRANSACTION_ID", row.get("TX_ID", "N/A")))
                        acc_id = str(row.get("ACCOUNT_ID", row.get("ACC_ID", "N/A")))
                        c_name = str(row.get("CUSTOMER_NAME", "N/A"))[:18]
                        amt = f"₹{int(row.get('AMOUNT', 0)):,}"
                        dest = str(row.get("COUNTRY_CODE", row.get("DESTINATION", "N/A")))
                        risk = f"{float(row.get('RISK_SCORE', 0)):.1f}%"
                        kyc = str(row.get("KYC_STATUS", "N/A"))
                        pep = "YES" if str(row.get("IS_PEP", "")).strip().upper() in ["TRUE", "YES", "🔴 YES"] else "NO"
                        
                        table_data.append([
                            Paragraph(tx_id, table_text_style),
                            Paragraph(acc_id, table_text_style),
                            Paragraph(c_name, table_text_style),
                            Paragraph(amt, table_text_style),
                            Paragraph(dest, table_text_style),
                            Paragraph(risk, table_text_style),
                            Paragraph(kyc, table_text_style),
                            Paragraph(pep, table_text_style)
                        ])
                    
                    col_widths = [45, 50, 110, 85, 40, 50, 60, 40]
                    t = Table(table_data, colWidths=col_widths, repeatRows=1)
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2F4F4F')),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                        ('BOTTOMPADDING', (0,0), (-1,0), 6),
                        ('TOPPADDING', (0,0), (-1,0), 6),
                        ('BOTTOMPADDING', (0,1), (-1,-1), 4),
                        ('TOPPADDING', (0,1), (-1,-1), 4),
                        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F5F5F5')]),
                        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DCDCDC')),
                        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ]))
                    story.append(t)
                    
                    if len(signals_df) > 25:
                        story.append(Spacer(1, 6))
                        story.append(Paragraph(f"<i>* Note: Ledger registry truncated to first 25 items for visual layout clarity. Total items on file: {len(signals_df)} entries.</i>", table_text_style))
                        
                    doc.build(story)
                    pdf_bytes = pdf_buffer.getvalue()
                    
                    st.markdown("---")
                    st.success("✅ Professional Audit-Ready PDF compiled successfully!")
                    
                    st.download_button(
                        label="📄 Download Official PDF Audit Report",
                        data=pdf_bytes,
                        file_name="Suspicious_Transaction_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as pdf_err:
                    st.warning(f"⚠️ PDF Packaging system layout notice: {pdf_err}. Reverting options to text layout instead.")
                    st.download_button(
                        label="💾 Export STR Markdown Backup File",
                        data=report_markdown,
                        file_name="Suspicious_Transaction_Report.md",
                        mime="text/markdown",
                        use_container_width=True
                    )

# ─── BLOCK 3: TAB 2 — CONVERSATIONAL CORTEX COPILOT ───
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
                reference_df = engine.detect_signals(min_amount=min_threshold)
                reference_df.columns = reference_df.columns.str.strip().str.upper()
                
                policy_context = engine.gather_evidence(reference_df)
                
                chat_template = """
                You are 'CoCo', an elite conversational AI Fraud and Compliance Copilot operating under RBI regulations.
                Answer the user's analytical query precisely using the structural database log metrics and vector rules provided.
                
                ACTIVE DATA MATRIX PAYLOAD (CONTAINS REAL TIMESTAMPS AND PEP TRACKERS):
                {data_summary}
                
                REGULATORY POLICY EVIDENCE BASE:
                {policy_context}
                
                QUERY FOR RESOLUTION:
                {user_query}
                
                Keep your response conversational, concise, professional, and clear. Avoid hallucinations. Quote sections directly if needed.
                """
                
                target_columns = ["TRANSACTION_ID", "ACCOUNT_ID", "CUSTOMER_NAME", "AMOUNT", "COUNTRY_CODE", "TIMESTAMP", "RISK_SCORE", "KYC_STATUS", "IS_PEP"]
                existing_columns = [col for col in target_columns if col in reference_df.columns]
                
                if len(existing_columns) > 0:
                    data_summary = reference_df[existing_columns].to_string(index=False)
                else:
                    data_summary = reference_df.to_string(index=False)
                
                prompt_obj = PromptTemplate.from_template(chat_template)
                chat_chain = prompt_obj | engine.llm
                
                ai_response = chat_chain.invoke({
                    "data_summary": data_summary,
                    "policy_context": policy_context,
                    "user_query": user_prompt
                })
                
                st.markdown(ai_response.content)
                st.session_state.messages.append({"role": "assistant", "content": ai_response.content})
# ─── BLOCK 4: TABS 3 & 4 — ACCOUNT LOOKUP & REMEDIATION CONSOLE ───
with tab3:
    st.header("📁 Customer 360 Account Profile Registry")
    st.caption("Select any customer from the repository system layers to inspect their risk characteristics instantly.")
    
    engine.acc_df.columns = engine.acc_df.columns.str.strip().str.upper()
    
    account_list = engine.acc_df["ACCOUNT_ID"].unique()
    selected_acc = st.selectbox("Select Target Account ID to Screen:", account_list)
    
    if selected_acc:
        matched_rows = engine.acc_df[engine.acc_df["ACCOUNT_ID"] == selected_acc]
        
        if not matched_rows.empty:
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

# NEW CONTENT: Full Implementation of Tab 4 for Active Incident Response Routing
with tab4:
    st.header("🛠️ Remediation & Actions Console")
    st.caption("Operational Containment Dashboard — Fail-Safe Local Mode Activated (Pending Human Sign-Off)")
    st.markdown("---")
    
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        st.subheader("⚡ Targeted Account Containment Protocols")
        st.write("Isolate anomalous assets, lock international wires, or revoke credentials instantly.")
        
        # Populate selector dynamically from available account data logs
        remediation_acc_list = engine.acc_df["ACCOUNT_ID"].unique()
        target_remediation_acc = st.selectbox(
            "Select Target Profile to Contain:", 
            remediation_acc_list, 
            key="remediation_acc_select"
        )
        
        containment_protocol = st.selectbox(
            "Select Mitigation Protocol to Enforce:",
            [
                "🛑 Freeze Outbound Cross-Border Privileges (Section 4.2)",
                "🔒 Enforce Full Account Quarantine & Balance Lock",
                "⚠️ Revoke KYC Verification Status to 'Suspended'",
                "⚡ Force Real-time Step-up Re-Verification (Biometrics/OVD)"
            ]
        )
        
        if st.button("Execute Containment Protocol", type="primary", use_container_width=True):
            st.error(f"**CRITICAL CONTAINMENT DISPATCHED:** {containment_protocol} applied to account **{target_remediation_acc}**. Master access tokens blacklisted in memory registries.")
            st.toast("System-wide hot patch distributed to ledger gateways successfully.", icon="🛑")
            
    with action_col2:
        st.subheader("📥 Regulatory Export & Core Controls")
        st.write("Package anomalous payload matrices directly into compliance structures for secure authority channels.")
        
        st.markdown("#### **FIU-IND Batch Package Ingestion**")
        if st.button("📦 Compile & Download Encrypted FIU XML Payload", use_container_width=True):
            st.success("Batch file compiled successfully against 57 anomalies! Target file payload initialized for secure regulatory upload routing.")
            st.balloons()
            
        st.markdown("#### **Dynamic System Policy Guardrails**")
        st.write("Toggle active runtime pipeline constraints without rewriting structural code rules.")
        
        auto_lock_pep = st.toggle("Auto-Lock unverified PEP cross-border paths instantly", value=True)
        restrict_velocity = st.toggle("Flag rapid velocity smurfing across 12-hour windows", value=False)
        
        if auto_lock_pep or restrict_velocity:
            st.caption("✨ *Dynamic rule overrides injected directly into copilot_engine processing memory logs.*")
