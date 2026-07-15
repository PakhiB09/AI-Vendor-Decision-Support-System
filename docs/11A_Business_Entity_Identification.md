# 11A.  Business Entity Identification

## Overview

Before designing the Entity-Relationship Diagram (ERD), the core business entities of the Vendor Decision-Support Tool are identified. These entities represent the primary business concepts managed by the application and form the conceptual foundation of the relational database.

The entities are grouped into logical modules based on their role within the system.

---

# Module 1 – Domain Structure

These entities describe the enterprise software landscape and define what is being evaluated.

| Entity               | Purpose                                                                                                                                   |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **SoftwareCategory** | Stores the vendor's primary software category (e.g., Cloud & AI Platform, CRM, ITSM, Enterprise Search).                                  |
| **EvaluationDomain** | Stores the capability or business domain through which vendors are evaluated (e.g., Agentic AI in the MVP).                               |
| **Vendor**           | Stores information about each enterprise software vendor.                                                                                 |
| **VendorCapability** | Associates vendors with one or more evaluation domains, allowing heterogeneous vendors to be evaluated under multiple capability domains. |

---

# Module 2 – Evaluation Framework

These entities define the evaluation methodology used within each evaluation domain.

| Entity                  | Purpose                                                                                                                                            |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **EvaluationCategory**  | Stores the high-level evaluation categories for a specific evaluation domain.                                                                      |
| **EvaluationCriterion** | Stores the detailed evaluation criteria belonging to each evaluation category, including the fixed internal weight used during score calculations. |

---

# Module 3 – Client Decision Support

These entities personalize vendor recommendations based on client priorities.

| Entity             | Purpose                                                                                          |
| ------------------ | ------------------------------------------------------------------------------------------------ |
| **ClientPersona**  | Stores predefined client personas such as Startup, Enterprise, Healthcare, BFSI, and Government. |
| **WeightProfile**  | Represents either a predefined persona profile or a consultant-created custom weighting profile. |
| **CategoryWeight** | Stores the weight assigned to each evaluation category within a specific weight profile.         |

---

# Module 4 – Vendor Assessment

These entities store the results of vendor evaluations.

| Entity                   | Purpose                                                                                                                                                    |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **VendorEvaluation**     | Represents a single evaluation instance for a vendor within a specific evaluation domain. Supports future reassessments and historical evaluation records. |
| **EvaluationStatus**     | Stores the lifecycle state of an evaluation (e.g., Draft, In Review, Approved, Archived).                                                                  |
| **VendorCriterionScore** | Stores the score assigned to each evaluation criterion during a vendor evaluation.                                                                         |

---

# Module 5 – Evidence Management

These entities provide transparency and traceability for every assigned score.

| Entity             | Purpose                                                                                                                          |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| **Evidence**       | Stores supporting evidence used to justify individual criterion scores.                                                          |
| **EvidenceSource** | Classifies the origin of evidence (e.g., Official Documentation, Analyst Report, Whitepaper, Product Demo, Customer Case Study). |

---

# Conceptual Business Flow

The Vendor Decision-Support Tool follows the business flow below:

Software Category

↓

Vendor

↓

Evaluation Domain

↓

Vendor Evaluation

↓

Criterion Scores

↓

Supporting Evidence

↓

Weighted Recommendation

This separation enables vendor information, evaluation methodology, assessment results, supporting evidence, and recommendation logic to evolve independently while maintaining a normalized and maintainable data model.

---

# Design Principles

The business entity model follows these principles:

* Each entity represents a single business concept.
* Evaluation domains own their own evaluation framework.
* Vendor information is independent of evaluation results.
* Client weighting profiles are independent of vendor assessments.
* Every assigned score is supported by traceable evidence.
* The model supports future expansion without requiring structural database changes.

These entities provide the conceptual foundation for the Entity-Relationship Diagram (ERD) and relational database schema.
