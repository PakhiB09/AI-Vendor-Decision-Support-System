# 11C.1 – Table Attributes

## Overview

This document defines the logical structure of each database entity by specifying its primary key, foreign keys, and core attributes.

The attributes are designed to support the Vendor Decision-Support Tool's reusable evaluation framework while maintaining normalization, scalability, and data integrity.

---

# 1. SoftwareCategory

### Purpose

Stores the primary software category of each vendor.

| Attribute                   | Description                                  |
| --------------------------- | -------------------------------------------- |
| **SoftwareCategoryID (PK)** | Unique identifier for the software category. |
| CategoryName                | Name of the software category.               |
| Description                 | Description of the software category.        |

---

# 2. EvaluationDomain

### Purpose

Stores the capability or business domain used for vendor evaluations.

| Attribute                   | Description                                  |
| --------------------------- | -------------------------------------------- |
| **EvaluationDomainID (PK)** | Unique identifier for the evaluation domain. |
| DomainName                  | Name of the evaluation domain.               |
| Description                 | Description of the evaluation domain.        |

---

# 3. Vendor

### Purpose

Stores master information about enterprise software vendors.

| Attribute               | Description                                        |
| ----------------------- | -------------------------------------------------- |
| **VendorID (PK)**       | Unique identifier for the vendor.                  |
| SoftwareCategoryID (FK) | References the vendor's primary software category. |
| VendorName              | Vendor name.                                       |
| Website                 | Official website.                                  |
| Headquarters            | Headquarters location (optional).                  |
| Description             | Short vendor overview.                             |

---

# 4. VendorCapability

### Purpose

Associates vendors with one or more evaluation domains.

| Attribute                   | Description                  |
| --------------------------- | ---------------------------- |
| **VendorCapabilityID (PK)** | Unique identifier.           |
| VendorID (FK)               | References Vendor.           |
| EvaluationDomainID (FK)     | References EvaluationDomain. |

---

# 5. EvaluationCategory

### Purpose

Stores the high-level evaluation categories belonging to an evaluation domain.

| Attribute                     | Description                      |
| ----------------------------- | -------------------------------- |
| **EvaluationCategoryID (PK)** | Unique identifier.               |
| EvaluationDomainID (FK)       | References EvaluationDomain.     |
| CategoryName                  | Name of the evaluation category. |
| Description                   | Category description.            |

---

# 6. EvaluationCriterion

### Purpose

Stores detailed evaluation criteria for a specific evaluation category.

| Attribute                 | Description                                                |
| ------------------------- | ---------------------------------------------------------- |
| **CriterionID (PK)**      | Unique identifier.                                         |
| EvaluationCategoryID (FK) | References EvaluationCategory.                             |
| CriterionName             | Criterion name.                                            |
| Definition                | Detailed description of the evaluation criterion.          |
| InternalCriterionWeight   | Fixed internal weight used within its evaluation category. |

---

# 7. ClientPersona

### Purpose

Stores predefined client personas.

| Attribute          | Description                        |
| ------------------ | ---------------------------------- |
| **PersonaID (PK)** | Unique identifier.                 |
| PersonaName        | Name of the client persona.        |
| Description        | Description of the client persona. |

---

# 8. WeightProfile

### Purpose

Stores weighting profiles used during vendor recommendations.

| Attribute                | Description                                            |
| ------------------------ | ------------------------------------------------------ |
| **WeightProfileID (PK)** | Unique identifier.                                     |
| PersonaID (FK, Nullable) | References ClientPersona for predefined profiles.      |
| ProfileName              | Name of the weighting profile.                         |
| ProfileType              | Indicates whether the profile is Predefined or Custom. |
| Description              | Optional profile description.                          |

---

# 9. CategoryWeight

### Purpose

Stores category weights assigned to each weighting profile.

| Attribute                     | Description                                            |
| ----------------------------- | ------------------------------------------------------ |
| **WeightProfileID (FK)**      | References WeightProfile.                              |
| **EvaluationCategoryID (FK)** | References EvaluationCategory.                         |
| Weight                        | Percentage weight assigned to the evaluation category. |

### Composite Primary Key

**(WeightProfileID, EvaluationCategoryID)**

---

# 10. EvaluationStatus

### Purpose

Stores the lifecycle state of vendor evaluations.

