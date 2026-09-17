import streamlit as st
import pandas as pd
import os
import snowflake.connector

# 1. Dashboard Layout & Typography Configuration
st.set_page_config(page_title="Risk & AML Copilot", layout="wide")
st.title("🏦 Risk, Fraud & Regulatory Intelligence Copilot")
st.caption("Snowflake CoCo CLI Hackathon — GCC Edition 2026")

# 2. Secure External Connection Channel (Bypasses Snowpark completely)
def get_clean_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database="HACKATHON_RISK_DB",
        schema="RISK_SCHEMA"
    )

# 3. Input Query Text Area Component
user_query = st.text_input(
    "Enter your regulatory query or compliance objective:",
    value="Audit high-value transactions from unverified accounts this week"
)

if user_query:
    with st.spinner("🕵️‍♂️ Fetching transactional signals and generating regulatory audit trail..."):
        try:
            # Open direct cursor channel
            conn = get_clean_connection()
            cursor = conn.cursor()
            
            # --- PHASE 1: SIGNAL DETECTION ---
            signal_sql = """
                SELECT t.transaction_id, t.account_id, a.customer_name, t.amount, t.country_code, a.kyc_status
                FROM TRANSACTION_LEDGER t
                JOIN ACCOUNT_MASTER a ON t.account_id = a.account_id
                WHERE t.amount > 5000000 AND a.kyc_status = 'PENDING';
            """
            cursor.execute(signal_sql)
            records = cursor.fetchall()
            df_signals = pd.DataFrame(records, columns=['TRANSACTION_ID', 'ACCOUNT_ID', 'CUSTOMER_NAME', 'AMOUNT', 'COUNTRY_CODE', 'KYC_STATUS'])
            
            # --- PHASE 2: EVIDENCE GATHERING ---
            cursor.execute("SELECT content_chunk FROM POLICIES_TEXT_BASE")
            policy_rows = cursor.fetchall()
            policy_context = "\n".join([str(row[0]) for row in policy_rows])

            # --- RENDER DASHBOARD COLUMNS ---
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📊 Live Fraud Signals Detected")
                if not df_signals.empty:
                    st.dataframe(df_signals, use_container_width=True)
                    
                    signal_context = ""
                    for _, row in df_signals.iterrows():
                        signal_context += f"Account {row['CUSTOMER_NAME']} ({row['ACCOUNT_ID']}) transferred {row['AMOUNT']} INR to destination {row['COUNTRY_CODE']} with KYC Status: {row['KYC_STATUS']}.\n"
                else:
                    st.success("No anomalous high-risk variances surfaced.")
                    signal_context = "No suspicious transaction parameters detected."

            with col2:
                st.subheader("📄 Generated Audit-Ready Report")
                
                # Rigid bounding context box to isolate LLM targets
                prompt = f"""
                You are an expert compliance investigator at a banking entity. Write an official Suspicious Transaction Report (STR).
                
                EVIDENCE DATA SIGNALS:
                {signal_context}
                
                REGULATORY INSTRUCTIONS:
                {policy_context}
                
                Instructions: Explicitly call out the exact rule code (e.g. RULE-AML-01) that was breached based on the numbers. Format beautifully using clean markdown text layout. Do not summarize this instruction sheet.
                """
                
                if not df_signals.empty:
                    # --- PHASE 3: CORTEX INFERENCE VIA STRING QUERY ---
                    # Calling the API endpoint directly via SQL prevents the 'No Default Session' exception!
                    cursor.execute("SELECT CORTEX.COMPLETE('snowflake-arctic', %s)", (prompt,))
                    query_result = cursor.fetchone()
                    
                    # Safely isolate the inner string from the database object tuple array
                    if query_result and len(query_result) > 0:
                        report_output = str(query_result[0])
                    else:
                        report_output = "⚠️ Error: The database warehouse failed to return a valid response layout context."
                    
                    # Display response text element layout
                    st.markdown(report_output)
                    st.download_button("📥 Export Report as TXT File", data=report_output, file_name="STR_Audit_Report.txt")
                else:
                    st.info("Awaiting high-risk flags to generate report documentation.")

            cursor.close()
            conn.close()

        except Exception as e:
            st.error(f"Error processing transaction pipeline: {str(e)}")
