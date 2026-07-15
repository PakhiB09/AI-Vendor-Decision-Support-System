# Step 13 – Project Folder and Repository Structure

## Purpose

A well-organized repository is an essential part of professional software development. Separating source code, configuration, documentation, data, analytics assets, and outputs improves maintainability, simplifies collaboration, and makes the project easier to understand.

Before implementation begins, the repository structure is planned to ensure each component has a clearly defined responsibility.

---

# Repository Structure

```text
AI-Vendor-Comparison-Dashboard/

│
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── requirements.txt
│
├── config/
│   ├── vendors.csv
│   ├── evaluation_criteria.csv
│   ├── criteria_weights.csv
│   ├── client_personas.csv
│   └── normalization_rules.csv
│
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── processed/
│
├── docs/
│   ├── project_vision.md
│   ├── problem_definition.md
│   ├── system_scope.md
│   ├── stakeholder_analysis.md
│   ├── functional_requirements.md
│   ├── non_functional_requirements.md
│   ├── evaluation_framework.md
│   ├── database_design.md
│   ├── entity_relationship_diagram.md
│   ├── python_etl_pipeline_plan.md
│   └── project_repository_structure.md
│
├── etl/
│   ├── extract.py
│   ├── clean.py
│   ├── normalize.py
│   ├── score.py
│   ├── load.py
│   └── main.py
│
├── sql/
│   ├── schema.sql
│   ├── seed_data.sql
│   └── queries.sql
│
├── powerbi/
│   ├── dashboard.pbix
│   └── dax_measures.md
│
├── assets/
│   ├── images/
│   └── diagrams/
│
├── notebooks/
│   └── 01_vendor_data_exploration.ipynb
│
├── logs/
│   ├── etl.log
│   ├── validation_report.txt
│   └── data_quality_report.txt
│
├── outputs/
│   ├── dashboard_screenshots/
│   ├── reports/
│   └── presentations/
│
└── tests/
    └── etl_tests.py
```

---

# Directory Overview

## Root Directory

The root directory contains the primary project files required for project setup, dependency management, licensing, and documentation.

| File             | Purpose                                                          |
| ---------------- | ---------------------------------------------------------------- |
| README.md        | Project overview, setup instructions, and usage guide            |
| LICENSE          | Defines the project's open-source license                        |
| .gitignore       | Excludes generated and sensitive files from version control      |
| .env.example     | Example environment variables required for database connectivity |
| requirements.txt | Lists Python package dependencies                                |

---

## config/

Stores configuration files that define business rules used by the ETL pipeline.

Examples include:

* Vendor definitions
* Evaluation criteria
* Criteria weights
* Client personas
* Normalization rules

Keeping these values outside the source code makes the application reusable and easier to maintain.

---

## data/

Stores datasets used throughout the ETL process.

### raw/

Original vendor datasets collected from external sources.

### cleaned/

Validated and standardized datasets after data cleaning.

### processed/

Normalized and scored datasets ready for database loading.

---

## docs/

Contains all project planning and design documentation created throughout the project lifecycle.

This includes project planning, requirements analysis, database design, ETL planning, architecture documentation, and supporting technical documentation.

---

## etl/

Contains the Python implementation of the ETL pipeline.

Each module performs a single stage of the pipeline.

| File         | Responsibility                             |
| ------------ | ------------------------------------------ |
| extract.py   | Read raw vendor data                       |
| clean.py     | Validate and standardize datasets          |
| normalize.py | Convert values into a common scoring scale |
| score.py     | Calculate weighted scores and rankings     |
| load.py      | Load processed data into the SQL database  |
| main.py      | Execute the complete ETL workflow          |

---

## sql/

Contains database resources.

Typical files include:

* Database schema
* Seed data
* Reusable SQL queries

---

## powerbi/

Contains Power BI reporting assets.

This directory stores the dashboard file and documentation for DAX measures and calculated columns.

---

## assets/

Stores images and diagrams referenced throughout the documentation.

Examples include architecture diagrams, ER diagrams, dashboard screenshots, and supporting visuals.

---

## notebooks/

Contains exploratory notebooks used during data analysis and development.

These notebooks document exploratory analysis, data quality observations, and reasoning before implementation of the production ETL pipeline.

---

## logs/

Stores ETL execution logs and validation reports generated during processing.

Examples include:

* ETL execution logs
* Data quality reports
* Validation summaries

Keeping these reports improves transparency and assists with troubleshooting and auditing.

---

## outputs/

Stores final project deliverables generated during development.

Examples include:

* Dashboard screenshots
* Exported reports
* Presentation materials

Separating generated outputs from source files keeps the repository organized while making project results easy to access.

---

## tests/

Contains automated tests for validating ETL functionality.

As the project evolves, this directory can include tests for data validation, normalization logic, scoring calculations, and database loading.

---

# Repository Design Principles

The repository follows several software engineering principles:

* Separation of concerns through dedicated directories
* Modular ETL architecture
* Externalized business configuration
* Clear separation of source code, documentation, data, and analytics assets
* Scalability for additional vendors, evaluation frameworks, and datasets
* Maintainable structure suitable for collaborative development

---

# Outcome

This repository structure provides a clean, modular, and scalable foundation for the AI Vendor Comparison Dashboard. By organizing documentation, configuration, ETL modules, SQL resources, Power BI assets, generated outputs, and supporting files into dedicated directories, the project remains maintainable, extensible, and aligned with professional software engineering practices.
