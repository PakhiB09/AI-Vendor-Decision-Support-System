# Step 38A – System Architecture Overview

## Overview
The Enterprise Agentic AI Decision-Support System is built on a decoupled, six-layer architecture that separates qualitative evidence collection, Python ETL data transformations[cite: 1, 8], MySQL database storage[cite: 1, 8], dynamic DAX scoring, and executive Power BI visualizations[cite: 1, 8].

---

## Architectural Layers & Component Responsibilities

```text
[Raw Qualitative Data] ──► [Python ETL Pipeline] ──► [MySQL Database] ──► [Power BI Semantic Model] ──► [DAX Re-Weighting Engine]
(data/raw/*.csv)            (etl/*.py)               (evaluations DB)     (Import Mode Star Schema)    (Dynamic Recommendations)

### 1. Data Collection Layer

- **Sources:** Official product documentation, developer APIs, trust security whitepapers, and analyst benchmarks.
- **Storage:** Immutable raw CSV files stored under `data/raw/*.csv` containing qualitative evidence notes and URLs.

### 2. Data Processing & Pipeline Layer (Python)

- **Scripts:** `etl/clean_data.py`, `etl/validate_data.py`, `etl/assign_scores.py`, `etl/generate_final_dataset.py`.
- **Responsibilities:** Standardizes text formatting, validates schema assertions, merges scoring rules from `config/score_assignments.csv`, and generates surrogate IDs (`V001`–`V008`, `C01`–`C17`, `E0001`–`E0136`).

### 3. Relational Storage Layer (MySQL)

- **Database:** `vendor_decision_support`.
- **Tables:** `vendors`, `categories`, `criteria`, `evaluations`, `personas`, `persona_weights`.
- **Integrity:** Enforces strict Foreign Key constraints and `CHECK` bounds on assigned scores ($1.0\text{--}5.0$) and category weights ($0.0\text{--}1.0$).

### 4. Semantic Data Model Layer (Power BI Import Mode)

- **Model:** Star Schema topology consisting of central `evaluations` fact table connected to single-directional `vendors`, `categories`, and `criteria` dimension tables.
- **Disconnected Slicers:** `personas` and `persona_weights` tables sit disconnected to prevent model circularity during runtime re-weighting.

### 5. Analytics & DAX Calculation Engine

- **Dynamic Re-Weighting:** Executes runtime recalculations of category scores using `SELECTEDVALUE(personas[persona_id])`.
- **Measures:** `Total Weighted Score`, `Score Delta to Leader`, `Vendor Rank`, and dynamic narrative string generation[cite: 2].

### 6. Executive Presentation Layer

- **Layout:** 16:9 widescreen ($1920 \times 1080\text{ px}$) dashboard featuring:
  - **Zone A:** Header & Recommendation Callout
  - **Zone B:** Leaderboard Table
  - **Zone C:** Category Contribution Stacked Bar Chart
