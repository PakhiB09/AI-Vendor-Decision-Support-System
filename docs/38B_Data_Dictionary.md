---

### 2. File 2: `docs/38B_Data_Dictionary.md`

Copy and paste this content into `docs/38B_Data_Dictionary.md`:

```markdown
# Step 38B – Relational Database Data Dictionary

## Overview
This data dictionary details the schema structure, data types, constraints, and entity relationships within the `vendor_decision_support` MySQL database[cite: 2].

---

## Entity Field Specifications

### 1. `vendors` Table (Dimension)
| Column Name | Data Type | Key Type | Nullable | Description / Constraint |
| :--- | :--- | :---: | :---: | :--- |
| `vendor_id` | `VARCHAR(10)` | PK | No | Unique vendor identifier (`V001`–`V008`)[cite: 2] |
| `vendor_name` | `VARCHAR(100)` | Unique | No | Name of vendor (e.g., C3.ai, ServiceNow, GCP)[cite: 1, 2] |
| `primary_category`| `VARCHAR(100)` | - | No | Core software domain classification[cite: 1] |
| `website_url` | `VARCHAR(255)` | - | Yes | Official vendor corporate portal URL[cite: 1] |

### 2. `categories` Table (Dimension)
| Column Name | Data Type | Key Type | Nullable | Description / Constraint |
| :--- | :--- | :---: | :---: | :--- |
| `category_id` | `VARCHAR(10)` | PK | No | Unique evaluation category ID (`CAT01`–`CAT05`)[cite: 2] |
| `category_name` | `VARCHAR(100)` | - | No | Pillar name (e.g., Core Agent Intelligence)[cite: 1, 2] |

### 3. `criteria` Table (Dimension)
| Column Name | Data Type | Key Type | Nullable | Description / Constraint |
| :--- | :--- | :---: | :---: | :--- |
| `criterion_id` | `VARCHAR(10)` | PK | No | Unique criterion ID (`C01`–`C17`)[cite: 2] |
| `category_id` | `VARCHAR(10)` | FK | No | References `categories(category_id)`[cite: 2] |
| `criterion_name` | `VARCHAR(100)` | - | No | Name of specific technical criterion[cite: 1, 2] |

### 4. `evaluations` Table (Fact)
| Column Name | Data Type | Key Type | Nullable | Description / Constraint |
| :--- | :--- | :---: | :---: | :--- |
| `evaluation_id` | `VARCHAR(10)` | PK | No | Unique evaluation record ID (`E0001`–`E0136`)[cite: 2] |
| `vendor_id` | `VARCHAR(10)` | FK | No | References `vendors(vendor_id)`[cite: 2] |
| `criterion_id` | `VARCHAR(10)` | FK | No | References `criteria(criterion_id)`[cite: 2] |
| `evaluation_status`| `VARCHAR(20)` | - | No | `Evaluated` or `Not Evaluated`[cite: 1, 2] |
| `assigned_score` | `DECIMAL(3,2)` | - | Yes | Score value ($1.00\text{--}5.00$ or `NULL`)[cite: 1, 2] |
| `rating` | `VARCHAR(20)` | - | Yes | `Excellent`, `Strong`, `Adequate`, `Limited`, `Poor`, `N/A`[cite: 1, 2] |
| `score_justification`| `TEXT` | - | Yes | Detailed evidence rationale for score[cite: 1, 2] |
| `evidence_summary` | `TEXT` | - | Yes | Technical capability evidence notes[cite: 1, 2] |
| `source_type` | `VARCHAR(100)`| - | Yes | Official Docs, Developer Guides, Whitepapers[cite: 1, 2] |
| `source_url` | `TEXT` | - | Yes | Direct citation hyperlink(s)[cite: 1, 2] |
| `evidence_confidence`| `VARCHAR(20)`| - | Yes | `High`, `Medium`, `Low` confidence rating[cite: 1, 2] |

### 5. `personas` Table (Disconnected Dimension)
| Column Name | Data Type | Key Type | Nullable | Description / Constraint |
| :--- | :--- | :---: | :---: | :--- |
| `persona_id` | `VARCHAR(10)` | PK | No | Unique persona identifier (`P001`–`P005`)[cite: 2] |
| `persona_name` | `VARCHAR(100)` | - | No | Profile name (e.g., Financial Services)[cite: 2] |
| `persona_description`| `TEXT` | - | Yes | Business profile and risk characteristics[cite: 2] |

### 6. `persona_weights` Table (Disconnected Fact Bridge)
| Column Name | Data Type | Key Type | Nullable | Description / Constraint |
| :--- | :--- | :---: | :---: | :--- |
| `persona_id` | `VARCHAR(10)` | PK, FK | No | References `personas(persona_id)`[cite: 2] |
| `category_id` | `VARCHAR(10)` | PK, FK | No | References `categories(category_id)`[cite: 2] |
| `weight` | `DECIMAL(5,4)`| - | No | Weighting allocation ($0.0\text{--}1.0$; sums to $1.00$ per persona)[cite: 2] |