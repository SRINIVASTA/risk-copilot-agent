# Cortex Risk Copilot: Automated Regulatory Intelligence & Operational Remediation Engine

An automated Risk, Fraud, and AML Regulatory Intelligence terminal engineered natively for secure enterprise operations within an **Azure Cloud Environment**. The system processes high-density financial transaction logs from two explicit local data ledgers against dense regulatory compliance frameworks (specifically mapping **Sections 4.1, 4.2, and 7.3 of the Master Anti-Money Laundering Directions**). 

By separating structured behavioral metrics from unstructured generative policy synthesis, the platform establishes a strict, auditable Line-of-Custody (**Signal ➔ Evidence ➔ Action**) to spot complex, multi-leg velocity structuring maneuvers (layering) across a 100-row historical transaction ledger.

---

## 🏛️ System Architecture Diagram

```text
========================================================================================
                      CORTEX RISK COPILOT SYSTEM ARCHITECTURE
========================================================================================

    [ USER INTERFACE LAYER ]
    ┌──────────────────────────────────────────────────────────────────────────────┐
    │                        Streamlit Application Workspace                       │
    │  (📊 Dashboard Terminal  |  💬 CoCo Chat Room  |  🛠️ Remediation Console)    │
    └─────────────────────────────────┬────────────────────────────────────────────┘
                                      │ (Local Data Processing Streams)
                                      ▼
    [ ANALYTICAL PROCESSING LAYER ]
    ┌──────────────────────────────────────────────────────────────────────────────┐
    │                            Cloud Compute Engine                              │
    │  • Deterministic Analytical Ingestion Filters                                │
    │  • 48-Hour Rolling Window Matrix Math (Sec 7.3 Velocity Tracking via Pandas) │
    │  • ReportLab Multi-Page PDF Generation Sub-Engine (In-Memory Stream)         │
    └─────────────────────────────────┬────────────────────────────────────────────┘
                                      │ (Native Internal Functions)
                                      ▼
    [ AI & SEMANTIC KNOWLEDGE LAYER ]
    ┌──────────────────────────────────────────────────────────────────────────────┐
    │                            Cortex AI Core Engine                             │
    │  ┌────────────────────────────────────┐ ┌──────────────────────────────────┐ │
    │  │       Semantic Search Service      │ │       Serverless LLM Service     │ │
    │  │  (Integrated Local Vector Index)   │ │  (Azure Perimeter gpt-4o/Gemini) │ │
    │  └────────────────────────────────────┘ └──────────────────────────────────┘ │
    └─────────────────────────────────┬────────────────────────────────────────────┘
                                      │ (Secure File Engine Mappings)
                                      ▼
    [ ENTERPRISE SECURE STORAGE LAYER ]
    ┌──────────────────────────────────────────────────────────────────────────────┐
    │                Local Flat-File Data Store (Exactly 2 CSVs)                   │
    │        ┌──────────────────────────────┐ ┌──────────────────────────────┐     │
    │        │      account_master.csv      │ │   transaction_ledger.csv     │     │
    │        │      (Profile Vectors)       │ │      (100 Telemetries)       │     │
    │        └──────────────────────────────┘ └──────────────────────────────┘     │
    │  ┌────────────────────────────────────────────────────────────────────────┐ │
    │  │                         rbi_aml_directions.txt                         │ │
    │  │               (Sections 4.1, 4.2, 7.3 Flat-Text Rules)                 │ │
    │  └────────────────────────────────────────────────────────────────────────┘ │
    └==============================================================================┘
                 [ SECURE SYSTEM BOUNDARY: HOSTED ENTIRELY ON AZURE ]
```

---

## 🌟 Key Technical Innovations

1. **Zero-Hallucination Pipeline Geometry:** Prevents LLM mathematical inaccuracies by running data through structured pandas filters first. Rolling 48-hour window velocity matches (**Section 7.3**) and limit tracking blocks (**Section 4.2**) are computed with absolute structural calculation precision before any prompt generation occurs.
2. **Deterministic Line-of-Custody:** Maps raw ledger anomalies back to active compliance rule text fragments in a transparent, 3-step design: **Signal Ingestion ➔ Vector Evidence Mapping ➔ In-Memory Multi-page PDF Report Generation**.
3. **Closed-Loop Active Mitigation:** Moves beyond passive visual monitoring dashboards. The **Remediation & Actions Console** allows compliance officers to enforce tactical kill-switches (freezing outbound privileges, stepping up KYC levels), which dynamically updates account state vectors directly in memory loops.
4. **Data Privacy Isolation:** The entire application runs inside a protected Azure cloud boundary. All data lookups, contextual search queries, and prompt reasoning arrays stay completely isolated within the secure enterprise file workspace.

