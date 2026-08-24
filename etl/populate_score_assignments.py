"""
STEP 21B.2 - POPULATE APPROVED SCORE ASSIGNMENTS

Purpose:
    Populate config/score_assignments.csv using the approved
    vendor-criterion scores from the evaluation process.

Input:
    data/cleaned/vendor_evaluation_cleaned.csv

Output:
    config/score_assignments.csv

The script validates:
    - Expected vendors
    - Expected criteria
    - Exactly 136 vendor-criterion combinations
    - No duplicate assignments
    - Valid evaluation statuses
    - Valid 1-5 scores for evaluated criteria
    - Correct N/A handling
"""

from pathlib import Path
import pandas as pd


# ============================================================
# PATH CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

EVIDENCE_FILE = (
    PROJECT_ROOT
    / "data"
    / "cleaned"
    / "vendor_evaluation_cleaned.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "config"
    / "score_assignments.csv"
)


# ============================================================
# EXPECTED VENDORS
# ============================================================

EXPECTED_VENDORS = [
    "C3.ai",
    "GCP",
    "Glean AI",
    "K2view",
    "Salesforce",
    "ServiceNow",
    "Signzy",
    "Writer AI",
]


# ============================================================
# EXPECTED CRITERIA
# ============================================================

EXPECTED_CRITERIA = [
    "Autonomy",
    "Learning & Adaptability",
    "Memory & Context Management",
    "Planning & Reasoning",
    "Workflow Orchestration",
    "Agent Creation (Low-Code / No-Code)",
    "Ease of Development",
    "LLM Agnosticism / Model Flexibility",
    "Multi-Agent Collaboration",
    "Deployment Flexibility",
    "Tool & API Integration",
    "Governance & Security",
    "Human-in-the-Loop (HITL)",
    "Observability & Explainability",
    "Business Domain Fit",
    "Business Value / ROI",
    "Scalability",
]


# ============================================================
# APPROVED SCORES
# ============================================================

