# 11B. Entity Relationships

## Overview

After identifying the business entities, the next step is to define the relationships between them. These relationships determine how data is connected throughout the application and form the structural blueprint for the Entity-Relationship Diagram (ERD).

The relationship model follows standard relational database design principles, minimizes redundancy through normalization, and supports future expansion without structural changes.

---

# Domain Relationships

### SoftwareCategory → Vendor

**Relationship:** One-to-Many (1:M)

* One software category can contain many vendors.
* Each vendor belongs to one primary software category.

---

### Vendor ↔ EvaluationDomain

**Relationship:** Many-to-Many (M:N)

Implemented through:

**VendorCapability**

A vendor can possess capabilities in multiple evaluation domains, and each evaluation domain can contain multiple vendors.

---

# Evaluation Framework Relationships

### EvaluationDomain → EvaluationCategory

**Relationship:** One-to-Many (1:M)

Each evaluation domain defines its own evaluation framework.

Each evaluation category belongs to one evaluation domain.

---

### EvaluationCategory → EvaluationCriterion

**Relationship:** One-to-Many (1:M)

Each evaluation category contains multiple evaluation criteria.

Each criterion belongs to one evaluation category.

The criterion also stores its fixed internal weight used by the scoring methodology.

---

# Client Decision Support Relationships

### ClientPersona → WeightProfile

**Relationship:** One-to-One (1:1)

Each predefined client persona has one default weighting profile.

Custom weighting profiles are created independently of predefined personas.

---

### WeightProfile → CategoryWeight

**Relationship:** One-to-Many (1:M)

Each weighting profile contains one weight for every evaluation category.

---

### EvaluationCategory → CategoryWeight

**Relationship:** One-to-Many (1:M)

Each evaluation category appears in multiple weighting profiles.

---

# Vendor Assessment Relationships

### Vendor → VendorEvaluation

**Relationship:** One-to-Many (1:M)

A vendor can have multiple evaluations over time.

Each evaluation belongs to one vendor.

---

### EvaluationDomain → VendorEvaluation

**Relationship:** One-to-Many (1:M)

Each evaluation is performed within one evaluation domain.

---

### EvaluationStatus → VendorEvaluation

**Relationship:** One-to-Many (1:M)

Each evaluation has one status.

A status can be shared by multiple evaluations.

---

### VendorEvaluation → VendorCriterionScore

**Relationship:** One-to-Many (1:M)

Each vendor evaluation contains multiple criterion scores.

Each criterion score belongs to one vendor evaluation.

---

### EvaluationCriterion → VendorCriterionScore

**Relationship:** One-to-Many (1:M)

Each evaluation criterion can be evaluated multiple times across different vendors and evaluation instances.

---

# Evidence Relationships

### VendorCriterionScore → Evidence

**Relationship:** One-to-Many (1:M)

Each criterion score can be supported by multiple pieces of evidence.

Each evidence record supports one criterion score.

---

### EvidenceSource → Evidence

**Relationship:** One-to-Many (1:M)

Each evidence source type classifies many evidence records.

Each evidence record belongs to one evidence source type.

---

# Relationship Summary

| Parent Entity        | Child Entity         | Relationship |
| -------------------- | -------------------- | ------------ |
| SoftwareCategory     | Vendor               | 1:M          |
| Vendor               | VendorCapability     | 1:M          |
| EvaluationDomain     | VendorCapability     | 1:M          |
| EvaluationDomain     | EvaluationCategory   | 1:M          |
| EvaluationCategory   | EvaluationCriterion  | 1:M          |
| ClientPersona        | WeightProfile        | 1:1          |
| WeightProfile        | CategoryWeight       | 1:M          |
| EvaluationCategory   | CategoryWeight       | 1:M          |
| Vendor               | VendorEvaluation     | 1:M          |
| EvaluationDomain     | VendorEvaluation     | 1:M          |
| EvaluationStatus     | VendorEvaluation     | 1:M          |
| VendorEvaluation     | VendorCriterionScore | 1:M          |
| EvaluationCriterion  | VendorCriterionScore | 1:M          |
| VendorCriterionScore | Evidence             | 1:M          |
| EvidenceSource       | Evidence             | 1:M          |

---

# Design Rationale

The relationship model follows the principles below:

* Lookup entities are separated from transactional entities.
* Many-to-many relationships are resolved through junction tables.
* Each evaluation domain owns its own evaluation framework, making the framework reusable across future domains.
* Vendor evaluations are stored independently of vendor master data, allowing historical assessments without overwriting previous results.
* Weighting profiles are independent of vendor evaluations, enabling consultants to generate multiple recommendations using different client priorities.
* Supporting evidence is stored independently of scores to ensure transparency, traceability, and auditability.

These relationships provide the structural foundation for the Entity-Relationship Diagram (ERD) and the normalized relational database schema developed in the next stage.
