import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

class FraudCopilotEngine:
    def __init__(self):
        # 1. Load data directly from your GitHub directory paths
        self.tx_df = pd.read_csv("data/transaction_ledger.csv")
        self.acc_df = pd.read_csv("data/account_master.csv")
        
        # 2. Load separate policy document
        with open("policies/rbi_aml_directions.txt", "r") as f:
            policy_content = f.read()
        
        chunks = [chunk.strip() for chunk in policy_content.split("\n\n") if chunk.strip()]
        
        # 3. Embedding and Engine Setup
        self.embeddings = OpenAIEmbeddings()
        self.vector_db = FAISS.from_texts(chunks, self.embeddings)
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)

    def detect_signals(self, min_amount=5000000):
        """Step 1: Signal Detection (Structured Data)"""
        merged = pd.merge(self.tx_df, self.acc_df, on="ACCOUNT_ID")
        # Flag if amount exceeds threshold OR has a dangerous risk score
        flagged = merged[(merged["AMOUNT"] >= min_amount) | (merged["RISK_SCORE"] > 70)]
        return flagged.to_dict(orient="records")

    def gather_evidence(self, flagged_records):
        """Step 2: Evidence Gathering (Unstructured RAG Data)"""
        evidence_pool = []
        for record in flagged_records:
            query = f"High value transfer of {record['AMOUNT']} to {record['COUNTRY_CODE']} with KYC status {record['KYC_STATUS']}"
            docs = self.vector_db.similarity_search(query, k=2)
            for doc in docs:
                if doc.page_content not in evidence_pool:
                    evidence_pool.append(doc.page_content)
        return "\n\n".join(evidence_pool)

    def generate_audit_report(self, signals, evidence):
        """Step 3: Audit Report Generation (The Workflow Completion)"""
        template = """
        You are an expert Risk, Fraud, and Regulatory Intelligence Officer.
        Generate an official, audit-ready Suspicious Transaction Report (STR) based on these data signals and regulatory evidence.
        
        DATA SIGNALS:
        {signals}
        
        REGULATORY EVIDENCE:
        {evidence}
        
        Use the following strict Markdown layout:
        
        # SUSPICIOUS TRANSACTION REPORT (STR)
        
        ## 📌 1. EXECUTIVE SUMMARY
        [Provide a summary of the compliance breaches found.]
        
        ## 📊 2. FLAGGED TRANSACTION LEDGER

        | Transaction ID | Account ID | Customer Name | Amount (INR) | Destination | Risk Score | KYC Status |
        | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
        [Populate Markdown table rows here using the data signals]
        
        ## 🔎 3. REGULATORY COMPLIANCE BREACH ANALYSIS
        * **Specific Section Broken:** [e.g., Section 4.1]
        * **Evidence:** [Quote text snippet matching back to the signal context]
        
        ## 💡 4. RECOMMENDED COMPLIANCE ACTIONS
        - [ ] Action 1
        - [ ] Action 2
        
        ---
        **Prepared By:** Risk & Compliance Copilot System  
        **Review Status:** ⚠️ PENDING HUMAN SIGN-OFF
        """
        prompt = PromptTemplate.from_template(template)
        chain = prompt | self.llm
        
        response = chain.invoke({"signals": str(signals), "evidence": evidence})
        return response.content
