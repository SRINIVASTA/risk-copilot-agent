# 🛡️ Risk, Fraud, and Regulatory Intelligence Copilot

A high-performance Python & Streamlit compliance agent engineered to trace an absolute, auditable line of custody for financial institutions. This application replaces manual compliance workflows by seamlessly bridging the gap between isolated transactional databases and dense regulatory frameworks.

---

## 🏛️ The 3-Step Solution Architecture

The application handles data ingestion and analysis through three distinct logical layers:

```text
[User Input Threshold]
         │
         ▼
1. SIGNAL DETECTION  ──► Joins Transaction & KYC Ledgers (Pandas SQL Logic)
         │
         ▼
2. EVIDENCE GATHERING ──► Semantic Search across RBI Master Directions (FAISS + Gemini)
         │
         ▼
3. AUDIT COMPLETION   ──► Generates formal Suspicious Transaction Reports (Gemini 2.5)
```

1. **Signal Detection (Structured Data):** Evaluates live relational tables (`transaction_ledger.csv` and `account_master.csv`) to immediately isolate high-risk transaction spikes, unverified account transfers, and outlier risk scores.
2. **Evidence Gathering (Unstructured RAG Data):** Uses a local vector database built with `faiss-cpu` and Google's production `gemini-embedding-001` to query and locate the exact compliance clauses broken within text-based policy documentation (`rbi_aml_directions.txt`).
3. **Audit-Ready Report Generation (Workflow Completion):** Fuses the transaction records with raw regulatory citations into a structured, strict markdown container using `gemini-2.5-flash`, preparing an official Suspicious Transaction Report (STR) for immediate export.

---

## 📂 Project Repository Structure

```text
risk-copilot-agent/
│
├── data/
│   ├── transaction_ledger.csv      # Mock transaction ledger dataset
│   └── account_master.csv          # Mock customer account master table
│
├── policies/
│   └── rbi_aml_directions.txt      # Unstructured RBI AML framework directions
│
├── app.py                          # Streamlit UX frontend dashboard wrapper
├── copilot_engine.py               # Vector database indexer & LLM pipeline logic
└── requirements.txt                # Production dependency registry
```

---

## 🚀 Execution & Setup Instructions

### Local Deployment
1. Install all system package prerequisites:
   ```bash
   pip install -r requirements.txt
   ```
2. Fire up the local Streamlit application server:
   ```bash
   streamlit run app.py
   ```
3. Input your secure **Google API Key** into the frontend sidebar mask component to unlock the system.

### Cloud Deployment
This project is fully tailored for one-click distribution on **Streamlit Community Cloud**. It features an explicit, self-healing runtime dependency injector block that synchronizes underlying libraries automatically upon code check-ins.
