# 🛡️ Risk, Fraud, and Regulatory Intelligence Copilot

A high-performance Python & Streamlit compliance agent engineered to trace an absolute, auditable line of custody for financial institutions. This application replaces manual compliance workflows by seamlessly bridging the gap between isolated transactional databases, interactive data analytics, and dense regulatory frameworks.

---

## 🏛️ The 3-Step Solution Architecture

The application handles data ingestion and analysis through three distinct logical layers to ensure absolute determinism and zero hallucination of mathematical metrics:

```text
[User Input Threshold / Control Panel Interaction]
                       │
                       ▼
1. SIGNAL DETECTION  ──► Calculates Live RBI Customer Risk Categorization (CRC) Matrix
                       │ (Deterministic Pandas calculations on raw, unscored transaction records)
                       ▼
2. EVIDENCE GATHERING ──► Semantic Search across RBI Master Directions (FAISS + Gemini)
                       │
                       ▼
3. AUDIT COMPLETION   ──► Generates formal Suspicious Transaction Reports (Gemini 2.5)
```

1. **Signal Detection (Structured Data & Interactive Analytics):** Evaluates live relational tables (`transaction_ledger.csv` and `account_master.csv`). It completely strips away pre-calculated score assumptions to compute a brand new **RBI-aligned Customer Risk Categorization (CRC) score** directly in memory. It immediately isolates high-risk transaction spikes, pending account transfers, and banned suspended activity, rendering high-impact KPI scorecards and an interactive **Plotly** chart.
2. **Evidence Gathering (Unstructured RAG Data):** Uses a local vector database built with `faiss-cpu` and Google's production `gemini-embedding-001` to query and locate the exact compliance clauses broken within text-based policy documentation (`rbi_aml_directions.txt`).
3. **Audit-Ready Report Generation (Workflow Completion):** Fuses the transaction records with raw regulatory citations into a structured, strict markdown container using `gemini-2.5-flash`, preparing an official Suspicious Transaction Report (STR) for immediate export.

---

## 🧮 Algorithmic Customer Risk Scoring Parameters

The system determines risk index values dynamically using a code-based, multi-factor additive matrix aligned with actual **Reserve Bank of India (RBI) KYC Master Directions** and **Prevention of Money Laundering Act (PMLA)** rules:

*   **Jurisdiction Vector (Max 40 Pts):** Automatically flags high-risk offshore corridors (Cayman Islands `[KY]`, Switzerland `[CH]` = 40 pts) and high-velocity transit clearing points (UAE `[AE]`, Hong Kong `[HK]`, Singapore `[SG]` = 20 pts).
*   **Onboarding Identity Profile (Max 55 Pts):** Applies heavy penalties for critical regulatory statuses (`Suspended` = 55 pts, `Pending` = 35 pts, `Verified` = 10 pts).
*   **Capital Scale Thresholds (Max 25 Pts):** Scales based on transaction tranches relative to institutional reporting lines (≥ ₹5,000,000 = 25 pts, ≥ ₹1,000,000 = 15 pts).
*   *The final composite index value is dynamically clamped between a logical `0` and `100` boundary.*

---

## 🛠️ Enterprise Tech Stack

*   **Frontend UI & UX:** Streamlit, Plotly (Dynamic Risk Charts)
*   **Vector Engine & Ingestion:** FAISS (`faiss-cpu`), LangChain native data processors
*   **Large Language Models:** Google `gemini-2.5-flash` (Reporting Engine), `gemini-embedding-001` (Embeddings)
*   **Data Processing:** Pandas (Deterministic Financial Log Analytics & Live CRC Calculation Matrix)

---

## 📂 Project Repository Structure

```text
risk-copilot-agent/
│
├── data/
│   ├── transaction_ledger.csv      # Raw transaction database ledger (unscored)
│   └── account_master.csv          # Standard customer account master profiles
│
├── policies/
│   └── rbi_aml_directions.txt      # Unstructured RBI AML framework directions
│
├── app.py                          # Streamlit UX frontend dashboard wrapper with Plotly charts
├── copilot_engine.py               # Vector database indexer & Live CRC risk-scoring engine
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
*   **Zero Pre-Scored Reliance:** Transactions are scored entirely downstream based on mathematical profiles in Python before compiling reporting objects, preventing stale tracking parameters.
*   **Deterministic Safety:** The engine processes all transaction sums, aggregations, and velocity rules natively in Python before passing summaries to the LLM. 
*   **No Hallucinations:** Every line item generated in the final Suspicious Transaction Report (STR) includes direct string citations from `rbi_aml_directions.txt` and direct hash references from `transaction_ledger.csv`.
