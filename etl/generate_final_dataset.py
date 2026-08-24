"""
STEP 22 - GENERATE FINAL STRUCTURED DATASET

Purpose:
    Transform the validated vendor scoring dataset into a
    final database-ready structured dataset.

Input:
    data/processed/vendor_criterion_scoring.csv

Output:
    data/processed/final_vendor_evaluation_dataset.csv

The final dataset:
    - preserves vendor evidence
    - preserves scoring information
    - creates stable vendor/category/criterion/evaluation IDs
    - standardizes column names
    - validates uniqueness and completeness
    - prepares the dataset for SQL loading in Step 23
"""

from pathlib import Path
import pandas as pd


# ============================================================
# PATH CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "vendor_criterion_scoring.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "final_vendor_evaluation_dataset.csv"
)


# ============================================================
# EXPECTED STRUCTURE
# ============================================================

REQUIRED_COLUMNS = [
    "Vendor",
    "Evaluation Category",
    "Evaluation Criterion",
    "Evaluation Status",
    "Assigned Score",
    "Rating",
    "Score Justification",
    "Evidence Summary",
    "Source Type",
    "Source URL",
    "Evidence Confidence",
    "Evaluation Notes",
]


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
# VALIDATION
# ============================================================

def validate_input_structure(df):
    """Validate the input scoring dataset."""

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    print("[PASS] Required columns present")


def validate_row_count(df):
    """Validate expected total record count."""

    if len(df) != 136:
        raise ValueError(
            f"Expected 136 records, found {len(df)}"
        )

    print("[PASS] Total row count: 136")


def validate_vendor_coverage(df):
    """Validate vendor coverage."""

    actual_vendors = set(df["Vendor"].unique())
    expected_vendors = set(EXPECTED_VENDORS)

    missing = expected_vendors - actual_vendors
    extra = actual_vendors - expected_vendors

    if missing:
        raise ValueError(
            f"Missing vendors: {sorted(missing)}"
        )

    if extra:
        raise ValueError(
            f"Unexpected vendors: {sorted(extra)}"
        )

    vendor_counts = df["Vendor"].value_counts()

    invalid_counts = vendor_counts[
        vendor_counts != 17
    ]

    if not invalid_counts.empty:
        raise ValueError(
            "Invalid vendor record counts:\n"
            f"{invalid_counts}"
        )

    print("[PASS] Vendor coverage: 8 vendors × 17 criteria")


def validate_criterion_coverage(df):
    """Validate criterion coverage."""

    actual_criteria = set(
        df["Evaluation Criterion"].unique()
    )

    expected_criteria = set(
        EXPECTED_CRITERIA
    )

    missing = expected_criteria - actual_criteria
    extra = actual_criteria - expected_criteria

    if missing:
        raise ValueError(
            f"Missing criteria: {sorted(missing)}"
        )

    if extra:
        raise ValueError(
            f"Unexpected criteria: {sorted(extra)}"
        )

    print("[PASS] All 17 evaluation criteria present")


def validate_uniqueness(df):
    """Validate vendor-criterion uniqueness."""

    duplicate_count = df.duplicated(
        subset=[
            "Vendor",
            "Evaluation Criterion",
        ]
    ).sum()

    if duplicate_count > 0:
        raise ValueError(
            f"Found {duplicate_count} duplicate "
            "vendor-criterion combinations."
        )

    print("[PASS] Vendor-criterion uniqueness")


def validate_status_and_scores(df):
    """Validate evaluation statuses and assigned scores."""

    valid_statuses = {
        "Evaluated",
        "Not Evaluated",
    }

    actual_statuses = set(
        df["Evaluation Status"].dropna().unique()
    )

    invalid_statuses = (
        actual_statuses - valid_statuses
    )

    if invalid_statuses:
        raise ValueError(
            f"Invalid evaluation statuses: "
            f"{sorted(invalid_statuses)}"
        )

    # Evaluated records must have scores 1–5
    evaluated = df[
        df["Evaluation Status"] == "Evaluated"
    ]

    invalid_scores = evaluated[
        ~evaluated["Assigned Score"].isin(
            [1, 2, 3, 4, 5]
        )
    ]

    if not invalid_scores.empty:
        raise ValueError(
            "Evaluated records contain invalid scores."
        )

    # Not Evaluated records must not have scores
    not_evaluated = df[
        df["Evaluation Status"] == "Not Evaluated"
    ]

    if not_evaluated["Assigned Score"].notna().any():
        raise ValueError(
            "Not Evaluated records contain numeric scores."
        )

    print("[PASS] Evaluation statuses and scores")


