# Enterprise Agentic AI — Vendor Decision-Support System

> An executive-grade, interactive decision-support engine designed for solutions consultants and enterprise procurement teams to evaluate, score, and rank Agentic AI platforms across dynamic client scenarios.

---

## Executive Overview & Business Value

Evaluating enterprise software platforms often relies on static comparison spreadsheets and presentation decks created manually by solutions consulting teams[cite: 8, 10]. These traditional approaches are difficult to maintain, time-consuming to update, and fail to adapt when client priorities shift[cite: 8].

This project transforms static vendor comparisons into an interactive, data-driven decision-support engine[cite: 8, 10]. By combining structured market research, a normalized relational database[cite: 8, 9], Python ETL data transformation pipelines[cite: 8, 9], and interactive Power BI dashboard analytics[cite: 8, 9], the system enables consultants to:

- Evaluate **8 leading enterprise platforms** across **17 technical criteria** and **5 core capability pillars**[cite: 1, 2, 8].
- Recalculate vendor rankings and score deltas dynamically across **5 distinct client scenarios** (*Large Enterprise, Healthcare, Financial Services / BFSI, Public Sector, and Startup / Scale-Up*)[cite: 1, 2, 8].
- Maintain a transparent, evidence-based audit trail with source citations and evidence confidence ratings for every score[cite: 1, 2, 8].

---

## System Architecture

The system follows a decoupled, multi-layered data flow that isolates qualitative evidence collection from Python processing, SQL storage, DAX business logic, and visual presentation[cite: 1, 4, 8]:

```text
[Qualitative Research] ──► [Python ETL Pipeline] ──► [MySQL Store] ──► [Power BI Model] ──► [DAX Engine]
 (data/raw/*.csv)            (etl/*.py)             (vendor_db)        (Star Schema)      (Dynamic Ranks)

 ## Data Acquisition & Extraction

Qualitative evidence summaries and citation URLs are ingested from immutable raw CSV datasets stored under `data/raw/`.

## Python Transformation & Scoring Engine

Automated ETL scripts:

- Standardize schemas
- Enforce constraint assertions
- Apply rubric rules from `config/score_assignments.csv`
- Generate surrogate keys:
  - `V001–V008`
  - `C01–C17`
  - `E0001–E0136`

## Relational Database Storage

Processed datasets are loaded into a normalized MySQL schema:

- **Database:** `vendor_decision_support`
- **Integrity:** Enforces referential integrity across 6 core tables.

## Semantic Data Model & DAX Engine

Power BI connects via **Import Mode** using a clean **Star Schema** topology.

Disconnected dimension tables (`personas`, `persona_weights`) feed dynamic DAX calculation measures to prevent circular dependencies during runtime re-weighting.

## Executive Interface

- **Canvas:** Widescreen
- **Resolution:** $1920 \times 1080\text{ px}$
- **Purpose:** Optimized for executive presentation.

---

# Dashboard Layout & Interactive UI

## Dashboard Interface & Analytics View

![Enterprise AI Vendor Dashboard Overview(outputs/dashboard_screenshots/complete_dashboard_overview.png)]

The Power BI presentation layer uses a three-zone visual layout designed for instant executive clarity.

### Zone A – Navigation & Recommendation Callout

Dark SaaS navigation header containing client scenario selection, paired with an executive card displaying:

- Top pick
- Active profile
- Dynamic consulting rationale
![Zone A Header(outputs/dashboard_screenshots/zone_A_1.png)]
![Zone A Recommendation Banner(outputs/dashboard_screenshots/zone_A_2.png)]

### Zone B – Rank Leaderboard Table

Stack-ranked table featuring:

- Vendor Name
- Rank
- Weighted Score
- Gap to Leader delta ($0.00$ to $-1.00$)
![Zone B Leaderboard Table(outputs/dashboard_screenshots/zone_B.png)]

### Zone C – 100% Stacked Bar Chart

Visual breakdown displaying category score contributions normalized across all **5 capability pillars** using a tech-gradient color palette.
![Zone C Category Breakdown Chart(outputs/dashboard_screenshots/zone_C.png)]
---

# Evaluated Vendors & Capability Pillars

## Evaluated Platforms

1. **C3.ai** — Enterprise AI Platform
2. **Google Cloud Platform / GCP** — Cloud & AI Infrastructure
3. **ServiceNow** — IT Service Management & Workflows
4. **Salesforce** — Customer Relationship Management
5. **Glean AI** — Enterprise Search & Knowledge
6. **Writer AI** — Enterprise Generative AI Suite
7. **K2view** — Enterprise Data Management & Data Mesh
8. **Signzy** — Identity Verification & Digital Trust

## Capability Pillars & Criteria ($17\text{ Total}$)

### Category 1 – Core Agent Intelligence

- Autonomy
- Planning & Reasoning
- Workflow Orchestration
- Memory & Context Management
- Learning & Adaptability

### Category 2 – Agent Architecture & Development

- Multi-Agent Collaboration
- Low-Code Agent Creation
- LLM Agnosticism
- Ease of Development

### Category 3 – Enterprise Integration & Deployment

- Tool & API Integration
- Deployment Flexibility

### Category 4 – Governance, Security & Trust

- Human-in-the-Loop (HITL)
- Observability & Explainability
- Governance & Security

### Category 5 – Enterprise Readiness & Business Value

- Scalability
- Business Domain Fit
- Business Value / ROI

---

# Tech Stack & Tooling

| **Component** | **Technology** | **Role / Functionality** |
|---|---|---|
| **Language** | Python 3.11+ | ETL automation, data cleaning, scoring & validation |
| **Data Manipulation** | Pandas, NumPy | Data transformation, string standardization, schema merging |
| **Database ORM** | SQLAlchemy, PyMySQL | Relational database connection, query execution & loading |
| **Relational DB** | MySQL 8.0 | Structured storage for vendors, criteria, evaluations, personas |
| **Analytics Engine** | Microsoft Power BI Desktop | Data modeling, DAX measures, dynamic re-weighting logic |
| **Version Control** | Git / GitHub | Code management, documentation tracking, revision control |

[cite: 8, 9]

# Repository Structure

Vendor-Decision-Support-System/
├── README.md                           # Master project overview & documentation
├── config/                             # External configuration files
│   ├── score_assignments.csv           # Primary score control matrix (1.0-5.0)
│   └── scoring_rubric.json             # Quality standards & rating definitions
├── data/                               # Data storage layer
│   ├── raw/                            # Immutable raw research CSVs (8 vendors)
│   ├── cleaned/                        # Standardized text datasets
│   └── processed/                      # Database-ready structured CSVs
├── docs/                               # Detailed technical documentation
│   ├── 36_Business_Insights.md         # Executive consulting findings & insights
│   ├── 37_Pipeline_Test_Report.md      # End-to-end pipeline test execution log
│   ├── 38A_System_Architecture.md      # System architecture & component mapping
│   ├── 38B_Data_Dictionary.md          # Database entity schemas & constraints
│   ├── 38C_Scoring_Methodology.md      # 5-point evaluation scale & formulas
│   └── 38D_Persona_Weighting_Rationale.md # Scenario weighting distributions
├── etl/                                # Modular Python ETL engine
│   ├── clean_data.py                   # Standardizes formatting & cleans text
│   ├── validate_data.py                # Quality assertion checks
│   ├── assign_scores.py                # Merges scoring assignments
│   ├── generate_final_dataset.py       # ID assignment & surrogate keys
│   ├── load_database.py                # Idempotent MySQL database loader
│   └── validate_database.py            # Relational database integrity check
├── sql/                                # Database scripts
│   ├── schema.sql                      # Relational table creation DDL
│   └── create_persona_tables.sql       # Seed scripts for personas & weights
└── powerbi/                            # Analytics assets
    └── dashboard.pbix                  # Power BI report & DAX semantic model

## Quickstart Setup & Installation

### 1. Prerequisites

- Python 3.11 or higher installed.
- MySQL Server 8.0 running locally or on a network.
- Microsoft Power BI Desktop.

### 2. Environment Setup

Clone the repository and initialize a virtual environment:

```bash
git clone https://github.com/your-username/Vendor-Decision-Support-System.git
cd Vendor-Decision-Support-System

