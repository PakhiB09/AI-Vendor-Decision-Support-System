"""
Step 20 - Validate Data Quality and Completeness

Validates the cleaned vendor evaluation dataset before
the scoring stage.

Input:
    data/cleaned/vendor_evaluation_cleaned.csv

Output:
    outputs/data_quality_report.txt

The script does not modify the input dataset.
"""

from pathlib import Path
import re

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

OUTPUT_DIR = PROJECT_ROOT / "outputs"

REPORT_FILE = OUTPUT_DIR / "data_quality_report.txt"


# ---------------------------------------------------------
# PROJECT EXPECTATIONS
# ---------------------------------------------------------

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

EXPECTED_VENDOR_COUNT = len(EXPECTED_VENDORS)

EXPECTED_CRITERIA_PER_VENDOR = 17

EXPECTED_TOTAL_ROWS = (
    EXPECTED_VENDOR_COUNT
    * EXPECTED_CRITERIA_PER_VENDOR
)


EXPECTED_COLUMNS = [
    "Vendor",
    "Evaluation Category",
    "Evaluation Criterion",
    "Evidence Summary",
    "Source Type",
    "Source URL",
    "Evidence Confidence",
    "Evaluation Notes",
]


VALID_CONFIDENCE_VALUES = {
    "High",
    "Medium",
    "Low",
    "High / Medium",
    "Medium / Low",
}


# ---------------------------------------------------------
# VALIDATION STORAGE
# ---------------------------------------------------------

validation_results = []


def record_check(name, passed, details):
    """
    Store the result of one validation check.
    """

    validation_results.append(
        {
            "name": name,
            "passed": passed,
            "details": details,
        }
    )


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def is_blank(value):
    """
    Return True when a value is missing or blank.
    """

    if pd.isna(value):
        return True

    return str(value).strip() == ""


def contains_http_url(value):
    """
    Check whether a source field contains at least
    one HTTP/HTTPS URL.
    """

    if is_blank(value):
        return False

    value = str(value)

    pattern = r"https?://[^\s\]\)]+"

    return bool(re.search(pattern, value))


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

def load_dataset():
    """
    Load the cleaned dataset.
    """

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    try:
        df = pd.read_csv(
            INPUT_FILE,
            encoding="utf-8-sig"
        )
    except UnicodeDecodeError:
        df = pd.read_csv(
            INPUT_FILE,
            encoding="latin-1"
        )

    return df


# ---------------------------------------------------------
# CHECK 1 - FILE EXISTS
# ---------------------------------------------------------

def check_file_exists():
    """
    Confirm the cleaned dataset exists.
    """

    passed = INPUT_FILE.exists()

    record_check(
        "Cleaned dataset exists",
        passed,
        str(INPUT_FILE)
        if passed
        else "Input file does not exist.",
    )


# ---------------------------------------------------------
# CHECK 2 - REQUIRED COLUMNS
# ---------------------------------------------------------

def check_required_columns(df):
    """
    Confirm all required columns exist.
    """

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    passed = len(missing_columns) == 0

    if passed:
        details = (
            f"All {len(EXPECTED_COLUMNS)} required columns "
            "are present."
        )
    else:
        details = (
            "Missing columns: "
            + ", ".join(missing_columns)
        )

    record_check(
        "Required columns present",
        passed,
        details,
    )


# ---------------------------------------------------------
# CHECK 3 - TOTAL ROW COUNT
# ---------------------------------------------------------

def check_total_rows(df):
    """
    Confirm the expected number of evaluation records exists.
    """

    actual_rows = len(df)

    passed = actual_rows == EXPECTED_TOTAL_ROWS

    details = (
        f"Expected {EXPECTED_TOTAL_ROWS} rows; "
        f"found {actual_rows}."
    )

    record_check(
        "Total row count",
        passed,
        details,
    )


# ---------------------------------------------------------
# CHECK 4 - EXPECTED VENDORS
# ---------------------------------------------------------