def validate_required_values(df):
    """Check important fields for missing values."""

    fields_that_must_exist = [
        "Vendor",
        "Evaluation Category",
        "Evaluation Criterion",
        "Evaluation Status",
        "Score Justification",
        "Evidence Summary",
        "Source Type",
        "Evidence Confidence",
        "Evaluation Notes",
    ]

    errors = []

    for column in fields_that_must_exist:

        missing_count = df[column].isna().sum()

        if missing_count > 0:
            errors.append(
                f"{column}: {missing_count} missing values"
            )

    if errors:

        for error in errors:
            print(f"[FAIL] {error}")

        raise ValueError(
            "Required-value validation failed."
        )

    print("[PASS] Required field completeness")


# ============================================================
# ID CREATION
# ============================================================

def create_id_mappings(df):
    """
    Create stable IDs for vendors, categories and criteria.
    """

    # --------------------------------------------------------
    # Vendor IDs
    # --------------------------------------------------------

    vendor_order = EXPECTED_VENDORS

    vendor_mapping = {
        vendor: f"V{i:03d}"
        for i, vendor in enumerate(
            vendor_order,
            start=1
        )
    }

    # --------------------------------------------------------
    # Category IDs
    # --------------------------------------------------------

    categories = (
        df[
            [
                "Evaluation Category"
            ]
        ]
        .drop_duplicates()
        .sort_values(
            "Evaluation Category"
        )[
            "Evaluation Category"
        ]
        .tolist()
    )

    category_mapping = {
        category: f"CAT{i:02d}"
        for i, category in enumerate(
            categories,
            start=1
        )
    }

    # --------------------------------------------------------
    # Criterion IDs
    # --------------------------------------------------------

    criterion_mapping = {
        criterion: f"C{i:02d}"
        for i, criterion in enumerate(
            EXPECTED_CRITERIA,
            start=1
        )
    }

    return (
        vendor_mapping,
        category_mapping,
        criterion_mapping,
    )


# ============================================================
# BUILD FINAL DATASET
# ============================================================

def build_final_dataset(df):
    """Create the final structured dataset."""

    (
        vendor_mapping,
        category_mapping,
        criterion_mapping,
    ) = create_id_mappings(df)

    final_df = pd.DataFrame()

    # --------------------------------------------------------
    # Evaluation ID
    # --------------------------------------------------------

    final_df["evaluation_id"] = [
        f"E{i:04d}"
        for i in range(
            1,
            len(df) + 1
        )
    ]

    # --------------------------------------------------------
    # Vendor
    # --------------------------------------------------------

    final_df["vendor_id"] = (
        df["Vendor"]
        .map(vendor_mapping)
    )

    final_df["vendor"] = df["Vendor"]

    # --------------------------------------------------------
    # Category
    # --------------------------------------------------------

    final_df["category_id"] = (
        df["Evaluation Category"]
        .map(category_mapping)
    )

    final_df["evaluation_category"] = (
        df["Evaluation Category"]
    )

    # --------------------------------------------------------
    # Criterion
    # --------------------------------------------------------

    final_df["criterion_id"] = (
        df["Evaluation Criterion"]
        .map(criterion_mapping)
    )

    final_df["evaluation_criterion"] = (
        df["Evaluation Criterion"]
    )

    # --------------------------------------------------------
    # Scoring
    # --------------------------------------------------------

    final_df["evaluation_status"] = (
        df["Evaluation Status"]
    )

    final_df["assigned_score"] = (
        pd.to_numeric(
            df["Assigned Score"],
            errors="coerce",
        )
    )

    final_df["rating"] = df["Rating"]

    final_df["score_justification"] = (
        df["Score Justification"]
    )

    # --------------------------------------------------------
    # Evidence
    # --------------------------------------------------------

    final_df["evidence_summary"] = (
        df["Evidence Summary"]
    )

    final_df["source_type"] = (
        df["Source Type"]
    )

    final_df["source_url"] = (
        df["Source URL"]
    )

    final_df["evidence_confidence"] = (
        df["Evidence Confidence"]
    )

    final_df["evaluation_notes"] = (
        df["Evaluation Notes"]
    )

    return final_df


# ============================================================
# VALIDATE FINAL DATASET
# ============================================================

