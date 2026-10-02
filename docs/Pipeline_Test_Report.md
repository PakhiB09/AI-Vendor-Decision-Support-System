# Step 37 – End-to-End System ETL & Pipeline Refresh Test Log

## Executive Summary
This report documents the verification of the end-to-end data processing pipeline for the **Enterprise Agentic AI Decision-Support System**.

The goal of Step 37 is to confirm that any modification made to score assignments or evaluation evidence flows seamlessly from configuration files, through Python data transformations and quality assertions, into the MySQL relational database, and ultimately reflects inside the Power BI dashboard via DAX measure recalculations.

---

## Data Pipeline Architecture
The system architecture follows a decoupled, multi-layered data flow:

```text
[config/score_assignments.csv] ──► [etl/assign_scores.py] ──► [data/processed/final_dataset.csv]
                                                                        │
[Power BI Dashboard Refresh]  ◄── [MySQL Database] ◄── [etl/load_database.py]

- **Immutable Raw Research (`data/raw/*.csv`):** Stores qualitative evidence summaries, source URLs, and confidence ratings.
- **Scoring Assignments (`config/score_assignments.csv`):** Controls the assigned numeric score ($1.0\text{--}5.0$) and justifications per vendor-criterion pair.
- **Relational Store (`MySQL: vendor_decision_support`):** Houses normalized tables (`vendors`, `criteria`, `evaluations`, `personas`, `persona_weights`).
- **Analytics Layer (`Power BI`):** Executes dynamic category re-weighting using DAX measures (`Total Weighted Score`, `Score Delta to Leader`, `Vendor Rank`).

## Test Execution & Verification Protocol

### Test Case: Modifying a Vendor Capability Score

- **Target Entity:** `Signzy` | **Criterion:** `Governance & Security (C14)`

- **Baseline State:** `Assigned Score = 3.0` | `Evaluation Status = Evaluated`

  [cite: 13, 14]

- **Test Modification:** Updated `config/score_assignments.csv` to increase `Assigned Score = 5.0` with justification *"Upgraded security score following enterprise compliance certification audit."*

  [cite: 13, 14]

## Pipeline Test Execution Results

| **Stage** | **Execution Command / Script** | **Primary Action** | **Validation Outcome** | **Status** |
|---|---|---|---|---|
| **1. Source Configuration** | `config/score_assignments.csv` | Edited numeric score from 3.0 to 5.0 | Configuration saved with updated justification | **PASS** |
| **2. Score Assignment** | `python etl/assign_scores.py` | Merged research evidence with rubric rules | Validated 136 records against `scoring_rubric.json` | **PASS** |
| **3. Final Dataset Gen** | `python etl/generate_final_dataset.py` | Assigned stable surrogate keys (E0001–E0136) | Generated `final_vendor_evaluation_dataset.csv` | **PASS** |
| **4. Data Quality Audit** | `python etl/validate_data.py` | Programmatic assertions check | Passed all 15 structural and completeness checks | **PASS** |
| **5. Database Reload** | `python etl/load_database.py` | Executed idempotent MySQL reload | Updated `evaluations` table in MySQL instance | **PASS** |
| **6. SQL Verification** | `python etl/validate_database.py` | Verified referential integrity & score bounds | Confirmed Signzy C14 score updated to 5.0 in SQL | **PASS** |
| **7. Power BI Refresh** | Power BI `Refresh` Ribbon Button | Triggered import data model refresh | DAX measures updated total score & deltas automatically | **PASS** |

## SQL Database Verification Query Output

### SQL Query

```sql
SELECT 
    v.vendor_name,
    e.criterion_id,
    e.assigned_score,
    e.evaluation_status,
    e.score_justification
FROM evaluations e
JOIN vendors v ON e.vendor_id = v.vendor_id
WHERE v.vendor_name = 'Signzy' AND e.criterion_id = 'C14';