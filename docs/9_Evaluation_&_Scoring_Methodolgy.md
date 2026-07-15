# Evaluation & Scoring Methodology

## Overview

The Vendor Decision-Support Tool uses a structured, evidence-based scoring methodology to evaluate enterprise software vendors through the selected evaluation domain. The methodology is designed to ensure that all vendor assessments are objective, transparent, repeatable, and explainable.

Rather than relying on subjective opinions, every score is supported by documented evidence, standardized evaluation criteria, and a consistent weighting framework. Client-specific priorities influence only the weighting of evaluation categories, while the underlying vendor assessments remain unchanged.

---

# 1. Scoring Scale

Each evaluation criterion is scored using a five-point scale.

| Score | Rating    | Description                                                                                             |
| ----: | --------- | ------------------------------------------------------------------------------------------------------- |
|     5 | Excellent | Comprehensive enterprise-grade capability with strong implementation and extensive supporting evidence. |
|     4 | Strong    | Strong capability with only minor limitations or missing advanced features.                             |
|     3 | Adequate  | Meets core enterprise requirements but lacks several advanced capabilities.                             |
|     2 | Limited   | Partial implementation with significant functional limitations.                                         |
|     1 | Poor      | Minimal capability or no meaningful support for the evaluated criterion.                                |

---

# 2. Scoring Guidelines

Evaluators should assign scores based on demonstrated capabilities rather than marketing claims.

A score should consider:

* Product functionality
* Technical maturity
* Enterprise readiness
* Publicly available evidence
* Consistency across documentation and demonstrations

Scores should remain consistent across all evaluated vendors.

---

# 3. Evidence Requirements

Every assigned score must be supported by one or more verifiable sources.

Acceptable evidence includes:

* Official product documentation
* Technical documentation
* Product demonstrations
* Whitepapers
* Analyst reports
* Customer case studies
* Official release notes

Scores should never be assigned solely on assumptions or promotional marketing statements without supporting evidence.

---

# 4. Source of Truth Policy

When multiple sources are available, evidence should be prioritized using the following hierarchy:

| Priority | Source                                                 |
| -------- | ------------------------------------------------------ |
| 1        | Official product documentation                         |
| 2        | Technical documentation and developer guides           |
| 3        | Official product demonstrations and webinars           |
| 4        | Analyst reports (e.g., Gartner, Forrester, IDC)        |
| 5        | Customer case studies and implementation stories       |
| 6        | Independent technical reviews and trusted publications |

When conflicting information exists, the higher-priority source takes precedence.

---

# 5. Two-Level Weighting Framework

The scoring methodology uses hierarchical weighting.

## Level 1 – Category Weight

Evaluation categories receive dynamic weights based on the selected client persona or custom weighting profile.

**Illustrative Example** *(Actual category weights are determined by the selected client persona or custom weighting profile defined in Step 8.)*

| Category                              | Weight |
| ------------------------------------- | -----: |
| Core Agent Intelligence               |    25% |
| Agent Architecture & Development      |    20% |
| Enterprise Integration & Deployment   |    15% |
| Governance, Security & Trust          |    25% |
| Enterprise Readiness & Business Value |    15% |

These weights always total **100%**.

---

## Level 2 – Criterion Weight

Each evaluation criterion has a predefined weight within its respective category.

### Example – Core Agent Intelligence

| Criterion                   | Internal Weight |
| --------------------------- | --------------: |
| Autonomy                    |             30% |
| Planning & Reasoning        |             25% |
| Workflow Orchestration      |             20% |
| Memory & Context Management |             15% |
| Learning & Adaptability     |             10% |

Criterion weights are defined by the evaluation framework and remain constant across all client personas.

The combined criterion weights within each category always total **100%**.

---

# 6. Weighted Score Formula

Vendor scores are calculated using a hierarchical weighted scoring approach.

### Step 1 – Calculate the Category Score

Each category score is calculated as the weighted sum of its evaluation criteria.