APPROVED_SCORES = {

    # --------------------------------------------------------
    # C3.ai
    # --------------------------------------------------------

    "C3.ai": {
        "Autonomy": 5,
        "Learning & Adaptability": 4,
        "Memory & Context Management": 4,
        "Planning & Reasoning": 5,
        "Workflow Orchestration": 5,
        "Agent Creation (Low-Code / No-Code)": 5,
        "Ease of Development": 5,
        "LLM Agnosticism / Model Flexibility": 5,
        "Multi-Agent Collaboration": 5,
        "Deployment Flexibility": 5,
        "Tool & API Integration": 5,
        "Governance & Security": 5,
        "Human-in-the-Loop (HITL)": 5,
        "Observability & Explainability": 5,
        "Business Domain Fit": 5,
        "Business Value / ROI": 5,
        "Scalability": 5,
    },

    # --------------------------------------------------------
    # GCP
    # --------------------------------------------------------

    "GCP": {
        "Autonomy": 5,
        "Learning & Adaptability": 4,
        "Memory & Context Management": 5,
        "Planning & Reasoning": 5,
        "Workflow Orchestration": 5,
        "Agent Creation (Low-Code / No-Code)": 5,
        "Ease of Development": 5,
        "LLM Agnosticism / Model Flexibility": 4,
        "Multi-Agent Collaboration": 5,
        "Deployment Flexibility": 4,
        "Tool & API Integration": 5,
        "Governance & Security": 5,
        "Human-in-the-Loop (HITL)": 5,
        "Observability & Explainability": 4,
        "Business Domain Fit": 4,
        "Business Value / ROI": 4,
        "Scalability": 5,
    },

    # --------------------------------------------------------
    # Glean AI
    # --------------------------------------------------------

    "Glean AI": {
        "Autonomy": 5,
        "Learning & Adaptability": 3,
        "Memory & Context Management": 5,
        "Planning & Reasoning": 5,
        "Workflow Orchestration": 5,
        "Agent Creation (Low-Code / No-Code)": 5,
        "Ease of Development": 4,
        "LLM Agnosticism / Model Flexibility": 5,
        "Multi-Agent Collaboration": 5,
        "Deployment Flexibility": 4,
        "Tool & API Integration": 5,
        "Governance & Security": 5,
        "Human-in-the-Loop (HITL)": 5,
        "Observability & Explainability": 4,
        "Business Domain Fit": 5,
        "Business Value / ROI": 4,
        "Scalability": 5,
    },

    # --------------------------------------------------------
    # K2view
    # --------------------------------------------------------

    "K2view": {
        "Autonomy": 4,
        "Learning & Adaptability": 3,
        "Memory & Context Management": 5,
        "Planning & Reasoning": 4,
        "Workflow Orchestration": 5,
        "Agent Creation (Low-Code / No-Code)": 4,
        "Ease of Development": 4,
        "LLM Agnosticism / Model Flexibility": 5,
        "Multi-Agent Collaboration": 4,
        "Deployment Flexibility": 5,
        "Tool & API Integration": 5,
        "Governance & Security": 5,
        "Human-in-the-Loop (HITL)": 4,
        "Observability & Explainability": 4,
        "Business Domain Fit": 5,
        "Business Value / ROI": 4,
        "Scalability": 5,
    },

    # --------------------------------------------------------
    # Salesforce
    # --------------------------------------------------------

    "Salesforce": {
        "Autonomy": 5,
        "Learning & Adaptability": 3,
        "Memory & Context Management": 4,
        "Planning & Reasoning": 5,
        "Workflow Orchestration": 5,
        "Agent Creation (Low-Code / No-Code)": 5,
        "Ease of Development": 5,
        "LLM Agnosticism / Model Flexibility": 5,
        "Multi-Agent Collaboration": 4,
        "Deployment Flexibility": 4,
        "Tool & API Integration": 5,
        "Governance & Security": 5,
        "Human-in-the-Loop (HITL)": 5,
        "Observability & Explainability": 4,
        "Business Domain Fit": 5,
        "Business Value / ROI": 4,
        "Scalability": 5,
    },

    # --------------------------------------------------------
    # ServiceNow
    # --------------------------------------------------------

    "ServiceNow": {
        "Autonomy": 5,
        "Learning & Adaptability": 4,
        "Memory & Context Management": 5,
        "Planning & Reasoning": 5,
        "Workflow Orchestration": 5,
        "Agent Creation (Low-Code / No-Code)": 5,
        "Ease of Development": 5,
        "LLM Agnosticism / Model Flexibility": 4,
        "Multi-Agent Collaboration": 5,
        "Deployment Flexibility": 4,
        "Tool & API Integration": 5,
        "Governance & Security": 5,
        "Human-in-the-Loop (HITL)": 5,
        "Observability & Explainability": 4,
        "Business Domain Fit": 5,
        "Business Value / ROI": 4,
        "Scalability": 5,
    },

    # --------------------------------------------------------
    # Signzy
    # --------------------------------------------------------

    "Signzy": {
        "Autonomy": 4,
        "Learning & Adaptability": None,
        "Memory & Context Management": None,
        "Planning & Reasoning": None,
        "Workflow Orchestration": 4,
        "Agent Creation (Low-Code / No-Code)": None,
        "Ease of Development": 3,
        "LLM Agnosticism / Model Flexibility": None,
        "Multi-Agent Collaboration": None,
        "Deployment Flexibility": 3,
        "Tool & API Integration": 5,
        "Governance & Security": 5,
        "Human-in-the-Loop (HITL)": 4,
        "Observability & Explainability": 3,
        "Business Domain Fit": 5,
        "Business Value / ROI": 4,
        "Scalability": 4,
    },

    # --------------------------------------------------------
    # Writer AI
    # --------------------------------------------------------

    "Writer AI": {
        "Autonomy": 5,
        "Learning & Adaptability": 4,
        "Memory & Context Management": 5,
        "Planning & Reasoning": 5,
        "Workflow Orchestration": 5,
        "Agent Creation (Low-Code / No-Code)": 5,
        "Ease of Development": 5,
        "LLM Agnosticism / Model Flexibility": 4,
        "Multi-Agent Collaboration": 5,
        "Deployment Flexibility": 4,
        "Tool & API Integration": 5,
        "Governance & Security": 5,
        "Human-in-the-Loop (HITL)": 4,
        "Observability & Explainability": 4,
        "Business Domain Fit": 5,
        "Business Value / ROI": 4,
        "Scalability": 5,
    },
}


# ============================================================
# VALIDATION FUNCTIONS
# ============================================================

