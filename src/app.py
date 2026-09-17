import streamlit as st
import pandas as pd
import snowflake.permissions as permissions
from snowflake.cortex import Complete
import os

# 1. Page Configuration & Visual Anchors
st.set_page_config(page_title="Risk & AML Copilot", layout="wide")
st.title("🏦 Risk, Fraud & Regulatory Intelligence Copilot")
st.caption("Snowflake CoCo CLI Hackathon — GCC Edition 2026")

# 2. Establish Secure Snowflake Connection
def get_active_session():
    # If running inside Snowflake, it uses the active session automatically
    try:
        from snowflake.snowpark.context import get_active_session
        return get_active_session()
    except ImportError:
        # Fallback for running locally during testing
        import snowflake.connector
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
    placeholder="e.g., Audit high-value transactions from unverified accounts this week."
)

if user_query:
    with st.spinner("🕵️‍♂️ Orchestrating agent workflow (Data ➔ Evidence ➔ Report)..."):
        try:
            session = get_active_session()
            
            # --- STEP 1: SIGNAL DETECTION (Structured Query Execution) ---
            # Automatically filtering cross-border wire transfers based on typical high-risk patterns
            signal_sql = """
                SELECT t.transaction_id, t.account_id, a.customer_name, t.amount, t.country_code, a.kyc_status
                FROM TRANSACTION_LEDGER t
                JOIN ACCOUNT_MASTER a ON t.account_id = a.account_id
                WHERE t.amount > 5000000 AND a.kyc_status = 'PENDING';
            """
            
            # Executing and loading structured anomalies into a pandas dataframe
            if hasattr(session, "sql"):  # Snowpark Environment
                df_signals = session.sql(signal_sql).to_pandas()
                # Dummy execute for LLM simulation text extraction
                policy_rows = session.sql("SELECT content_chunk FROM POLICIES_TEXT_BASE").to_pandas()
                policy_context = "\n".join(policy_rows['CONTENT_CHUNK'].tolist())
            else:  # Standard Snowflake Connector Environment
                cursor = session.cursor()
                cursor.execute(signal_sql)
                df_signals = pd.DataFrame(cursor.fetchall(), columns=['TRANSACTION_ID', 'ACCOUNT_ID', 'CUSTOMER_NAME', 'AMOUNT', 'COUNTRY_CODE', 'KYC_STATUS'])
                cursor.execute("SELECT content_chunk FROM POLICIES_TEXT_BASE")
                policy_context = "\n".join([row[0] for row in cursor.fetchall()])
                cursor.close()

            # --- DISPLAY THE DASHBOARD LAYOUT ---
            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader("📊 Live Fraud Signals Detected")
                if not df_signals.empty:
                    st.dataframe(df_signals, use_container_width=True)
                    # Format data entries as clean context strings for the LLM context prompt window
                    signal_context = ""
                    for _, row in df_signals.iterrows():
                        signal_context += f"Account {row['CUSTOMER_NAME']} ({row['ACCOUNT_ID']}) transferred {row['AMOUNT']} INR to high-risk country code {row['COUNTRY_CODE']} with KYC Status: {row['KYC_STATUS']}.\n"
                else:
                    st.success("No critical high-risk signal variances found.")
                    signal_context = "No anomalous transaction parameters detected."

            with col2:
                st.subheader("📄 Generated Audit-Ready Report")
                
                # --- STEP 3: CONTEXT COMPILATION & REPORT GENERATION ---
                prompt = f"""
                You are an expert enterprise compliance officer at an NBFC banking unit. Produce an official, audit-ready Suspicious Transaction Report (STR) or Case Assessment based ONLY on the evidence provided below.
                
                STRUCTURED DATA SIGNALS:
                {signal_context}
                
                REGULATORY MOCK LAW BASELINES:
                {policy_context}
                
                Instructions:
                1. Clearly define the regulatory compliance breach.
                2. Explicitly cite the exact rule code (e.g. RULE-AML-01 or RULE-KYC-02) from the guidelines.
                3. Structure output neatly using professional markdown formatting. Include an Executive Summary, Details Table, and Next Steps.
                """
                
                # Executing the Cortex LLM Text generation call safely
                if not df_signals.empty:
                    report_output = Complete("snowflake-arctic", prompt, session=session)
                    st.markdown(report_output)
                    
                    # Add download button for submission completeness
                    st.download_button("📥 Export Report as TXT File", data=report_output, file_name="STR_Audit_Report.txt")
                else:
                    st.info("Awaiting high-risk flags to generate report documentation.")

        except Exception as e:
            st.error(f"Error processing transaction pipeline: {str(e)}")