---

## 📁 Repository File Layout & Datasets

The application relies on a streamlined local file structure located inside the project directories to feed the operational metrics engine:

### 1. `policies/rbi_aml_directions.txt`
The central compliance knowledge text base. Sections are explicitly separated by double blank line spacings to preserve indexing boundaries:
```text
Section 4.1: High-Value Cross-Border Transfers & PEP Multipliers
Any single cross-border transaction exceeding INR 5,000,000 (₹50 Lakhs) to high-risk offshore jurisdictions (including Cayman Islands [KY], Switzerland [CH]) must be flagged immediately for enhanced due diligence (EDD). If the underlying account is flagged as a Politically Exposed Person (PEP), mandatory senior management sign-off and explicit source of wealth/funds validation are required prior to final settlement, regardless of the transaction amount.

Section 4.2: KYC Compliance Thresholds & Restricted Accounts
Entities operating with a 'Pending' KYC onboarding status are strictly restricted from executing outbound international wire transfers exceeding an operational threshold of INR 1,000,000 (₹10 Lakhs). Any operational volume exceeding this cap constitutes a high-risk compliance breach. Politically Exposed Persons (PEPs) are prohibited from operating under a 'Pending' KYC state for cross-border routes; any transaction initiated by an unverified PEP profile triggers an automatic global system lock.

Section 7.3: Structural Anomalies & Velocity Structuring
Multiple high-value transfers initiated by the same corporate or individual account within a rolling 48-hour window to disparate offshore entities indicate potential velocity structuring (layering activities) and require an immediate Suspicious Transaction Report (STR) filing with FIU-IND. Systemic alerts compile cumulative transaction velocities to prevent evasion of transaction reporting limits.
```

### 2. `data/account_master.csv`
Defines onboarding parameters and risk markers for client accounts:
```csv
ACCOUNT_ID,CUSTOMER_NAME,KYC_STATUS,IS_PEP,CUSTOMER_TYPE
ACC_991,Alpha Global Holdings,Pending,FALSE,Corporate
ACC_101,Srinivasta Enterprises,Verified,TRUE,Corporate
ACC_202,Anita Sharma,Pending,TRUE,Individual
ACC_303,Zeta Logistics,Suspended,FALSE,Corporate
ACC_808,Nexus Infotech,Verified,FALSE,Corporate
ACC_606,Sigma Ventures,Pending,FALSE,Corporate
ACC_445,Omega Trade Corp,Verified,FALSE,Corporate
```

### 3. `data/transaction_ledger.csv`
A high-density data register housing exactly **100 precision mock transaction items** carefully configured to trip Sections 4.1, 4.2, and 7.3 analytics.

---

## 🚀 Environment Quick Start & Deployment

### 1. Installation of Dependencies
Clone this repository to your target secure infrastructure node and run the package synchronization command via your terminal window:

```bash
pip install streamlit pandas plotly reportlab langchain-core langchain-community faiss-cpu
```

### 2. Execution of Dashboard App
Ensure your `account_master.csv` and `transaction_ledger.csv` files are saved inside the `data/` folder, and your `rbi_aml_directions.txt` is inside `policies/`. Launch the dashboard terminal workspace using:

```bash
streamlit run app.py
```

---

## 🎛️ Detailed Workspace Tab Breakdown

* **Tab 1: 📊 Operational Dashboard:** Features live aggregate metrics (Total Exposure, Signal Counts, Network Risk Factors) alongside interactive Plotly transaction map charts. Pushing the audit button triggers the complete threat discovery flow and generates a downloadable corporate **Official PDF Compliance Report**.
* **Tab 2: 💬 Conversational CoCo Copilot:** An interactive, conversational context workspace allowing natural language exploration. Compliance officers can query specific velocity tracking chains or ask for instant policy justifications regarding active high-risk clients.
* **Tab 3: 📁 Account Profile Directory Lookup:** Provides a 360-degree deep dive window into individual corporate data layers, displaying current onboarding statuses, political indicator badges, and complete chronological transaction logs.
* **Tab 4: 🛠️ Remediation & Actions Console:** The platform's strategic intervention bridge. Includes interactive drop-down menus to isolate profiles like `ACC_991`, execute immediate outbound financial overrides, toggle systemic rule sets on the fly, and download aggregated batch packages configured for regulatory reporting structures.