def validate_structure(evidence_df):
    """Validate the cleaned evidence dataset."""

    required_columns = [
        "Vendor",
        "Evaluation Criterion",
        "Evaluation Notes",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in evidence_df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Evidence dataset is missing columns: {missing_columns}"
        )

    print("[PASS] Evidence dataset structure")


def validate_vendor_coverage():
    """Validate that all expected vendors have assignments."""

    actual_vendors = set(APPROVED_SCORES.keys())
    expected_vendors = set(EXPECTED_VENDORS)

    if actual_vendors != expected_vendors:
        missing = expected_vendors - actual_vendors
        extra = actual_vendors - expected_vendors

        raise ValueError(
            f"Vendor mismatch. Missing={missing}, Extra={extra}"
        )

    print("[PASS] All 8 vendors present")


def validate_criteria_coverage():
    """Validate that every vendor has all 17 criteria."""

    errors = []

    for vendor in EXPECTED_VENDORS:

        vendor_criteria = set(
            APPROVED_SCORES[vendor].keys()
        )

        expected = set(EXPECTED_CRITERIA)

        missing = expected - vendor_criteria
        extra = vendor_criteria - expected

        if missing:
            errors.append(
                f"{vendor}: missing criteria {sorted(missing)}"
            )

        if extra:
            errors.append(
                f"{vendor}: unexpected criteria {sorted(extra)}"
            )

    if errors:
        for error in errors:
            print(f"[FAIL] {error}")

        raise ValueError(
            "Criteria coverage validation failed."
        )

    print("[PASS] All vendors contain all 17 criteria")


def validate_scores():
    """Validate scores and N/A values."""

    errors = []

    for vendor in EXPECTED_VENDORS:

        for criterion in EXPECTED_CRITERIA:

            score = APPROVED_SCORES[vendor][criterion]

            # N/A
            if score is None:
                continue

            # Numeric score
            if score not in {1, 2, 3, 4, 5}:
                errors.append(
                    f"{vendor} / {criterion}: invalid score {score}"
                )

    if errors:

        for error in errors:
            print(f"[FAIL] {error}")

        raise ValueError(
            "Score validation failed."
        )

    print("[PASS] All scores are valid")


def build_assignment_dataframe(evidence_df):
    """
    Build the completed assignment dataframe.

    Evidence is used to retrieve the corresponding
    Evaluation Notes for score justification.
    """

    records = []

    for vendor in EXPECTED_VENDORS:

        vendor_evidence = evidence_df[
            evidence_df["Vendor"] == vendor
        ].copy()

        for criterion in EXPECTED_CRITERIA:

            score = APPROVED_SCORES[vendor][criterion]

            matching_rows = vendor_evidence[
                vendor_evidence["Evaluation Criterion"]
                == criterion
            ]

            if len(matching_rows) != 1:

                raise ValueError(
                    f"Expected exactly one evidence record for "
                    f"{vendor} / {criterion}, "
                    f"found {len(matching_rows)}."
                )

            evidence_row = matching_rows.iloc[0]

            evaluation_notes = evidence_row[
                "Evaluation Notes"
            ]

            # ------------------------------------------------
            # N/A RECORD
            # ------------------------------------------------

            if score is None:

                status = "Not Evaluated"
                assigned_score = "N/A"

                justification = (
                    "Insufficient publicly available evidence "
                    "to evaluate this criterion. "
                    f"Source evaluation note: {evaluation_notes}"
                )

            # ------------------------------------------------
            # EVALUATED RECORD
            # ------------------------------------------------

            else:

                status = "Evaluated"
                assigned_score = score

                justification = (
                    f"Assigned score of {score} based on the "
                    f"documented evidence for this criterion. "
                    f"{evaluation_notes}"
                )

            records.append(
                {
                    "Vendor": vendor,
                    "Evaluation Criterion": criterion,
                    "Evaluation Status": status,
                    "Assigned Score": assigned_score,
                    "Score Justification": justification,
                }
            )

    return pd.DataFrame(records)


