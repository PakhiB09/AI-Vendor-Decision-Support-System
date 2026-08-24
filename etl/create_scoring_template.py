"""
Step 21A - Create Vendor Criterion Scoring Template

Creates a structured scoring template from the validated
cleaned vendor evaluation dataset.

The template contains one row per Vendor + Criterion pair.

Scores are intentionally left blank so that they can be
assigned against the documented 1-5 evaluation methodology.
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

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_FILE = (
    OUTPUT_DIR
    / "vendor_criterion_scoring.csv"
)


# ---------------------------------------------------------
# REQUIRED INPUT COLUMNS
# ---------------------------------------------------------

REQUIRED_COLUMNS = [
    "Vendor",
    "Evaluation Category",
    "Evaluation Criterion",
    "Evidence Summary",
    "Source Type",
    "Source URL",
    "Evidence Confidence",
    "Evaluation Notes",
]


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("STEP 21A - CREATE SCORING TEMPLATE")
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
    # VALIDATE INPUT COLUMNS
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
    # CREATE SCORING COLUMNS
    # -----------------------------------------------------

    df["Evaluation Status"] = ""

    df["Assigned Score"] = pd.NA

    df["Rating"] = ""

    df["Score Justification"] = ""

    # -----------------------------------------------------
    # REORDER COLUMNS
    # -----------------------------------------------------

    output_columns = [
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

    df = df[output_columns]

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

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    # -----------------------------------------------------
    # OUTPUT SUMMARY
    # -----------------------------------------------------

    print(
        f"Scoring template created:"
    )

    print(
        f"  Rows: {len(df)}"
    )

    print(
        f"  Columns: {len(df.columns)}"
    )

    print(
        f"  Output: {OUTPUT_FILE}"
    )

    print(
        "\nScoring columns created:"
    )

    print(
        "  - Evaluation Status"
    )

    print(
        "  - Assigned Score"
    )

    print(
        "  - Rating"
    )

    print(
        "  - Score Justification"
    )

    print(
        "\nStep 21A completed successfully."
    )


# ---------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":
    main()