python -m venv .venv

# Activate on Windows:
.venv\Scripts\activate

# Activate on macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Database Credentials Configuration

Create a `.env` file in the root directory based on `.env.example`:

```ini
DB_HOST=localhost
DB_PORT=3306
DB_NAME=vendor_decision_support
DB_USER=root
DB_PASSWORD=your_mysql_password
```

### 4. Execute ETL Pipeline & Load MySQL

Run the pipeline to process raw evidence and load the database:

```bash
# 1. Clean raw vendor research data
python etl/clean_data.py

# 2. Validate data completeness
python etl/validate_data.py

# 3. Apply scoring rubric rules
python etl/assign_scores.py

# 4. Generate database-ready final dataset
python etl/generate_final_dataset.py

# 5. Initialize schema and load MySQL database
python etl/load_database.py

# 6. Verify relational database integrity
python etl/validate_database.py
```

### 5. Launch Power BI Dashboard

1. Open `powerbi/dashboard.pbix` in Power BI Desktop.
2. If prompted, update the MySQL native database connection credentials under **Transform Data → Data source settings**.
3. Click **Refresh** on the top Home ribbon to update all visuals.

## Key Business Findings

- **Platform Leadership:** C3.ai consistently holds the top rank across all five client scenario profiles (weighted scores of $4.92\text{--}4.94$), driven by its mature object models and uniform high scores across both technical intelligence and governance criteria.
- **Specialized Point Solutions:** Niche providers (e.g., Signzy) show significant score deltas (up to $-1.00$ below the leader) during broad enterprise evaluations due to functional gaps outside their primary vertical domain.
- **Competitive Clustering:** Runners-up (**ServiceNow, Glean AI, GCP, Salesforce**) operate within a tight 0.08 score band ($4.58\text{--}4.66$), indicating that secondary procurement selections depend heavily on a buyer's existing core software infrastructure.