def check_expected_vendors(df):
    """
    Confirm all expected vendors are present.
    """

    actual_vendors = sorted(
        df["Vendor"].dropna().unique().tolist()
    )

    expected_vendors = sorted(EXPECTED_VENDORS)

    missing_vendors = sorted(
        set(expected_vendors)
        - set(actual_vendors)
    )

    unexpected_vendors = sorted(
        set(actual_vendors)
        - set(expected_vendors)
    )

    passed = (
        len(missing_vendors) == 0
        and len(unexpected_vendors) == 0
    )

    if passed:
        details = (
            f"All {EXPECTED_VENDOR_COUNT} expected vendors "
            "are present."
        )
    else:
        details = (
            f"Missing vendors: {missing_vendors}; "
            f"Unexpected vendors: {unexpected_vendors}."
        )

    record_check(
        "Expected vendors present",
        passed,
        details,
    )


# ---------------------------------------------------------
# CHECK 5 - ROWS PER VENDOR
# ---------------------------------------------------------

def check_rows_per_vendor(df):
    """
    Confirm every vendor has exactly 17 evaluation records.
    """

    vendor_counts = (
        df["Vendor"]
        .value_counts()
        .to_dict()
    )

    incorrect_counts = {
        vendor: count
        for vendor, count in vendor_counts.items()
        if count != EXPECTED_CRITERIA_PER_VENDOR
    }

    missing_expected_vendors = {
        vendor: 0
        for vendor in EXPECTED_VENDORS
        if vendor not in vendor_counts
    }

    incorrect_counts.update(
        missing_expected_vendors
    )

    passed = len(incorrect_counts) == 0

    if passed:
        details = (
            "Every vendor contains exactly "
            f"{EXPECTED_CRITERIA_PER_VENDOR} records."
        )
    else:
        details = (
            "Incorrect vendor record counts: "
            + str(incorrect_counts)
        )

    record_check(
        "Records per vendor",
        passed,
        details,
    )


# ---------------------------------------------------------
# CHECK 6 - MISSING VALUES
# ---------------------------------------------------------

def check_missing_values(df):
    """
    Check all required columns for missing or blank values.
    """

    missing_summary = {}

    for column in EXPECTED_COLUMNS:

        missing_count = int(
            df[column].isna().sum()
        )

        blank_count = int(
            df[column]
            .astype(str)
            .str.strip()
            .eq("")
            .sum()
        )

        total_missing = (
            missing_count
            + blank_count
        )

        if total_missing > 0:
            missing_summary[column] = total_missing

    passed = len(missing_summary) == 0

    if passed:
        details = (
            "No missing or blank values found "
            "in required columns."
        )
    else:
        details = (
            "Missing/blank values detected: "
            + str(missing_summary)
        )

    record_check(
        "Missing value check",
        passed,
        details,
    )


# ---------------------------------------------------------
# CHECK 7 - DUPLICATE ROWS
# ---------------------------------------------------------

def check_duplicate_rows(df):
    """
    Check for completely duplicated records.
    """

    duplicate_count = int(
        df.duplicated().sum()
    )

    passed = duplicate_count == 0

    details = (
        f"Duplicate rows found: {duplicate_count}."
    )

    record_check(
        "Duplicate row check",
        passed,
        details,
    )


# ---------------------------------------------------------
# CHECK 8 - DUPLICATE VENDOR/CRITERION
# ---------------------------------------------------------

def check_duplicate_vendor_criteria(df):
    """
    Confirm each vendor has each criterion only once.
    """

    duplicate_mask = df.duplicated(
        subset=[
            "Vendor",
            "Evaluation Criterion",
        ],
        keep=False,
    )

    duplicate_count = int(
        duplicate_mask.sum()
    )

    passed = duplicate_count == 0

    if passed:
        details = (
            "No duplicate Vendor + Evaluation Criterion "
            "combinations found."
        )
    else:
        duplicate_records = (
            df.loc[
                duplicate_mask,
                [
                    "Vendor",
                    "Evaluation Criterion",
                ],
            ]
            .drop_duplicates()
            .to_dict("records")
        )

        details = (
            f"Duplicate combinations found: "
            f"{duplicate_records}"
        )

    record_check(
        "Vendor-criterion uniqueness",
        passed,
        details,
    )


