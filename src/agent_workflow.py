import os
import snowflake.connector
from snowflake.cortex import Complete

def get_snowflake_connection():
    # Credentials are automatically injected by the CoCo CLI / Snowflake Environment
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database="HACKATHON_RISK_DB",
        schema="RISK_SCHEMA"
    )

def run_copilot_workflow(user_query):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    
    print(f"🔎 Step 1: Scanning Database for Structured Signals for query: '{user_query}'...")
    # Mocking standard deterministic parser based on user intent triggers
    signal_query = """
        SELECT t.transaction_id, t.account_id, a.customer_name, t.amount, t.country_code, a.kyc_status
        FROM TRANSACTION_LEDGER t
        JOIN ACCOUNT_MASTER a ON t.account_id = a.account_id
        WHERE t.amount > 5000000 AND a.kyc_status = 'PENDING';
    """
    cursor.execute(signal_query)
    flagged_records = cursor.fetchall()
    
    # Format the structured signals into readable text context
    signal_context = ""
    for rec in flagged_records:
        signal_context += f"Account {rec[1]} ({rec[2]}) transferred {rec[3]} INR to {rec[4]} with KYC Status: {rec[5]}. "

    print("📖 Step 2: Querying Cortex Knowledge Base for Regulatory Evidence...")
    evidence_query = "SELECT content_chunk FROM POLICIES_TEXT_BASE"
    cursor.execute(evidence_query)
    policy_rows = cursor.fetchall()
    policy_context = "\n".join([row[0] for row in policy_rows])

    print("📄 Step 3: Compiling Audit-Ready Regulatory Report via Cortex LLM...")
    prompt = f"""
    You are an expert enterprise compliance officer. Produce an official, audit-ready Suspicious Transaction Report (STR).
    
    STRUCTURED SIGNALS DETECTED:
    {signal_context}
    
    REGULATORY POLICY BASELINES:
    {policy_context}
    
    Instructions:
    1. Identify the compliance violation clearly.
    2. Reference the exact rule code (e.g. RULE-AML-01) from the policy baseline.
    3. Output an executive summary followed by explicit data fields.
    """
    
    # Execute the final compilation via native Snowflake Cortex function
    report_output = Complete("snowflake-arctic", prompt, session=conn)
    
    cursor.close()
    conn.close()
    
    return report_output

if __name__ == "__main__":
    # Sample question from a Compliance Officer
    sample_question = "Audit high-value transactions from unverified accounts this week."
    final_report = run_copilot_workflow(sample_question)
    
    print("\n==================== GENERATED COMPLIANCE REPORT ====================\n")
    print(final_report)
