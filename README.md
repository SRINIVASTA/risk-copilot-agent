# 🛡️ Risk, Fraud, and Regulatory Intelligence Copilot

A high-performance Python & Streamlit compliance agent engineered to trace an absolute, auditable line of custody for financial institutions. This application replaces manual compliance workflows by seamlessly bridging the gap between isolated transactional databases, interactive data analytics, and dense regulatory frameworks.

---

## 🏛️ The 3-Step Solution Architecture

The application handles data ingestion and analysis through three distinct logical layers to ensure absolute determinism and zero hallucination of mathematical metrics:

```text
[User Input Threshold / Natural Language Query]
                       │
                       ▼
1. SIGNAL DETECTION  ──► Joins Transaction & KYC Ledgers (Deterministic Pandas/SQL)
                       │
                       ▼
2. EVIDENCE GATHERING ──► Semantic Search across RBI Master Directions (FAISS + Gemini)
                       │
                       ▼
3. AUDIT COMPLETION   ──► Generates formal Suspicious Transaction Reports (Gemini 2.5)
```

1. **Signal Detection (Structured Data & Interactive Analytics):** Evaluates live relational tables (`transaction_ledger.csv` and `account_master.csv`) to immediately isolate high-risk transaction spikes, unverified account transfers, and outlier risk scores. Renders high-impact KPI scorecards and an interactive **Plotly** data visualization showing capital exposure colored by risk intensity.
2. **Evidence Gathering (Unstructured RAG Data):** Uses a local vector database built with `faiss-cpu` and Google's production `gemini-embedding-001` to query and locate the exact compliance clauses broken within text-based policy documentation (`rbi_aml_directions.txt`).
3. **Audit-Ready Report Generation (Workflow Completion):** Fuses the transaction records with raw regulatory citations into a structured, strict markdown container using `gemini-2.5-flash`, preparing an official Suspicious Transaction Report (STR) for immediate export.

---

## 🛠️ Enterprise Tech Stack

*   **Frontend UI & UX:** Streamlit, Plotly (Dynamic Risk Charts)
*   **Vector Engine & Ingestion:** FAISS (`faiss-cpu`), LlamaIndex / LangChain native data splitters
*   **Large Language Models:** Google `gemini-2.5-flash` (Reporting Engine), `gemini-embedding-001` (Embeddings)
*   **Data Processing:** Pandas (Deterministic Financial Log Aggregations)

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
├── app.py                          # Streamlit UX frontend dashboard wrapper with Plotly charts
├── copilot_engine.py               # Vector database indexer & LLM pipeline logic
└── requirements.txt                # Production dependency registry
```

---

## 🚀 Execution & Setup Instructions

### Local Deployment

1. **Clone the Repository & Navigate:**
   ```bash
   git clone https://github.com
   cd risk-copilot-agent
   ```

2. **Install all system package prerequisites:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Fire up the local Streamlit application server:**
   ```bash
   streamlit run app.py
   ```

4. **Authentication:**
   Input your secure **Google API Key** into the frontend sidebar mask component to unlock the system.

### Cloud Deployment
This project is fully tailored for one-click distribution on **Streamlit Community Cloud**. It features an explicit, self-healing runtime dependency injector block that synchronizes underlying libraries (including Plotly and Google GenAI) automatically upon code check-ins.

---

## 🔒 Governance & Auditability Guardrails
*   **Deterministic Safety:** The engine processes all transaction sums, aggregations, and velocity rules natively in Python before passing summaries to the LLM. 
*   **No Hallucinations:** Every line item generated in the final Suspicious Transaction Report (STR) includes direct string citations from `rbi_aml_directions.txt` and direct hash references from `transaction_ledger.csv`.
