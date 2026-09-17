-- Create Database Architecture
CREATE DATABASE IF NOT EXISTS HACKATHON_RISK_DB;
USE DATABASE HACKATHON_RISK_DB;
CREATE SCHEMA IF NOT EXISTS RISK_SCHEMA;
USE SCHEMA RISK_SCHEMA;

-- Create Structured Data Tables
CREATE OR REPLACE TABLE TRANSACTION_LEDGER (
    transaction_id VARCHAR,
    account_id VARCHAR,
    amount NUMBER,
    country_code VARCHAR,
    timestamp TIMESTAMP,
    tx_type VARCHAR,
    risk_score FLOAT
);

CREATE OR REPLACE TABLE ACCOUNT_MASTER (
    account_id VARCHAR,
    customer_name VARCHAR,
    kyc_status VARCHAR,
    customer_type VARCHAR,
    risk_category VARCHAR
);

-- Internal Stage to hold Unstructured Policy Docs
CREATE OR REPLACE STAGE compliance_policy_stage
    DIRECTORY = (ENABLE = TRUE)
    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

-- Create Cortex Search Index over the text files (Simulated here via a table for execution ease)
CREATE OR REPLACE TABLE POLICIES_TEXT_BASE (
    content_chunk VARCHAR,
    metadata_rule_id VARCHAR
);

INSERT INTO POLICIES_TEXT_BASE VALUES 
('[RULE-AML-01] High-Value Offshore Transfers: Any single outward remittance exceeding INR 5,000,000 to high-risk tax jurisdictions (including Cyprus [CY], Cayman Islands [KY]) must be flagged.', 'RULE-AML-01'),
('[RULE-KYC-02] Account Governance: Corporate accounts operating with a PENDING KYC status are restricted from executing cross-border wire transfers exceeding INR 1,000,000.', 'RULE-KYC-02');
