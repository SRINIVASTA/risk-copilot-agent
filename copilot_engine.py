import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

class FraudCopilotEngine:
    def __init__(self):
        # 1. Load structured components from repository
        self.tx_df = pd.read_csv("data/transaction_ledger.csv")
        self.acc_df = pd.read_csv("data/account_master.csv")
        
        # Clean column names to prevent tracking bugs
        self.tx_df.columns = self.tx_df.columns.str.strip()
        self.acc_df.columns = self.acc_df.columns.str.strip()
        
        # 2. Extract unstructured policies
        with open("policies/rbi_aml_directions.txt", "r") as f:
            policy_content = f.read()
        
        chunks = [chunk.strip() for chunk in policy_content.split("\n\n") if chunk.strip()]
        
        # 3. Model Engine Setup
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        self.vector_db = FAISS.from_texts(chunks, self.embeddings)
        self.llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", temperature=0)

    def detect_signals(self, min_amount=5000000):
        """Step 1: Signal Detection (Structured Data) with complete regulatory alignment"""
        merged = pd.merge(self.tx_df, self.acc_df, on="ACCOUNT_ID")
        
        # Condition logic to capture high risk profiles and thresholds
        condition = (
            (merged["AMOUNT"] >= min_amount) | 
            (merged["RISK_SCORE"] > 70) |
            ((merged["KYC_STATUS"] == "Pending") & (merged["AMOUNT"] > 1000000)) |
            (merged["KYC_STATUS"] == "Suspended")
        )
        
        flagged_df = merged[condition].copy()
        return flagged_df

    def gather_evidence(self, flagged_df):
        """Step 2: Optimized Vector Search using batched distinct entity fields"""
        if flagged_df.empty:
            return "No systemic signals detected."
            
        evidence_pool = []
        
        # Optimize RAG performance by querying unique conditions
        unique_countries = flagged_df["COUNTRY_CODE"].unique()
        unique_statuses = flagged_df["KYC_STATUS"].unique()
        
        search_queries = [
            f"High value cross border transfer thresholds for countries {', '.join(unique_countries)}",
            f"KYC compliance limitations and transaction caps for status {', '.join(unique_statuses)}"
        ]
        
        for query in search_queries:
            docs = self.vector_db.similarity_search(query, k=3)
            for doc in docs:
                if doc.page_content not in evidence_pool:
                    evidence_pool.append(doc.page_content)
                    
        return "\n\n".join(evidence_pool)

    def generate_audit_report(self, flagged_df, evidence):
        """Step 3: Render data directly to clean Markdown structures before invoking LLM"""
        if flagged_df.empty:
            return "### No Anomalies Detected\nAll transaction patterns fall within standard operational bounds."

        # Format numerical fields within Python to guarantee a crisp table display
        table_rows = []
        for _, row in flagged_df.iterrows():
            formatted_amt = f"₹{row['AMOUNT']:,}"
            table_rows.append(
                f"| {row['TRANSACTION_ID']} | {row['ACCOUNT_ID']} | {row['CUSTOMER_NAME']} | "
                f"{formatted_amt} | {row['COUNTRY_CODE']} | {row['RISK_SCORE']} | {row['KYC_STATUS']} |"
            )
        markdown_ledger = "\n".join(table_rows)

        template = """
        You are an expert Risk, Fraud, and Regulatory Intelligence Officer.
        Generate an official, audit-ready Suspicious Transaction Report (STR) based on these data signals and regulatory evidence.
        
        DATA SIGNALS LEDGER:

        | Transaction ID | Account ID | Customer Name | Amount (INR) | Destination | Risk Score | KYC Status |
        | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
        {markdown_ledger}
        
        REGULATORY EVIDENCE BASE:
        {evidence}
        
        Use the following strict Markdown layout down to the exact header structure:
        
        # SUSPICIOUS TRANSACTION REPORT (STR)
        
        ## 📌 1. EXECUTIVE SUMMARY
        Provide a detailed executive summary here explaining the overall risk profile, total capital exposure, and systemic internal control vulnerabilities found.
        
        ## 📊 2. FLAGGED TRANSACTION LEDGER
        [Inject the rendered Markdown ledger here exactly as provided]
        
        ## 🔎 3. REGULATORY COMPLIANCE BREACH ANALYSIS
        * **Specific Section Broken:** [Identify explicit sections from evidence, e.g., Section 4.1 or 4.2]
        * **Evidence:** [Quote the direct policy text snippet that proves a breach occurred based on the data ledger]
        
        ## 💡 4. RECOMMENDED COMPLIANCE ACTIONS
        - [ ] Action 1
        - [ ] Action 2
        
        ---
        **Prepared By:** Risk & Compliance Copilot System  
        **Review Status:** ⚠️ PENDING HUMAN SIGN-OFF
        """
        
        prompt = PromptTemplate.from_template(template)
        chain = prompt | self.llm
        
        response = chain.invoke({
            "markdown_ledger": markdown_ledger, 
            "evidence": evidence
        })
        return response.content