def validate_final_dataset(df):
    """Validate the generated final dataset."""

    expected_columns = [
        "evaluation_id",
        "vendor_id",
        "vendor",
        "category_id",
        "evaluation_category",
        "criterion_id",
        "evaluation_criterion",
        "evaluation_status",
        "assigned_score",
        "rating",
        "score_justification",
        "evidence_summary",
        "source_type",
        "source_url",
        "evidence_confidence",
        "evaluation_notes",
    ]

    # --------------------------------------------------------
    # Column validation
    # --------------------------------------------------------

    if list(df.columns) != expected_columns:

        raise ValueError(
            "Final dataset columns do not match "
            "the expected structure."
        )

    print("[PASS] Final column structure")

    # --------------------------------------------------------
    # Row count
    # --------------------------------------------------------

    if len(df) != 136:

        raise ValueError(
            f"Expected 136 rows, found {len(df)}"
        )

    print("[PASS] Final row count")

    # --------------------------------------------------------
    # ID uniqueness
    # --------------------------------------------------------

    if df["evaluation_id"].duplicated().any():

        raise ValueError(
            "Duplicate evaluation IDs found."
        )

    if df["vendor_id"].isna().any():

        raise ValueError(
            "Missing vendor IDs found."
        )

    if df["category_id"].isna().any():

        raise ValueError(
            "Missing category IDs found."
        )

    if df["criterion_id"].isna().any():

        raise ValueError(
            "Missing criterion IDs found."
        )

    print("[PASS] ID generation and uniqueness")

    # --------------------------------------------------------
    # Vendor-criterion uniqueness
    # --------------------------------------------------------

    duplicates = df.duplicated(
        subset=[
            "vendor_id",
            "criterion_id",
        ]
    ).sum()

    if duplicates > 0:

        raise ValueError(
            f"Found {duplicates} duplicate "
            "vendor-criterion combinations."
        )

    print("[PASS] Final vendor-criterion uniqueness")

    # --------------------------------------------------------
    # Status counts
    # --------------------------------------------------------

    evaluated_count = (
        df["evaluation_status"]
        == "Evaluated"
    ).sum()

    not_evaluated_count = (
        df["evaluation_status"]
        == "Not Evaluated"
    ).sum()

    if (
        evaluated_count != 130
        or not_evaluated_count != 6
    ):

        raise ValueError(
            "Unexpected evaluation status counts."
        )

    print(
        "[PASS] Evaluation status counts "
        "(130 Evaluated / 6 N/A)"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("STEP 22 - GENERATE FINAL STRUCTURED DATASET")
    print("=" * 60)
    print()

    # --------------------------------------------------------
    # Check input
    # --------------------------------------------------------

    if not INPUT_FILE.exists():

        raise FileNotFoundError(
            f"Input file not found:\n{INPUT_FILE}"
        )

    # --------------------------------------------------------
    # Load scoring dataset
    # --------------------------------------------------------

    df = pd.read_csv(
        INPUT_FILE
    )

    print(
        f"Loaded scoring dataset: "
        f"{len(df)} rows × {len(df.columns)} columns"
    )

    print()

    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    validate_input_structure(df)
    validate_row_count(df)
    validate_vendor_coverage(df)
    validate_criterion_coverage(df)
    validate_uniqueness(df)
    validate_status_and_scores(df)
    validate_required_values(df)

    # --------------------------------------------------------
    # Build final dataset
    # --------------------------------------------------------

    final_df = build_final_dataset(df)

    print()
    print(
        f"Generated final dataset: "
        f"{len(final_df)} rows × "
        f"{len(final_df.columns)} columns"
    )

    # --------------------------------------------------------
    # Validate final dataset
    # --------------------------------------------------------

    validate_final_dataset(
        final_df
    )

    # --------------------------------------------------------
    # Save output
    # --------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    final_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print()
    print("-" * 60)
    print("FINAL DATASET SUMMARY")
    print("-" * 60)

    print(
        f"Rows:                    {len(final_df)}"
    )

    print(
        f"Columns:                 {len(final_df.columns)}"
    )

    print(
        f"Vendors:                 "
        f"{final_df['vendor'].nunique()}"
    )

    print(
        f"Categories:              "
        f"{final_df['evaluation_category'].nunique()}"
    )

    print(
        f"Criteria:                "
        f"{final_df['evaluation_criterion'].nunique()}"
    )

    print(
        f"Evaluated:               "
        f"{(final_df['evaluation_status'] == 'Evaluated').sum()}"
    )

    print(
        f"Not Evaluated:           "
        f"{(final_df['evaluation_status'] == 'Not Evaluated').sum()}"
    )

    print()
    print("-" * 60)
    print("FINAL STATUS: PASS")
    print("-" * 60)

    print(
        f"Output: {OUTPUT_FILE}"
    )

    print()
    print(
        "Step 22 completed successfully."
    )


if __name__ == "__main__":
    main()