**Category Score = Σ (Criterion Score × Criterion Weight)**

---

### Step 2 – Calculate the Overall Vendor Score

The overall vendor score is calculated by applying the selected category weights.

**Overall Vendor Score = Σ (Category Score × Category Weight)**

This two-level weighting methodology allows client priorities to influence recommendations while ensuring that the relative importance of individual evaluation criteria remains consistent across all assessments.

---

# 7. Normalization Rules

### MVP Implementation

All evaluation criteria in the MVP use the standardized **1–5 scoring scale**. Therefore, no score normalization is required during the evaluation process.

### Future Framework Support

If future evaluation domains introduce different scoring scales (e.g., 0–10, percentages, or domain-specific metrics), scores will first be normalized to a common scale before weighted calculations are performed.

This ensures consistent and comparable results across all evaluation criteria.

---

# 8. Missing Data Policy

Not all vendors publicly disclose information for every evaluation criterion.

If sufficient evidence cannot be obtained:

* The criterion is marked as **Not Evaluated (N/A)**.
* No assumptions or estimated scores are assigned.
* The missing criterion is excluded from the evaluation until sufficient evidence becomes available.
* The final evaluation notes clearly indicate the absence of sufficient evidence.

### Weight Re-normalization

If one or more criteria within a category are marked **Not Evaluated (N/A)**, the remaining criterion weights in that category are automatically re-normalized so that their combined weight equals **100%** before calculating the category score.

Each remaining criterion weight is divided by the sum of the remaining weights, ensuring that vendors are neither penalized nor rewarded due to unavailable evidence.

---

# 9. Evidence Confidence Level

Each criterion score is assigned an evidence confidence level based on the quality and quantity of supporting evidence.

| Confidence | Description                                                                                 |
| ---------- | ------------------------------------------------------------------------------------------- |
| High       | Multiple high-quality, authoritative sources consistently support the assigned score.       |
| Medium     | Adequate supporting evidence exists, but coverage or consistency is limited.                |
| Low        | Limited publicly available evidence; the assigned score should be interpreted with caution. |

Evidence confidence improves transparency without directly affecting the vendor's calculated score.

---

# 10. Score Justification & Audit Trail

Every assigned score should include supporting documentation to maintain transparency and traceability.

The evaluation record should contain:

| Field               | Purpose                             |
| ------------------- | ----------------------------------- |
| Vendor              | Evaluated vendor                    |
| Criterion           | Evaluation criterion                |
| Assigned Score      | Numerical score                     |
| Score Justification | Explanation for the assigned score  |
| Evidence Source(s)  | Supporting references               |
| Evidence Confidence | High / Medium / Low                 |
| Evaluated By        | Evaluator name                      |
| Evaluation Date     | Date of assessment                  |
| Framework Version   | Version of the evaluation framework |

This information creates a complete audit trail for every vendor assessment.

---

# 11. Tie-Breaking Rules

In the event that two or more vendors receive identical overall scores, recommendations are determined using the following priority order:

1. Higher score in **Governance, Security & Trust**
2. Higher score in **Core Agent Intelligence**
3. Higher score in **Enterprise Integration & Deployment**
4. Higher score in **Enterprise Readiness & Business Value**
5. Higher score in **Agent Architecture & Development**

If vendors remain tied after all category comparisons, they are reported as jointly ranked.

---

# Design Principles

The Evaluation & Scoring Methodology is based on the following principles:

* Objectivity through standardized criteria.
* Transparency through documented evidence and score justifications.
* Repeatability through consistent scoring rules.
* Explainability through hierarchical weighting and detailed score breakdowns.
* Flexibility through persona-based and custom weighting profiles.
* Reusability across multiple evaluation domains without requiring changes to the underlying scoring framework.

This methodology forms the analytical foundation of the Vendor Decision-Support Tool and guides every stage of the evaluation process, from data collection to final vendor recommendations.
