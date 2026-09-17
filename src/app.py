import streamlit as st
import pandas as pd
import os

# 1. Page Configuration
st.set_page_config(page_title="Risk & AML Copilot", layout="wide")
st.title("🏦 Risk, Fraud & Regulatory Intelligence Copilot")
st.caption("Snowflake CoCo CLI Hackathon — GCC Edition 2026")

# 2. Hybrid Connection Architecture (Detects Platform Environment Automatically)
def get_active_session():
    try:
        # If running INSIDE Snowflake, this succeeds instantly
        from snowflake.snowpark.context import get_active_session
        return get_active_session(), "NATIVE"
    except ImportError:
        # Fallback for running OUTSIDE on external Streamlit Web Apps
        import snowflake.connector
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database="HACKATHON_RISK_DB",
            schema="RISK_SCHEMA"
        )
        return conn, "EXTERNAL"

# 3. User Input Query UI
user_query = st.text_input(
    "Enter your regulatory query or compliance objective:",
    value="Audit high-value transactions from unverified accounts this week"
)

if user_query:
    with st.spinner("🕵️‍♂️ Orchestrating agent workflow (Data ➔ Evidence ➔ Report)..."):
        try:
            conn, env_mode = get_active_session()
            signal_sql = """
                SELECT t.transaction_id, t.account_id, a.customer_name, t.amount, t.country_code, a.kyc_status
                FROM TRANSACTION_LEDGER t
                JOIN ACCOUNT_MASTER a ON t.account_id = a.account_id
                WHERE t.amount > 5000000 AND a.kyc_status = 'PENDING';
            """
            
            # --- EXTRACT STRUCTURED SIGNALS ---
            if env_mode == "NATIVE":
                df_signals = conn.sql(signal_sql).to_pandas()
                policy_rows = conn.sql("SELECT content_chunk FROM POLICIES_TEXT_BASE").to_pandas()
                policy_context = "\n".join(policy_rows['CONTENT_CHUNK'].tolist())
            else:
                cursor = conn.cursor()
                cursor.execute(signal_sql)
                df_signals = pd.DataFrame(cursor.fetchall(), columns=['TRANSACTION_ID', 'ACCOUNT_ID', 'CUSTOMER_NAME', 'AMOUNT', 'COUNTRY_CODE', 'KYC_STATUS'])
                cursor.execute("SELECT content_chunk FROM POLICIES_TEXT_BASE")
                policy_context = "\n".join([row[0] for row in cursor.fetchall()])
                cursor.close()

            # --- DISPLAY GRID SPLIT LAYOUT ---
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📊 Live Fraud Signals Detected")
                if not df_signals.empty:
                    st.dataframe(df_signals, use_container_width=True)
                    signal_context = ""
                    for _, row in df_signals.iterrows():
                        signal_context += f"Account {row['CUSTOMER_NAME']} ({row['ACCOUNT_ID']}) transferred {row['AMOUNT']} INR to country {row['COUNTRY_CODE']} with KYC Status: {row['KYC_STATUS']}.\n"
                else:
                    st.success("No critical high-risk signals found.")
                    signal_context = "No anomalous transaction parameters detected."

            with col2:
                st.subheader("📄 Generated Audit-Ready Report")
                
                prompt = f"""
                You are an expert compliance officer at an NBFC banking unit. Produce an official, audit-ready Suspicious Transaction Report (STR).
                
                STRUCTURED DATA SIGNALS:
                {signal_context}
                
                REGULATORY LAW BASELINES:
                {policy_context}
                
                Instructions: Identify compliance violations and cite the exact rule code (e.g. RULE-AML-01 or RULE-KYC-02). Format beautifully using markdown.
                """
                
                if not df_signals.empty:
                    # --- EXECUTE CORTEX SAFELY DEPENDING ON ENVIRONMENT ---
                    if env_mode == "NATIVE":
                        # Native path uses fast Snowpark compilation
                        report_df = conn.sql("SELECT CORTEX.COMPLETE('snowflake-arctic', %s)", params=[prompt]).to_pandas()
                        report_output = str(report_df.iloc[0, 0])
                    else:
                        # External Web App extracts data explicitly from raw tuples
                        cursor = conn.cursor()
                        cursor.execute("SELECT CORTEX.COMPLETE('snowflake-arctic', %s)", (prompt,))
                        res = cursor.fetchone()
                        report_output = str(res[0]) if res else "Error generating output text profile."
                        cursor.close()
                    
                    st.markdown(report_output)
                    st.download_button("📥 Export Report as TXT", data=report_output, file_name="STR_Audit_Report.txt")
                else:
                    st.info("Awaiting high-risk flags to generate report documentation.")

            if env_mode == "EXTERNAL":
                conn.close()

        except Exception as e:
            st.error(f"Error processing transaction pipeline: {str(e)}")