def validate_final_assignments(df):
    """Validate the completed assignment dataframe."""

    errors = []

    # --------------------------------------------------------
    # Row count
    # --------------------------------------------------------

    if len(df) != 136:
        errors.append(
            f"Expected 136 rows, found {len(df)}"
        )

    # --------------------------------------------------------
    # Duplicate combinations
    # --------------------------------------------------------

    duplicates = df.duplicated(
        subset=["Vendor", "Evaluation Criterion"]
    )

    if duplicates.any():

        duplicate_rows = df.loc[
            duplicates,
            ["Vendor", "Evaluation Criterion"]
        ]

        errors.append(
            "Duplicate vendor-criterion combinations found: "
            f"{duplicate_rows.to_dict('records')}"
        )

    # --------------------------------------------------------
    # Status validation
    # --------------------------------------------------------

    valid_statuses = {
        "Evaluated",
        "Not Evaluated",
    }

    invalid_statuses = set(
        df["Evaluation Status"].dropna()
    ) - valid_statuses

    if invalid_statuses:
        errors.append(
            f"Invalid evaluation statuses: "
            f"{sorted(invalid_statuses)}"
        )

    # --------------------------------------------------------
    # Score validation
    # --------------------------------------------------------

    for index, row in df.iterrows():

        status = row["Evaluation Status"]
        score = row["Assigned Score"]

        if status == "Evaluated":

            if score not in {1, 2, 3, 4, 5}:

                errors.append(
                    f"Row {index + 2}: evaluated record "
                    f"has invalid score {score}"
                )

        elif status == "Not Evaluated":

            if str(score).strip().upper() != "N/A":

                errors.append(
                    f"Row {index + 2}: N/A record must "
                    f"have Assigned Score = N/A"
                )

    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    for column in [
        "Vendor",
        "Evaluation Criterion",
        "Evaluation Status",
        "Assigned Score",
        "Score Justification",
    ]:

        missing_count = df[column].isna().sum()

        if missing_count > 0:

            errors.append(
                f"{column}: {missing_count} missing values"
            )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    if errors:

        print("\nVALIDATION ERRORS:")

        for error in errors:
            print(f"  [FAIL] {error}")

        raise ValueError(
            f"\nFound {len(errors)} assignment validation error(s)."
        )

    print("[PASS] Final assignment validation")


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("STEP 21B.2 - POPULATE APPROVED SCORE ASSIGNMENTS")
    print("=" * 60)
    print()

    # --------------------------------------------------------
    # Load evidence
    # --------------------------------------------------------

    if not EVIDENCE_FILE.exists():

        raise FileNotFoundError(
            f"Evidence dataset not found:\n{EVIDENCE_FILE}"
        )

    evidence_df = pd.read_csv(
        EVIDENCE_FILE
    )

    print(
        f"Loaded evidence dataset: "
        f"{len(evidence_df)} rows"
    )

    # --------------------------------------------------------
    # Validate source data
    # --------------------------------------------------------

    validate_structure(evidence_df)
    validate_vendor_coverage()
    validate_criteria_coverage()
    validate_scores()

    # --------------------------------------------------------
    # Build assignments
    # --------------------------------------------------------

    assignments_df = build_assignment_dataframe(
        evidence_df
    )

    print()
    print(
        f"Generated assignments: "
        f"{len(assignments_df)} rows"
    )

    # --------------------------------------------------------
    # Validate final assignments
    # --------------------------------------------------------

    validate_final_assignments(
        assignments_df
    )

    # --------------------------------------------------------
    # Create output directory
    # --------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    assignments_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    evaluated_count = (
        assignments_df["Evaluation Status"]
        == "Evaluated"
    ).sum()

    not_evaluated_count = (
        assignments_df["Evaluation Status"]
        == "Not Evaluated"
    ).sum()

    print()
    print("-" * 60)
    print("ASSIGNMENT SUMMARY")
    print("-" * 60)

    print(
        f"Total assignments:       {len(assignments_df)}"
    )

    print(
        f"Evaluated:                {evaluated_count}"
    )

    print(
        f"Not Evaluated (N/A):      {not_evaluated_count}"
    )

    print()
    print("Vendor assignment counts:")

    vendor_counts = (
        assignments_df["Vendor"]
        .value_counts()
        .sort_index()
    )

    for vendor, count in vendor_counts.items():

        print(
            f"  {vendor:<15} {count}"
        )

    print()
    print("-" * 60)
    print("FINAL STATUS: PASS")
    print("-" * 60)

    print(
        f"Output file: {OUTPUT_FILE}"
    )

    print()
    print(
        "Step 21B.2 population completed successfully."
    )


if __name__ == "__main__":
    main()