# ---------------------------------------------------------
# CHECK 9 - CONSISTENT CRITERIA ACROSS VENDORS
# ---------------------------------------------------------

def check_criteria_consistency(df):
    """
    Confirm every vendor is evaluated against the same
    set of criteria.
    """

    criteria_by_vendor = {}

    for vendor in EXPECTED_VENDORS:

        vendor_data = df[
            df["Vendor"] == vendor
        ]

        criteria = set(
            vendor_data[
                "Evaluation Criterion"
            ]
            .dropna()
            .tolist()
        )

        criteria_by_vendor[vendor] = criteria

    reference_vendor = EXPECTED_VENDORS[0]

    reference_criteria = criteria_by_vendor[
        reference_vendor
    ]

    inconsistent_vendors = {}

    for vendor, criteria in criteria_by_vendor.items():

        if criteria != reference_criteria:

            missing = sorted(
                reference_criteria - criteria
            )

            extra = sorted(
                criteria - reference_criteria
            )

            inconsistent_vendors[vendor] = {
                "missing": missing,
                "extra": extra,
            }

    passed = len(inconsistent_vendors) == 0

    if passed:
        details = (
            "All vendors use the same set of "
            f"{len(reference_criteria)} evaluation criteria."
        )
    else:
        details = (
            "Criterion inconsistencies detected: "
            + str(inconsistent_vendors)
        )

    record_check(
        "Criteria consistency across vendors",
        passed,
        details,
    )


# ---------------------------------------------------------
# CHECK 10 - CATEGORY CONSISTENCY
# ---------------------------------------------------------

def check_category_consistency(df):
    """
    Confirm each criterion maps to one consistent category.
    """

    criterion_category_counts = (
        df.groupby(
            "Evaluation Criterion"
        )["Evaluation Category"]
        .nunique()
    )

    inconsistent = (
        criterion_category_counts[
            criterion_category_counts > 1
        ]
    )

    passed = len(inconsistent) == 0

    if passed:
        details = (
            "Every evaluation criterion maps to "
            "one consistent evaluation category."
        )
    else:
        details = (
            "Criteria mapped to multiple categories: "
            + str(inconsistent.to_dict())
        )

    record_check(
        "Criterion-category consistency",
        passed,
        details,
    )


# ---------------------------------------------------------
# CHECK 11 - EVIDENCE CONFIDENCE
# ---------------------------------------------------------

