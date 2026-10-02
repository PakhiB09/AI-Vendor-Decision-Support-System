# Step 38C – Evaluation & Scoring Methodology

## 1. Five-Point Normalized Evaluation Scale
Every vendor capability criterion is evaluated against empirical evidence and scored on a 5-point scale[cite: 1, 2]:

| Assigned Score | Rating | Definition |
| :---: | :--- | :--- |
| **5.0** | **Excellent** | Comprehensive enterprise-grade capability with full production support and verifiable documentation[cite: 1, 2]. |
| **4.0** | **Strong** | Robust implementation meeting all standard requirements with minor advanced capability limitations[cite: 1, 2]. |
| **3.0** | **Adequate** | Functional baseline capability requiring custom development or workaround configuration[cite: 1, 2]. |
| **2.0** | **Limited** | Partial implementation with significant functional constraints[cite: 1, 2]. |
| **1.0** | **Poor** | Minimal functionality or unverified marketing claim[cite: 1, 2]. |
| **N/A** | **Not Evaluated** | Insufficient public evidence available; excluded from calculation[cite: 1, 2]. |

---

## 2. Dynamic DAX Re-Weighting Formula
Vendor scoring is calculated dynamically at report runtime based on the active client persona selected in the user interface[cite: 2]:

$$\text{Category Score}_{c, v} = \text{AVERAGE}(\text{evaluations.assigned\_score}_{c, v})$$

$$\text{Total Weighted Score}_v = \sum_{c=1}^{5} \left( \text{Category Score}_{c, v} \times \text{Persona Weight}_{c, p} \right)$$

Where:
* $c$ represents one of the 5 evaluation categories (`CAT01`–`CAT05`)[cite: 2].
* $v$ represents the evaluated vendor (`V001`–`V008`)[cite: 2].
* $p$ represents the selected client persona scenario (`P001`–`P005`)[cite: 2].

---

## 3. Missing Data & N/A Handling Policy
To prevent unrated criteria from penalizing a vendor's standing, unverified capabilities are assigned `assigned_score = NULL` and `evaluation_status = 'Not Evaluated'`[cite: 1, 2]. 

The DAX `AVERAGE()` function automatically calculates category averages across evaluated criteria only, preserving score integrity without requiring artificial default values[cite: 2].