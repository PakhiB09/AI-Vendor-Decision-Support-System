# Client Personas and Weighting Profiles

## Overview

Different organizations evaluate enterprise AI platforms using different business priorities. A startup may prioritize rapid implementation and return on investment, while a financial institution may place greater emphasis on governance, security, and compliance.

To support these varying business needs, the Vendor Decision-Support Tool uses a flexible weighting framework that influences how vendor scores are calculated.

The framework supports two weighting modes:

1. **Predefined Client Personas** – Industry-based weighting presets that represent common enterprise purchasing scenarios.
2. **Custom Weight Profiles** – Consultant-defined category weightings tailored to a specific client's unique priorities.

This approach combines standardized recommendations with the flexibility expected in real-world pre-sales engagements.

---

# Evaluation Categories

All weighting profiles operate on the five evaluation categories defined in Step 7.

1. Core Agent Intelligence
2. Agent Architecture & Development
3. Enterprise Integration & Deployment
4. Governance, Security & Trust
5. Enterprise Readiness & Business Value

The combined category weights must always total **100%**.

---

# Weighting Modes

## Mode 1 – Predefined Client Personas

Predefined personas serve as recommended starting points for common enterprise customer types. Selecting a persona automatically applies a predefined weighting profile to the evaluation categories.

### Startup / Scale-Up

**Business Characteristics**

* Limited budget
* Small technical teams
* Rapid implementation
* Focus on productivity and growth

| Evaluation Category                   | Weight |
| ------------------------------------- | -----: |
| Core Agent Intelligence               |    25% |
| Agent Architecture & Development      |    25% |
| Enterprise Integration & Deployment   |    15% |
| Governance, Security & Trust          |    10% |
| Enterprise Readiness & Business Value |    25% |

---

### Large Enterprise

**Business Characteristics**

* Complex IT ecosystem
* Enterprise-wide deployments
* Long-term scalability
* Standardized governance

| Evaluation Category                   | Weight |
| ------------------------------------- | -----: |
| Core Agent Intelligence               |    20% |
| Agent Architecture & Development      |    15% |
| Enterprise Integration & Deployment   |    25% |
| Governance, Security & Trust          |    20% |
| Enterprise Readiness & Business Value |    20% |

---

### Financial Services (BFSI)

**Business Characteristics**

* Highly regulated environment
* Sensitive financial data
* Strict compliance requirements
* Risk-focused decision making

| Evaluation Category                   | Weight |
| ------------------------------------- | -----: |
| Core Agent Intelligence               |    15% |
| Agent Architecture & Development      |    10% |
| Enterprise Integration & Deployment   |    20% |
| Governance, Security & Trust          |    35% |
| Enterprise Readiness & Business Value |    20% |

---

### Healthcare

**Business Characteristics**

* Patient data privacy
* Regulatory compliance
* Secure clinical workflows
* Reliable AI-assisted operations

| Evaluation Category                   | Weight |
| ------------------------------------- | -----: |
| Core Agent Intelligence               |    20% |
| Agent Architecture & Development      |    10% |
| Enterprise Integration & Deployment   |    20% |
| Governance, Security & Trust          |    35% |
| Enterprise Readiness & Business Value |    15% |

---

### Public Sector / Government

**Business Characteristics**

* Security-first procurement
* High transparency requirements
* Long procurement cycles
* Preference for mature enterprise platforms

| Evaluation Category                   | Weight |
| ------------------------------------- | -----: |
| Core Agent Intelligence               |    15% |
| Agent Architecture & Development      |    10% |
| Enterprise Integration & Deployment   |    20% |
| Governance, Security & Trust          |    40% |
| Enterprise Readiness & Business Value |    15% |

---

# Mode 2 – Custom Weight Profiles

While predefined personas cover common business scenarios, enterprise clients often have unique priorities that do not align perfectly with a standard profile.

To support these situations, consultants can create a custom weighting profile by assigning their own weights to each evaluation category.

### Example

| Evaluation Category                   | Weight |
| ------------------------------------- | -----: |
| Core Agent Intelligence               |    30% |
| Agent Architecture & Development      |    20% |
| Enterprise Integration & Deployment   |    15% |
| Governance, Security & Trust          |    25% |
| Enterprise Readiness & Business Value |    10% |

The system validates that the total weight equals **100%** before recalculating vendor rankings.

Custom profiles allow consultants to accurately reflect client priorities without modifying the underlying vendor evaluation data.

---

# Recommendation Workflow

The recommendation process follows these steps:

1. Select an evaluation domain.
2. Choose either:

   * a predefined client persona, or
   * a custom weighting profile.
3. Apply the selected category weights.
4. Calculate weighted vendor scores.
5. Rank vendors based on the weighted results.
6. Display recommendations with transparent score breakdowns.

---

# Design Principles

The weighting framework follows these principles:

* Vendor scores remain objective and independent of client preferences.
* Weighting affects only the final recommendation, not the underlying evaluation.
* Category-level weighting simplifies dashboard interaction and improves explainability.
* Consultants can quickly switch between predefined personas or create custom profiles without changing the scoring methodology.
* The framework supports future expansion through additional personas or reusable weight profiles.

---

# Future Enhancements

Future versions of the framework may include:

* Saving custom weight profiles for reuse.
* Department-specific weighting templates.
* Side-by-side comparison of multiple weighting profiles.
* AI-assisted weight recommendations based on client requirements.
* Importing weighting profiles from external configuration files.
