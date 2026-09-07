# Step 12 – Python ETL Pipeline Plan

## Purpose

The AI Vendor Comparison Dashboard relies on an Extract–Transform–Load (ETL) pipeline to convert raw vendor evaluation data into structured, standardized, and analytics-ready records stored in the SQL database.

To preserve architectural separation of concerns, the Python pipeline is responsible for **static data engineering, validation, internal weight re-normalization, and database ingestion**. Dynamic client persona re-weighting, real-time rankings, and recommendation generation are strictly decoupled from Python and executed downstream inside the Power BI DAX engine.

---

# ETL Pipeline Overview

```
External Configuration & Seeds
(categories, criteria, personas)
          │
          ▼
       Extract
(Read raw vendor evidence & research)
          │
          ▼
        Clean
(Validate, standardize, and enforce types)
          │
          ▼
      Normalize
(Map qualitative evidence to standard 1–5 scale)
          │
          ▼
   Prepare Scoring
(Handle missing data & re-normalize criterion weights)
          │
          ▼
        Load
(Populate relational SQL database)
          │
          ▼
 Power BI (DAX Dynamic Recalculation)
```

---

# ETL Pipeline Architecture

## Stage 1 – Extract

### Objective

Incorporate raw vendor evaluation data and qualitative evidence from source files into dataframes without applying business transformations.

### Data Sources

- Local tabular files (`data/raw/*.csv` or `.xlsx`) containing research notes, citations, and vendor attributes.

### Input

Raw tabular evidence files.

### Output

Raw pandas DataFrames.

---

## Stage 2 – Clean

### Objective

Enforce schema constraints, sanitize text fields, and ensure relational referential integrity before loading.

### Responsibilities

- Standardize vendor naming conventions (e.g., `GCP` / `google-cloud` → `Google Cloud Platform`).
- Strip whitespace and enforce character encoding standards.
- Validate that foreign key references exist in dimension tables (`VendorID`, `CriterionID`, `EvaluationDomainID`).
- Flag and quarantine invalid, duplicate, or unverified records.

### Input

Raw DataFrames.

### Output

Cleaned and validated DataFrames.

---

## Stage 3 – Normalize

### Objective

Ensure all vendor evaluation metrics adhere to the standardized evaluation rubric.

### Responsibilities

- Map input ratings directly to the project's uniform 1–5 integer scale.
- Assign deterministic confidence rankings (`High`, `Medium`, `Low`) based on evidence source tiers.
- Ensure data consistency across heterogeneous vendors.

### Input

Cleaned DataFrames.

### Output

Normalized DataFrames.

---

## Stage 4 – Prepare Scoring & Audit

### Objective

Format criterion-level scores and handle missing data adjustments prior to database ingestion.

### Responsibilities

- Calculate effective criterion weights per category if specific vendor criteria are marked `N/A` (redistributing missing weights proportionally across remaining criteria).
- Assemble score justifications, timestamps, evaluator metadata, and source citations.
- Construct the target entity payloads matching `VendorCriterionScore` and `Evidence` schemas.
- **Out of Scope for this stage:** Persona weighting and final vendor rankings (computed dynamically in Power BI).

### Input

Normalized DataFrames and criterion reference tables.

### Output

Analytics-ready DataFrames formatted for relational tables.

---

## Stage 5 – Load

### Objective

Perform idempotent insertion of structured datasets into the relational SQL database via SQLAlchemy.

### Responsibilities

- Maintain transactional integrity across parent-child inserts (`VendorEvaluation` → `VendorCriterionScore` → `Evidence`).
- Execute staging/upsert routines to prevent record duplication on repeated pipeline executions.
- Populate dimension tables (`Vendor`, `EvaluationCategory`, `EvaluationCriterion`, `ClientPersona`, `WeightProfile`, `CategoryWeight`).

### Input

Final processed DataFrames.

### Output

Populated relational SQL database.

---

# ETL Module Architecture

```text
etl/
├── __init__.py
├── extract.py      # Reads raw input files and research data
├── clean.py        # Validates data types, duplicates, and constraints
├── normalize.py    # Standardizes scores to the 1–5 scale
├── score.py        # Formats criterion-level scores and handles N/A redistributions
├── load.py         # Handles SQLAlchemy connections and batch loads
└── main.py         # Pipeline orchestrator executing stages sequentially


# ETL Flow Summary
| **Stage**           | **Input**                 | **Primary Operation**                                       | **Target SQL Entity**              |
| ------------------- | ------------------------- | ----------------------------------------------------------- | ---------------------------------- |
| **Extract**         | Raw vendor files (`.csv`) | Ingest raw research inputs                                  | N/A (In-memory)                    |
| **Clean**           | Raw DataFrames            | Standardize schema, strip characters, validate foreign keys | N/A (In-memory)                    |
| **Normalize**       | Clean DataFrames          | Verify 1–5 scoring scale and map confidence tiers           | N/A (In-memory)                    |
| **Prepare Scoring** | Normalized DataFrames     | Re-normalize N/A criterion weights; format justifications   | `VendorCriterionScore`, `Evidence` |
| **Load**            | Processed DataFrames      | Batch insert via SQLAlchemy                                 | All Database Tables                |


# Outcome

This ETL design establishes a modular and reusable data processing pipeline for the AI Vendor Comparison Dashboard. By separating extraction, cleaning, normalization, scoring, and loading into independent stages and externalizing business configuration, the system remains scalable, maintainable, and adaptable to future vendors, evaluation frameworks, and client requirements without requiring changes to the core application logic.
