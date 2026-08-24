"""
Step 21B Layer 2 - Create Score Assignment Template

Creates a structured template for assigning an evidence-based
score to every Vendor + Evaluation Criterion combination.

The actual score is intentionally left blank until the
evaluation is performed against the scoring rubric.
"""

from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "cleaned"
    / "vendor_evaluation_cleaned.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "config"

OUTPUT_FILE = (
    OUTPUT_DIR
    / "score_assignments.csv"
)


# ---------------------------------------------------------
# REQUIRED INPUT COLUMNS
# ---------------------------------------------------------

REQUIRED_COLUMNS = [
    "Vendor",
    "Evaluation Criterion",
]


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("STEP 21B - LAYER 2 - CREATE SCORE ASSIGNMENT TEMPLATE")
    print("=" * 60)

    # -----------------------------------------------------
    # CHECK INPUT
    # -----------------------------------------------------

    if not INPUT_FILE.exists():

        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    # -----------------------------------------------------
    # LOAD CLEANED DATA
    # -----------------------------------------------------

    df = pd.read_csv(
        INPUT_FILE,
        encoding="utf-8-sig"
    )

    print(
        f"\nLoaded cleaned dataset: "
        f"{len(df)} rows"
    )

    # -----------------------------------------------------
    # VALIDATE REQUIRED COLUMNS
    # -----------------------------------------------------

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    # -----------------------------------------------------
    # CHECK VENDOR + CRITERION UNIQUENESS
    # -----------------------------------------------------

    duplicate_count = (
        df.duplicated(
            subset=[
                "Vendor",
                "Evaluation Criterion"
            ]
        )
        .sum()
    )

    if duplicate_count > 0:

        raise ValueError(
            "Duplicate Vendor + Evaluation Criterion "
            f"records found: {duplicate_count}"
        )

    # -----------------------------------------------------
    # CREATE ASSIGNMENT TEMPLATE
    # -----------------------------------------------------

    assignments = df[
        [
            "Vendor",
            "Evaluation Criterion"
        ]
    ].copy()

    assignments[
        "Evaluation Status"
    ] = ""

    assignments[
        "Assigned Score"
    ] = pd.NA

    assignments[
        "Score Justification"
    ] = ""

    # -----------------------------------------------------
    # CREATE OUTPUT DIRECTORY
    # -----------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # -----------------------------------------------------
    # SAVE TEMPLATE
    # -----------------------------------------------------

    assignments.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    # -----------------------------------------------------
    # OUTPUT SUMMARY
    # -----------------------------------------------------

    print(
        "\nScore assignment template created:"
    )

    print(
        f"  Rows: {len(assignments)}"
    )

    print(
        f"  Columns: {len(assignments.columns)}"
    )

    print(
        f"  Output: {OUTPUT_FILE}"
    )

    print(
        "\nAssignment fields:"
    )

    print(
        "  - Evaluation Status"
    )

    print(
        "  - Assigned Score"
    )

    print(
        "  - Score Justification"
    )

    print(
        "\nStep 21B Layer 2 template completed successfully."
    )


# ---------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":
    main()