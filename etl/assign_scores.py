"""
Step 21B.2 - Reusable Score Assignment

Reads approved vendor-criterion score assignments,
validates them against the scoring rubric, maps scores
to ratings, and writes the final scored dataset.

The script is vendor-independent and can process all
vendors using the same logic.
"""

from pathlib import Path
import json

import pandas as pd


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ASSIGNMENT_FILE = (
    PROJECT_ROOT
    / "config"
    / "score_assignments.csv"
)

RUBRIC_FILE = (
    PROJECT_ROOT
    / "config"
    / "scoring_rubric.json"
)

EVIDENCE_FILE = (
    PROJECT_ROOT
    / "data"
    / "cleaned"
    / "vendor_evaluation_cleaned.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "vendor_criterion_scoring.csv"
)


# ---------------------------------------------------------
# REQUIRED COLUMNS
# ---------------------------------------------------------

ASSIGNMENT_COLUMNS = [
    "Vendor",
    "Evaluation Criterion",
    "Evaluation Status",
    "Assigned Score",
    "Score Justification",
]


EVIDENCE_COLUMNS = [
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
# LOAD RUBRIC
# ---------------------------------------------------------

def load_rubric():

    if not RUBRIC_FILE.exists():

        raise FileNotFoundError(
            f"Scoring rubric not found: {RUBRIC_FILE}"
        )

    with open(
        RUBRIC_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

def load_assignment_data():

    if not ASSIGNMENT_FILE.exists():

        raise FileNotFoundError(
            f"Score assignment file not found: "
            f"{ASSIGNMENT_FILE}"
        )

    return pd.read_csv(
        ASSIGNMENT_FILE,
        encoding="utf-8-sig"
    )


def load_evidence_data():

    if not EVIDENCE_FILE.exists():

        raise FileNotFoundError(
            f"Cleaned evidence file not found: "
            f"{EVIDENCE_FILE}"
        )

    return pd.read_csv(
        EVIDENCE_FILE,
        encoding="utf-8-sig"
    )


# ---------------------------------------------------------
# VALIDATE COLUMNS
# ---------------------------------------------------------

def validate_columns(df, required_columns, dataset_name):

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"{dataset_name} is missing columns: "
            + ", ".join(missing_columns)
        )


# ---------------------------------------------------------
# VALIDATE ASSIGNMENT STRUCTURE
# ---------------------------------------------------------

def validate_assignment_structure(assignments):

    duplicate_count = (
        assignments
        .duplicated(
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
            f"assignments found: {duplicate_count}"
        )


# ---------------------------------------------------------
# VALIDATE ASSIGNMENT VALUES
# ---------------------------------------------------------

def validate_assignment_values(
    assignments,
    rubric
):

    valid_statuses = set(
        rubric[
            "evaluation_statuses"
        ].values()
    )

    minimum_score = rubric[
        "scoring_scale"
    ][
        "minimum_score"
    ]

    maximum_score = rubric[
        "scoring_scale"
    ][
        "maximum_score"
    ]

    errors = []

    for index, row in assignments.iterrows():

        status = row[
            "Evaluation Status"
        ]

        score = row[
            "Assigned Score"
        ]

        justification = row[
            "Score Justification"
        ]

        # ---------------------------------------------
        # STATUS CHECK
        # ---------------------------------------------

        if pd.isna(status) or str(status).strip() == "":

            errors.append(
                f"Row {index + 2}: Evaluation Status is blank."
            )

            continue

        status = str(status).strip()

        if status not in valid_statuses:

            errors.append(
                f"Row {index + 2}: Invalid status '{status}'."
            )

            continue

        # ---------------------------------------------
        # JUSTIFICATION CHECK
        # ---------------------------------------------

        if (
            pd.isna(justification)
            or str(justification).strip() == ""
        ):

            errors.append(
                f"Row {index + 2}: "
                "Score Justification is blank."
            )

        # ---------------------------------------------
        # EVALUATED CHECK
        # ---------------------------------------------

        if status == "Evaluated":

            if pd.isna(score):

                errors.append(
                    f"Row {index + 2}: "
                    "Evaluated record has no score."
                )

                continue

            try:

                numeric_score = float(score)

            except ValueError:

                errors.append(
                    f"Row {index + 2}: "
                    f"Invalid score '{score}'."
                )

                continue

            if (
                numeric_score < minimum_score
                or numeric_score > maximum_score
                or numeric_score != int(numeric_score)
            ):

                errors.append(
                    f"Row {index + 2}: "
                    f"Score must be an integer from "
                    f"{minimum_score} to "
                    f"{maximum_score}."
                )

        # ---------------------------------------------
        # NOT EVALUATED CHECK
        # ---------------------------------------------

        elif status == "Not Evaluated":

            if not pd.isna(score):

                errors.append(
                    f"Row {index + 2}: "
                    "Not Evaluated record must have "
                    "a blank score."
                )

    if errors:

        print("\nVALIDATION ERRORS:")

        for error in errors:

            print(f"  [FAIL] {error}")

        raise ValueError(
            f"\nFound {len(errors)} assignment validation error(s)."
        )


# ---------------------------------------------------------
# CHECK ASSIGNMENTS AGAINST EVIDENCE
# ---------------------------------------------------------

def validate_vendor_criteria(
    assignments,
    evidence
):

    assignment_keys = set(
        zip(
            assignments["Vendor"],
            assignments["Evaluation Criterion"]
        )
    )

    evidence_keys = set(
        zip(
            evidence["Vendor"],
            evidence["Evaluation Criterion"]
        )
    )

    missing_assignments = (
        evidence_keys
        - assignment_keys
    )

    unexpected_assignments = (
        assignment_keys
        - evidence_keys
    )

    if missing_assignments:

        print("\n[FAIL] Missing score assignments:")

        for vendor, criterion in sorted(
            missing_assignments
        ):

            print(
                f"  - {vendor} | {criterion}"
            )

        raise ValueError(
            f"{len(missing_assignments)} "
            "vendor-criterion combinations "
            "have no assignment."
        )

    if unexpected_assignments:

        print("\n[FAIL] Unexpected assignments:")

        for vendor, criterion in sorted(
            unexpected_assignments
        ):

            print(
                f"  - {vendor} | {criterion}"
            )

        raise ValueError(
            f"{len(unexpected_assignments)} "
            "assignments do not exist in "
            "the evidence dataset."
        )


# ---------------------------------------------------------
# MAP SCORE TO RATING
# ---------------------------------------------------------

def map_score_to_rating(
    score,
    rubric
):

    if pd.isna(score):

        return "N/A"

    score_key = str(
        int(float(score))
    )

    return rubric[
        "ratings"
    ][
        score_key
    ][
        "rating"
    ]


# ---------------------------------------------------------
# CREATE FINAL DATASET
# ---------------------------------------------------------

def create_final_dataset(
    assignments,
    evidence,
    rubric
):

    scored = evidence.merge(
        assignments,
        on=[
            "Vendor",
            "Evaluation Criterion"
        ],
        how="left",
        validate="one_to_one"
    )

    # ---------------------------------------------
    # MAP SCORE TO RATING
    # ---------------------------------------------

    scored["Rating"] = scored[
        "Assigned Score"
    ].apply(
        lambda score:
        map_score_to_rating(
            score,
            rubric
        )
    )

    # ---------------------------------------------
    # ORDER COLUMNS
    # ---------------------------------------------

    column_order = [
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

    scored = scored[
        column_order
    ]

    return scored


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("STEP 21B.2 - REUSABLE SCORE ASSIGNMENT")
    print("=" * 60)

    # ---------------------------------------------
    # LOAD
    # ---------------------------------------------

    rubric = load_rubric()

    assignments = load_assignment_data()

    evidence = load_evidence_data()

    print(
        f"\nLoaded evidence dataset: "
        f"{len(evidence)} rows"
    )

    print(
        f"Loaded assignment dataset: "
        f"{len(assignments)} rows"
    )

    # ---------------------------------------------
    # COLUMN VALIDATION
    # ---------------------------------------------

    validate_columns(
        assignments,
        ASSIGNMENT_COLUMNS,
        "Score assignment dataset"
    )

    validate_columns(
        evidence,
        EVIDENCE_COLUMNS,
        "Evidence dataset"
    )

    print(
        "[PASS] Required columns present"
    )

    # ---------------------------------------------
    # STRUCTURE VALIDATION
    # ---------------------------------------------

    validate_assignment_structure(
        assignments
    )

    print(
        "[PASS] Assignment uniqueness"
    )

    # ---------------------------------------------
    # VALUE VALIDATION
    # ---------------------------------------------

    validate_assignment_values(
        assignments,
        rubric
    )

    print(
        "[PASS] Assignment values"
    )

    # ---------------------------------------------
    # VENDOR/CRITERION VALIDATION
    # ---------------------------------------------

    validate_vendor_criteria(
        assignments,
        evidence
    )

    print(
        "[PASS] Vendor-criterion coverage"
    )

    # ---------------------------------------------
    # CREATE FINAL DATASET
    # ---------------------------------------------

    scored = create_final_dataset(
        assignments,
        evidence,
        rubric
    )

    # ---------------------------------------------
    # FINAL ROW COUNT CHECK
    # ---------------------------------------------

    if len(scored) != len(evidence):

        raise ValueError(
            "Final dataset row count does not "
            "match evidence dataset."
        )

    print(
        "[PASS] Final row count"
    )

    # ---------------------------------------------
    # OUTPUT DIRECTORY
    # ---------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # ---------------------------------------------
    # SAVE
    # ---------------------------------------------

    scored.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    # ---------------------------------------------
    # SUMMARY
    # ---------------------------------------------

    evaluated_count = (
        scored[
            "Evaluation Status"
        ]
        == "Evaluated"
    ).sum()

    not_evaluated_count = (
        scored[
            "Evaluation Status"
        ]
        == "Not Evaluated"
    ).sum()

    print("\n" + "-" * 60)

    print(
        "SCORING DATASET CREATED"
    )

    print(
        f"Total records: {len(scored)}"
    )

    print(
        f"Evaluated: {evaluated_count}"
    )

    print(
        f"Not Evaluated: {not_evaluated_count}"
    )

    print(
        f"Output: {OUTPUT_FILE}"
    )

    print(
        "-" * 60
    )

    print(
        "\nStep 21B.2 completed successfully."
    )


# ---------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":
    main()