def check_confidence_values(df):
    """
    Confirm evidence confidence uses approved values.
    """

    actual_values = set(
        df["Evidence Confidence"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )

    invalid_values = sorted(
        actual_values
        - VALID_CONFIDENCE_VALUES
    )

    passed = len(invalid_values) == 0

    if passed:
        details = (
            "All Evidence Confidence values are valid: "
            + ", ".join(
                sorted(actual_values)
            )
        )
    else:
        details = (
            "Invalid confidence values: "
            + str(invalid_values)
        )

    record_check(
        "Evidence confidence values",
        passed,
        details,
    )


# ---------------------------------------------------------
# CHECK 12 - SOURCE URL
# ---------------------------------------------------------

def check_source_urls(df):
    """
    Validate source URLs.

    A valid HTTP/HTTPS URL is required when public evidence
    is available.

    A missing URL is allowed when the evidence explicitly
    states that the criterion was not publicly evaluated,
    provided the evidence confidence is Low.
    """

    invalid_rows = []
    accepted_no_source_rows = []

    for index, row in df.iterrows():

        source_url = row["Source URL"]
        evidence_summary = str(
            row["Evidence Summary"]
        ).strip().lower()
        confidence = str(
            row["Evidence Confidence"]
        ).strip()

        # -------------------------------------------------
        # Case 1: Valid HTTP/HTTPS URL
        # -------------------------------------------------

        if contains_http_url(source_url):
            continue

        # -------------------------------------------------
        # Case 2: No public evaluation available
        # -------------------------------------------------

        not_publicly_evaluated = (
            "not publicly evaluated"
            in evidence_summary
        )

        if (
            not_publicly_evaluated
            and confidence == "Low"
        ):
            accepted_no_source_rows.append(
                index + 2
            )
            continue

        # -------------------------------------------------
        # Case 3: Missing/invalid URL where one is expected
        # -------------------------------------------------

        invalid_rows.append(index + 2)

    passed = len(invalid_rows) == 0

    if passed:

        details = (
            "All records contain a valid HTTP/HTTPS URL "
            "or are explicitly documented as not publicly "
            "evaluated with Low confidence. "
            f"Accepted no-source records: "
            f"{len(accepted_no_source_rows)}."
        )

    else:

        details = (
            "Records without a valid source URL and "
            "without an approved no-public-evaluation "
            f"exception: {invalid_rows}"
        )

    record_check(
        "Source URL check",
        passed,
        details,
    )
    

# ---------------------------------------------------------
# CHECK 13 - EVIDENCE SUMMARY
# ---------------------------------------------------------

def check_evidence_summary(df):
    """
    Confirm every evaluation has evidence.
    """

    empty_rows = []

    for index, value in df["Evidence Summary"].items():

        if is_blank(value):
            empty_rows.append(index + 2)

    passed = len(empty_rows) == 0

    if passed:
        details = (
            "Every evaluation record contains "
            "an evidence summary."
        )
    else:
        details = (
            f"Records without evidence summaries: "
            f"{empty_rows}"
        )

    record_check(
        "Evidence summary completeness",
        passed,
        details,
    )


# ---------------------------------------------------------
# CHECK 14 - EVALUATION NOTES
# ---------------------------------------------------------

def check_evaluation_notes(df):
    """
    Confirm every evaluation has evaluation notes.
    """

    empty_rows = []

    for index, value in df["Evaluation Notes"].items():

        if is_blank(value):
            empty_rows.append(index + 2)

    passed = len(empty_rows) == 0

    if passed:
        details = (
            "Every evaluation record contains "
            "evaluation notes."
        )
    else:
        details = (
            f"Records without evaluation notes: "
            f"{empty_rows}"
        )

    record_check(
        "Evaluation notes completeness",
        passed,
        details,
    )


# ---------------------------------------------------------
# CHECK 15 - DATASET READY
# ---------------------------------------------------------

def check_overall_status():
    """
    Determine whether the dataset passed all checks.
    """

    failed_checks = [
        result
        for result in validation_results
        if not result["passed"]
    ]

    passed = len(failed_checks) == 0

    if passed:
        details = (
            "All validation checks passed. "
            "Dataset is ready for the scoring stage."
        )
    else:
        details = (
            f"{len(failed_checks)} validation check(s) failed."
        )

    record_check(
        "Overall dataset readiness",
        passed,
        details,
    )


# ---------------------------------------------------------
# REPORT GENERATION
# ---------------------------------------------------------

def generate_report(df):
    """
    Generate the human-readable validation report.
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    passed_count = sum(
        result["passed"]
        for result in validation_results
    )

    failed_count = len(
        validation_results
    ) - passed_count

    overall_passed = failed_count == 0

    report_lines = []

    report_lines.append(
        "=" * 70
    )
    report_lines.append(
        "STEP 20 - DATA QUALITY AND COMPLETENESS REPORT"
    )
    report_lines.append(
        "=" * 70
    )

    report_lines.append("")
    report_lines.append(
        f"Input file: {INPUT_FILE}"
    )

    report_lines.append(
        f"Rows checked: {len(df)}"
    )

    report_lines.append(
        f"Columns checked: {len(df.columns)}"
    )

    report_lines.append(
        f"Expected vendors: {EXPECTED_VENDOR_COUNT}"
    )

    report_lines.append(
        f"Expected criteria per vendor: "
        f"{EXPECTED_CRITERIA_PER_VENDOR}"
    )

    report_lines.append("")

    report_lines.append(
        "-" * 70
    )

    report_lines.append(
        "VALIDATION RESULTS"
    )

    report_lines.append(
        "-" * 70
    )

    for number, result in enumerate(
        validation_results,
        start=1,
    ):

        status = (
            "PASS"
            if result["passed"]
            else "FAIL"
        )

        report_lines.append(
            f"{number:02d}. [{status}] "
            f"{result['name']}"
        )

        report_lines.append(
            f"    {result['details']}"
        )

        report_lines.append("")

    report_lines.append(
        "-" * 70
    )

    report_lines.append(
        "SUMMARY"
    )

    report_lines.append(
        "-" * 70
    )

    report_lines.append(
        f"Checks passed: {passed_count}"
    )

    report_lines.append(
        f"Checks failed: {failed_count}"
    )

    report_lines.append("")

    if overall_passed:

        report_lines.append(
            "FINAL STATUS: PASS"
        )

        report_lines.append(
            "The cleaned dataset passed all data quality "
            "and completeness checks."
        )

        report_lines.append(
            "The dataset is ready for Step 21 scoring."
        )

    else:

        report_lines.append(
            "FINAL STATUS: FAIL"
        )

        report_lines.append(
            "The dataset should not proceed to scoring "
            "until the failed checks are resolved."
        )

    report_lines.append("")

    report_lines.append(
        "=" * 70
    )

    REPORT_FILE.write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("STEP 20 - VALIDATE DATA QUALITY")
    print("=" * 60)

    # Start with file check
    check_file_exists()

    if not INPUT_FILE.exists():

        generate_report(
            pd.DataFrame()
        )

        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    # Load dataset
    df = load_dataset()

    print(
        f"\nLoaded dataset: "
        f"{len(df)} rows × {len(df.columns)} columns"
    )

    # Run validation checks
    check_required_columns(df)

    # Only perform column-dependent checks if
    # the required columns exist.
    if all(
        column in df.columns
        for column in EXPECTED_COLUMNS
    ):

        check_total_rows(df)
        check_expected_vendors(df)
        check_rows_per_vendor(df)
        check_missing_values(df)
        check_duplicate_rows(df)
        check_duplicate_vendor_criteria(df)
        check_criteria_consistency(df)
        check_category_consistency(df)
        check_confidence_values(df)
        check_source_urls(df)
        check_evidence_summary(df)
        check_evaluation_notes(df)

    else:

        print(
            "\nRequired columns are missing."
        )

    # Overall status
    check_overall_status()

    # Generate report
    generate_report(df)

    # Print results
    print("\n" + "-" * 60)
    print("VALIDATION RESULTS")
    print("-" * 60)

    for result in validation_results:

        status = (
            "PASS"
            if result["passed"]
            else "FAIL"
        )

        print(
            f"[{status}] {result['name']}"
        )

    print("\n" + "-" * 60)

    failed_checks = [
        result
        for result in validation_results
        if not result["passed"]
    ]

    if not failed_checks:

        print(
            "FINAL STATUS: PASS"
        )

        print(
            "All data quality checks passed."
        )

        print(
            f"Report saved to: {REPORT_FILE}"
        )

        print(
            "\nStep 20 completed successfully."
        )

    else:

        print(
            "FINAL STATUS: FAIL"
        )

        print(
            f"Failed checks: {len(failed_checks)}"
        )

        print(
            f"Review the report: {REPORT_FILE}"
        )

        raise SystemExit(1)


# ---------------------------------------------------------
# SCRIPT ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":
    main()