| Attribute         | Description                           |
| ----------------- | ------------------------------------- |
| **StatusID (PK)** | Unique identifier.                    |
| StatusName        | Draft, In Review, Approved, Archived. |

---

# 11. VendorEvaluation

### Purpose

Represents a single vendor evaluation.

| Attribute                | Description                                                                                                                                                                     |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **EvaluationID (PK)**    | Unique identifier.                                                                                                                                                              |
| VendorID (FK)            | References Vendor.                                                                                                                                                              |
| EvaluationDomainID (FK)  | References EvaluationDomain.                                                                                                                                                    |
| StatusID (FK)            | References EvaluationStatus.                                                                                                                                                    |
| EvaluationDate           | Date the evaluation was performed.                                                                                                                                              |
| EvaluatedBy              | Name of the evaluator.                                                                                                                                                          |
| EvaluationFrameworkLabel | Text label identifying the evaluation methodology used (e.g., "Agentic AI Framework v1.0"). Stored for documentation purposes only; it does not implement framework versioning. |
| Notes                    | General evaluation comments.                                                                                                                                                    |
| CreatedAt                | Record creation timestamp.                                                                                                                                                      |
| UpdatedAt                | Last modification timestamp.                                                                                                                                                    |

---

# 12. VendorCriterionScore

### Purpose

Stores criterion-level evaluation scores.

| Attribute                 | Description                                |
| ------------------------- | ------------------------------------------ |
| **CriterionScoreID (PK)** | Unique identifier.                         |
| EvaluationID (FK)         | References VendorEvaluation.               |
| CriterionID (FK)          | References EvaluationCriterion.            |
| Score                     | Assigned score (1–5).                      |
| ConfidenceLevel           | High, Medium, or Low evidence confidence.  |
| Justification             | Explanation supporting the assigned score. |
| CreatedAt                 | Record creation timestamp.                 |
| UpdatedAt                 | Last modification timestamp.               |

---

# 13. EvidenceSource

### Purpose

Stores evidence source classifications.

| Attribute                 | Description                                                                                 |
| ------------------------- | ------------------------------------------------------------------------------------------- |
| **EvidenceSourceID (PK)** | Unique identifier.                                                                          |
| SourceType                | Official Documentation, Whitepaper, Analyst Report, Product Demo, Customer Case Study, etc. |
| Description               | Description of the evidence source type.                                                    |

---

# 14. Evidence

### Purpose

Stores supporting evidence used to justify criterion scores.

| Attribute             | Description                                  |
| --------------------- | -------------------------------------------- |
| **EvidenceID (PK)**   | Unique identifier.                           |
| CriterionScoreID (FK) | References VendorCriterionScore.             |
| EvidenceSourceID (FK) | References EvidenceSource.                   |
| Title                 | Title or name of the supporting evidence.    |
| ReferenceURL          | URL or citation for the supporting evidence. |
| Notes                 | Additional evaluator notes.                  |
| CreatedAt             | Record creation timestamp.                   |
| UpdatedAt             | Last modification timestamp.                 |

---

# Key Design Decisions

* Every entity has a stable primary key, while associative entities use composite primary keys where appropriate.
* Many-to-many relationships are resolved through junction tables.
* Each evaluation domain owns its own evaluation categories and criteria, enabling the framework to support multiple evaluation domains without structural changes.
* Internal criterion weights are stored directly within the **EvaluationCriterion** entity as **InternalCriterionWeight**, as they remain constant within the MVP.
* Framework versioning was considered during the database design process but intentionally deferred in accordance with the MVP scope defined in Step 3. The **EvaluationFrameworkLabel** field is stored solely as descriptive metadata and does not implement framework versioning.
* Weight profiles are independent of vendor evaluations, allowing recommendations to be recalculated dynamically for different client personas or custom profiles.
* Vendor evaluations preserve historical assessment records without modifying vendor master data.
* Supporting evidence is stored independently from evaluation scores to ensure transparency, traceability, and auditability.
* Final vendor rankings and weighted scores are **not stored in the database**. They are calculated dynamically within **Power BI (DAX)** based on the selected weighting profile, ensuring recommendations always reflect the latest client priorities.

This logical schema provides the foundation for the Entity-Relationship Diagram (ERD), SQL implementation, ETL pipeline, and Power BI semantic model.


