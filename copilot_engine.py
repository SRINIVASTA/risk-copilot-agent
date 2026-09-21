# Save this file as: copilot_engine.py
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

class FraudCopilotEngine:
    def __init__(self):
        # 1. Load data tables from repository
        self.tx_df = pd.read_csv("data/transaction_ledger.csv")
        self.acc_df = pd.read_csv("data/account_master.csv")
        
        # Clean header column fields
        self.tx_df.columns = self.tx_df.columns.str.strip()
        self.acc_df.columns = self.acc_df.columns.str.strip()
        
        # Drop pre-existing risk columns to compute fresh from the RBI framework
        if "RISK_SCORE" in self.tx_df.columns:
            self.tx_df = self.tx_df.drop(columns=["RISK_SCORE"])
        
        # 2. Load policy files for the vector database
        with open("policies/rbi_aml_directions.txt", "r") as f:
            policy_content = f.read()
        
        chunks = [chunk.strip() for chunk in policy_content.split("\n\n") if chunk.strip()]
        
        # 3. Model Engine Infrastructure
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        self.vector_db = FAISS.from_texts(chunks, self.embeddings)
        self.llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", temperature=0)

    def _calculate_live_risk_score(self, df):
        """
        Calculates risk matrices adhering strictly to RBI-mandated 
        Customer Risk Categorization (CRC) profiles, now with PEP monitoring.
        """
        scores = []
        for _, row in df.iterrows():
            score = 0
            
            # Dimension 1: FATF & Offshore Jurisdiction Profile
            if row["COUNTRY_CODE"] in ["KY", "CH"]:  # Cayman Islands / Switzerland Tax Havens
                score += 40
            elif row["COUNTRY_CODE"] in ["AE", "HK", "SG"]:  # High-volume clearing hubs
                score += 20
            else:
                score += 5
                
            # Dimension 2: RBI Customer Acceptance and KYC Status Onboarding Matrix
            if row["KYC_STATUS"] == "Suspended":
                score += 55  # Critical Violation
            elif row["KYC_STATUS"] == "Pending":
                score += 35  # Restricted Account
            else:
                score += 10  # Standard Verified Base
                
            # Dimension 3: Capital Exposure Banding (RBI High-Value Reporting Caps)
            if row["AMOUNT"] >= 5000000:
                score += 25  # ₹50 Lakh Threshold Breached
            elif row["AMOUNT"] >= 1000000:
                score += 15  # ₹10 Lakh Threshold Breached
            else:
                score += 5

            # Dimension 4: Politically Exposed Person (PEP) Flag Check
            if str(row["IS_PEP"]).strip().lower() == "true":
                score += 30  # High-impact political exposure multiplier
                
            # Lock parameters inside normal 0-100 system limits
            scores.append(min(score, 100))
            
        return scores

    def detect_signals(self, min_amount=5000000):
        """Step 1: Signal Detection aligned with RBI Anti-Money Laundering Thresholds"""
        # Execute table joins
        merged = pd.merge(self.tx_df, self.acc_df, on="ACCOUNT_ID")
        
        # Feed live calculated metrics back into DataFrame
        merged["RISK_SCORE"] = self._calculate_live_risk_score(merged)
        
        # Trigger hard alarms based on official compliance filters (including PEP overrides)
        condition = (
            (merged["AMOUNT"] >= min_amount) | 
            (merged["RISK_SCORE"] >= 70) | 
            ((merged["KYC_STATUS"] == "Pending") & (merged["AMOUNT"] > 1000000)) | 
            (merged["KYC_STATUS"] == "Suspended") |
            (merged["IS_PEP"] == True)
        )
        
        flagged_df = merged[condition].copy()
        return flagged_df

    def gather_evidence(self, flagged_df):
        """Step 2: Optimized Context Search mapping back to rule documents"""
        if flagged_df.empty:
            return "No systemic compliance violations detected."
            
        evidence_pool = []
        unique_countries = flagged_df["COUNTRY_CODE"].unique()
        unique_statuses = flagged_df["KYC_STATUS"].unique()
        
        search_queries = [
            f"RBI regulations for wire transfers to jurisdictions: {', '.join(unique_countries)}",
            f"Official Master Direction restrictions on account onboarding status: {', '.join(unique_statuses)}",
            "Enhanced due diligence requirements for Politically Exposed Persons PEP profiles"
        ]
        
        for query in search_queries:
            docs = self.vector_db.similarity_search(query, k=3)
            for doc in docs:
                if doc.page_content not in evidence_pool:
                    evidence_pool.append(doc.page_content)
                    
        return "\n\n".join(evidence_pool)

    def generate_audit_report(self, flagged_df, evidence):
        """Step 3: Compile final, regulatory-compliant STR document matching data to legal rules"""
        if flagged_df.empty:
            return "### Compliance Verified\nAll entries comply completely with PMLA tracking layers."

        table_rows = []
        for _, row in flagged_df.iterrows():
            formatted_amt = f"₹{row['AMOUNT']:,}"
            pep_status = "🔴 YES" if row['IS_PEP'] else "🟢 NO"
            table_rows.append(
                f"| {row['TRANSACTION_ID']} | {row['ACCOUNT_ID']} | {row['CUSTOMER_NAME']} | "
                f"{formatted_amt} | {row['COUNTRY_CODE']} | {int(row['RISK_SCORE'])} | {row['KYC_STATUS']} | {pep_status} |"
            )
        markdown_ledger = "\n".join(table_rows)

        template = """
        You are an expert Chief Compliance and AML Reporting Officer operating under RBI guidelines.
        Generate an official Suspicious Transaction Report (STR) adhering strictly to FIU-IND submission conventions.
        
        DATA SIGNALS LEDGER:

        | Transaction ID | Account ID | Customer Name | Amount (INR) | Destination | Risk Score | KYC Status | PEP Flag |
        | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
        {markdown_ledger}
        
        REGULATORY EVIDENCE BASE:
        {evidence}
        
        Use the following strict Markdown layout down to the exact header structure:
        
        # SUSPICIOUS TRANSACTION REPORT (STR)
        
        ## 📌 1. EXECUTIVE SUMMARY
        Provide a legal executive summary here explaining the overall risk profile, total capital exposure, and systemic internal control vulnerabilities found under PMLA and RBI directives. Explicitly mention if any Politically Exposed Persons (PEPs) triggered alerts.
        
        ## 📊 2. FLAGGED TRANSACTION LEDGER
        [Inject the rendered Markdown ledger here exactly as provided]
        
        ## 🔎 3. REGULATORY COMPLIANCE BREACH ANALYSIS
        * **Specific Section Broken:** [Identify explicit sections from evidence, e.g., RBI Section 4.1 or 4.2]
        * **Evidence:** [Quote the policy text snippet that proves a breach occurred based on the data ledger parameters]
        
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
