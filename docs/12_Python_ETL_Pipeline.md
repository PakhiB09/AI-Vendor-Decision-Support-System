# Step 12 – Python ETL Pipeline Plan

## Purpose

The AI Vendor Comparison Dashboard relies on an Extract–Transform–Load (ETL) pipeline to convert raw vendor evaluation data into structured, standardized, and analytics-ready information stored in the SQL database.

Rather than implementing all processing in a single script, the pipeline is designed as a modular, configuration-driven workflow. This approach improves maintainability, supports future enhancements, and allows the system to evaluate different vendors, industries, and client scenarios without modifying the application logic.

---

# ETL Pipeline Overview

```
Configuration Files
(vendors, criteria, weights, personas)

          │
          ▼

      Extract
(Read raw vendor data)

          │
          ▼

       Clean
(Validate and standardize data)

          │
          ▼

     Normalize
(Convert values to a common scale)

          │
          ▼

       Score
(Apply weights and calculate rankings)

          │
          ▼

        Load
(Store processed data in SQL)

          │
          ▼

   Power BI Dashboard
```

---

# Stage 1 – Extract

### Objective

Read raw vendor evaluation data from external sources.

No business logic or calculations are performed during this stage.

### Possible Data Sources

* CSV files
* Excel spreadsheets
* JSON files
* REST APIs
* Manual research datasets

For the MVP, vendor data will be sourced from CSV or Excel files.

### Input

Raw vendor evaluation data.

### Output

A raw DataFrame containing the imported vendor information.

---

# Stage 2 – Clean

### Objective

Improve data quality before any scoring or analysis takes place.

### Responsibilities

* Remove duplicate records
* Handle missing values
* Standardize vendor names
* Standardize categorical values
* Validate required fields
* Detect invalid or unexpected values

Examples include converting inconsistent values such as:

* Azure, azure, MICROSOFT AZURE → Microsoft Azure
* Excellent, excellent, EXCELLENT → Excellent

### Input

Raw DataFrame.

### Output

Validated and standardized DataFrame.

---

# Stage 3 – Normalize

### Objective

Convert different measurement scales into a common scoring system.

Since evaluation criteria may use different formats (numeric scales, percentages, or descriptive ratings), all values are normalized before scoring.

Examples include:

* 1–5 ratings
* 0–100 percentages
* Gold/Silver/Bronze classifications
* Excellent/Good/Fair/Poor ratings

These values are converted into a single numerical scale (for example, 0–10) to enable consistent comparison across vendors.

### Input

Clean DataFrame.

### Output

Normalized DataFrame.

---

# Stage 4 – Score

### Objective

Calculate vendor performance using the evaluation framework.

During this stage, the system combines:

* Normalized criterion scores
* Evaluation criteria
* Category weights
* Client persona priorities

The pipeline calculates:

* Weighted criterion scores
* Category scores
* Overall vendor score
* Vendor ranking
* Recommendation results

This stage represents the core business logic of the application.

### Input

Normalized DataFrame and configuration files.

### Output

Fully evaluated vendor dataset.

---

# Stage 5 – Load

### Objective

Store processed results inside the SQL database.

Processed information is inserted into the appropriate database tables, making it available for reporting and visualization.

The ETL pipeline does not communicate directly with Power BI. Instead, Power BI retrieves all information from the SQL database.

### Input

Scored vendor dataset.

### Output

Analytics-ready relational database.

---

# Configuration Externalization

To keep the ETL pipeline reusable and maintainable, business rules are stored outside the Python code.

The following configurations are externalized:

| Configuration       | Purpose                                     |
| ------------------- | ------------------------------------------- |
| Vendors             | Add or remove vendors without changing code |
| Evaluation Criteria | Modify comparison criteria                  |
| Criteria Weights    | Support different weighting strategies      |
| Client Personas     | Enable persona-specific evaluations         |
| Normalization Rules | Define score conversion mappings            |
| Input File Paths    | Support different data sources              |

This design allows new vendors, evaluation frameworks, or client scenarios to be introduced through configuration updates rather than code changes.

---

# Proposed Project Structure

```
project/

│
├── config/
│   ├── vendors.csv
│   ├── criteria.csv
│   ├── weights.csv
│   └── personas.csv
│
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── processed/
│
├── etl/
│   ├── extract.py
│   ├── clean.py
│   ├── normalize.py
│   ├── score.py
│   └── load.py
│
├── sql/
│
├── powerbi/
│
└── main.py
```

Each ETL module has a single responsibility, making the pipeline easier to test, maintain, and extend.

---

# ETL Flow Summary

| Stage     | Input                                | Processing                                  | Output                   |
| --------- | ------------------------------------ | ------------------------------------------- | ------------------------ |
| Extract   | Raw vendor data                      | Read external data sources                  | Raw DataFrame            |
| Clean     | Raw DataFrame                        | Validate and standardize data               | Clean DataFrame          |
| Normalize | Clean DataFrame                      | Convert values to a common scoring scale    | Normalized DataFrame     |
| Score     | Normalized DataFrame + configuration | Apply weights and calculate vendor rankings | Scored DataFrame         |
| Load      | Scored DataFrame                     | Store processed results in SQL              | Analytics-ready database |

---

# Outcome

This ETL design establishes a modular and reusable data processing pipeline for the AI Vendor Comparison Dashboard. By separating extraction, cleaning, normalization, scoring, and loading into independent stages and externalizing business configuration, the system remains scalable, maintainable, and adaptable to future vendors, evaluation frameworks, and client requirements without requiring changes to the core application logic.
