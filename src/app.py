import streamlit as st
import pandas as pd
import os

# 1. Page Configuration
st.set_page_config(page_title="Risk & AML Copilot", layout="wide")
st.title("🏦 Risk, Fraud & Regulatory Intelligence Copilot")
st.caption("Snowflake CoCo CLI Hackathon — GCC Edition 2026")

# 2. Establish Secure Snowflake Connection for Streamlit Cloud
def get_active_session():
    import snowflake.connector
    # This reads credentials securely from your Streamlit Secrets or Environment Variables
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database="HACKATHON_RISK_DB",
        schema="RISK_SCHEMA"
    )
    return conn

# 3. User Input Query UI
user_query = st.text_input(
    "Enter your regulatory query or compliance objective:",
    value="Audit high-value transactions from unverified accounts this week"
)

if user_query:
    with st.spinner("🕵️‍♂️ Orchestrating agent workflow (Data ➔ Evidence ➔ Report)..."):
        try:
            # Connect to database via regular connector profile
            conn = get_active_session()
            cursor = conn.cursor()
            
            # --- STEP 1: SIGNAL DETECTION (Structured SQL) ---
            signal_sql = """
                SELECT t.transaction_id, t.account_id, a.customer_name, t.amount, t.country_code, a.kyc_status
                FROM TRANSACTION_LEDGER t
                JOIN ACCOUNT_MASTER a ON t.account_id = a.account_id
                WHERE t.amount > 5000000 AND a.kyc_status = 'PENDING';
            """
            cursor.execute(signal_sql)
            records = cursor.fetchall()
            
            # Load transaction rows into standard pandas dataframe
            df_signals = pd.DataFrame(records, columns=['TRANSACTION_ID', 'ACCOUNT_ID', 'CUSTOMER_NAME', 'AMOUNT', 'COUNTRY_CODE', 'KYC_STATUS'])
            
            # --- STEP 2: EVIDENCE GATHERING (Unstructured Text) ---
            cursor.execute("SELECT content_chunk FROM POLICIES_TEXT_BASE")
            policy_rows = cursor.fetchall()
            policy_context = "\n".join([row[0] for row in policy_rows])

            # --- DISPLAY DASHBOARD LAYOUT GRID ---
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📊 Live Fraud Signals Detected")
                if not df_signals.empty:
                    st.dataframe(df_signals, use_container_width=True)
                    
                    # Package structured rows into readable string snippets for the AI
                    signal_context = ""
                    for _, row in df_signals.iterrows():
                        signal_context += f"Account {row['CUSTOMER_NAME']} ({row['ACCOUNT_ID']}) transferred {row['AMOUNT']} INR to country {row['COUNTRY_CODE']} with KYC Status: {row['KYC_STATUS']}.\n"
                else:
                    st.success("No critical high-risk signals found.")
                    signal_context = "No anomalous transaction parameters detected."

            with col2:
                st.subheader("📄 Generated Audit-Ready Report")
                
                # Ground the prompt boundary to prevent AI hallucinations
                prompt = f"""
                You are an expert compliance officer at an NBFC banking unit. Produce an official, audit-ready Suspicious Transaction Report (STR).
                
                STRUCTURED DATA SIGNALS:
                {signal_context}
                
                REGULATORY LAW BASELINES:
                {policy_context}
                
                Instructions: Identify compliance violations and cite the exact rule code (e.g. RULE-AML-01 or RULE-KYC-02). Format beautifully using professional markdown headers, lists, and bold text.
                """
                
                if not df_signals.empty:
                    # --- STEP 3: EXECUTE CORTEX VIA RAW SQL QUERY ---
                    # This safely bypasses all session/UDF library validation bugs!
                    cortex_sql = "SELECT CORTEX.COMPLETE('snowflake-arctic', %s)"
                    cursor.execute(cortex_sql, (prompt,))
                    report_output = cursor.fetchone()[0]
                    
                    # Render the beautiful compliance report output
                    st.markdown(report_output)
                    st.download_button("📥 Export Report as TXT", data=report_output, file_name="STR_Audit_Report.txt")
                else:
                    st.info("Awaiting high-risk flags to generate report documentation.")

            cursor.close()
            conn.close()

        except Exception as e:
            st.error(f"Error processing transaction pipeline: {str(e)}")
