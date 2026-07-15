# System Architecture

## Overview

The Vendor Decision-Support Tool follows a layered architecture that separates data collection, processing, storage, business logic, analytics, and user interaction. This modular design improves maintainability, scalability, and reusability while allowing individual components to evolve independently.

The architecture supports multiple software categories and evaluation domains through a reusable framework while implementing a single evaluation domain in the MVP.

---

# Architectural Layers

## Layer 1 – Data Collection

### Purpose

Collect structured evaluation evidence from trusted public sources.

### Inputs

* Official product documentation
* Technical documentation
* Product demonstrations
* Whitepapers
* Analyst reports
* Customer case studies
* Release notes

### Output

Raw vendor research and supporting evidence.

---

## Layer 2 – Data Processing (Python ETL)

### Purpose

Transform raw research into standardized evaluation data.

### Responsibilities

* Data validation
* Data cleaning
* Metadata assignment
* Evidence verification
* Score preparation
* Missing data validation
* Criterion weight re-normalization (when applicable)
* Data transformation
* Data loading into the relational database

### Output

Structured evaluation dataset ready for database storage.

---

## Layer 3 – Relational Database

### Purpose

Store all evaluation data in a normalized relational database that serves as the single source of truth for the application.

### Stores

* Vendors
* Software Categories
* Evaluation Domains
* Vendor Capabilities
* Evaluation Categories
* Evaluation Criteria
* Vendor Evaluations
* Vendor Criterion Scores
* Evidence
* Evidence Sources
* Client Personas
* Persona Category Weights
* Custom Weight Profiles
* Audit Information

### Output

Centralized data repository for reporting, analytics, and dynamic score calculations.

---

## Layer 4 – Evaluation & Scoring Engine

### Purpose

Apply the Evaluation & Scoring Methodology to generate objective, explainable, and dynamic vendor recommendations.

### Implementation

The Evaluation & Scoring Engine is implemented across two components:

#### Python ETL (Static Processing)

Responsible for:

* Validating evaluation data
* Verifying supporting evidence
* Handling missing data
* Re-normalizing criterion weights when required
* Preparing raw criterion scores
* Loading validated evaluation data into SQL

These processes are executed during data preparation and do not depend on the selected client persona.

#### Power BI (Dynamic Processing using DAX)

Responsible for:

* Applying persona category weights
* Applying custom weight profiles
* Calculating weighted category scores
* Calculating overall vendor scores
* Ranking vendors
* Applying tie-breaking rules
* Updating recommendations dynamically as consultants change weighting profiles

These calculations are performed at report runtime, enabling interactive decision support without modifying the underlying stored evaluation data.

---

## Layer 5 – Analytics & Visualization

### Technology

Microsoft Power BI

### Responsibilities

* Interactive dashboards
* Vendor comparison
* Category score breakdown
* Criterion-level drill-down
* Persona selection
* Custom weighting
* Recommendation visualization
* Evidence exploration
* Explainable score analysis

---

## Layer 6 – Decision Support

### Primary User

Internal Pre-Sales / Solutions Consultant

### Workflow

1. Select the evaluation domain.
2. Select a predefined client persona or create a custom weight profile.
3. Review dynamically calculated vendor rankings.
4. Analyze category and criterion score breakdowns.
5. Review supporting evidence and score justifications.
6. Recommend the most suitable vendor based on the client's priorities.

---

# End-to-End Data Flow

```text
Trusted Research Sources
            │
            ▼
   Python ETL Pipeline
            │
            ▼
 Relational SQL Database
            │
            ▼
      Microsoft Power BI
            │
            ├── DAX Scoring Engine
            ├── Persona Weighting
            ├── Custom Weight Profiles
            ├── Dynamic Ranking
            └── Recommendation Logic
            │
            ▼
 Consultant Recommendation
```

---

# Architectural Design Principles

The architecture is designed around the following principles:

* Modular separation of responsibilities.
* Reusable evaluation framework.
* Evidence-based scoring.
* Explainable recommendations.
* Normalized and maintainable data model.
* Dynamic recommendation generation through interactive weighting.
* Separation of business logic from presentation.
* Scalability to support additional software categories and evaluation domains.
* Future extensibility without requiring major architectural redesign.

---

# Technology Mapping

| Layer                     | Technology              | Primary Responsibility                                            |
| ------------------------- | ----------------------- | ----------------------------------------------------------------- |
| Data Collection           | Public Research Sources | Collect trusted vendor information and supporting evidence        |
| Data Processing           | Python                  | Clean, validate, transform, and prepare evaluation data           |
| Data Storage              | SQL Database            | Store normalized evaluation data and metadata                     |
| Evaluation & Scoring      | Python + Power BI (DAX) | Prepare raw scores and calculate dynamic weighted recommendations |
| Analytics & Visualization | Power BI                | Interactive reporting and decision support                        |
| Decision Support          | Consultant Workflow     | Generate transparent, client-specific vendor recommendations      |

---

This layered architecture serves as the blueprint for the database design, ETL pipeline, Power BI implementation, and overall system development. By separating data preparation from interactive scoring, the framework ensures consistent vendor evaluations while enabling consultants to generate real-time recommendations based on different client priorities.
