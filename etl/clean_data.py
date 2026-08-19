"""
Step 19 - Clean and Normalize Raw Vendor Evaluation Data

Reads all raw vendor CSV files from data/raw/,
standardizes their structure and text fields,
and writes one cleaned intermediate dataset
to data/cleaned/vendor_evaluation_cleaned.csv.
"""

from pathlib import Path
import re
import unicodedata

import pandas as pd


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_ROOT / "data" / "raw"
CLEANED_DIR = PROJECT_ROOT / "data" / "cleaned"

OUTPUT_FILE = CLEANED_DIR / "vendor_evaluation_cleaned.csv"


# ---------------------------------------------------------
# EXPECTED STANDARD COLUMNS
# ---------------------------------------------------------

STANDARD_COLUMNS = [
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
# COLUMN NAME NORMALIZATION
# ---------------------------------------------------------

COLUMN_ALIASES = {
    "vendor": "Vendor",
    "vendor name": "Vendor",
    "evaluation category": "Evaluation Category",
    "category": "Evaluation Category",
    "evaluation criterion": "Evaluation Criterion",
    "criterion": "Evaluation Criterion",
    "evidence summary": "Evidence Summary",
    "evidence": "Evidence Summary",
    "source type": "Source Type",
    "source": "Source Type",
    "source url": "Source URL",
    "url": "Source URL",
    "evidence confidence": "Evidence Confidence",
    "confidence": "Evidence Confidence",
    "evaluation notes": "Evaluation Notes",
    "notes": "Evaluation Notes",
}


# ---------------------------------------------------------
# TEXT CLEANING
# ---------------------------------------------------------

def clean_text(value):
    """
    Clean a text value without changing its meaning.
    """

    if pd.isna(value):
        return ""

    value = str(value)

    # Normalize Unicode characters
    value = unicodedata.normalize("NFKC", value)

    # Replace line breaks and tabs with spaces
    value = re.sub(r"[\r\n\t]+", " ", value)

    # Collapse multiple spaces
    value = re.sub(r"\s+", " ", value)

    # Remove leading/trailing whitespace
    value = value.strip()

    return value


# ---------------------------------------------------------
# COLUMN CLEANING
# ---------------------------------------------------------

def standardize_column_name(column_name):
    """
    Convert different column naming styles into
    the project's standard column names.
    """

    column_name = clean_text(column_name)

    normalized = column_name.lower()

    return COLUMN_ALIASES.get(normalized, column_name)


# ---------------------------------------------------------
# VENDOR NAME EXTRACTION
# ---------------------------------------------------------

def extract_vendor_name(file_path):
    """
    Extract vendor name from the raw filename.

    Example:
        c3ai_raw.csv -> C3.ai
        gcp_raw.csv -> GCP
        writerai_raw.csv -> Writer AI
    """

    filename = file_path.stem

    # Remove "_raw"
    vendor_key = re.sub(r"_raw$", "", filename, flags=re.IGNORECASE)

    vendor_mapping = {
        "c3ai": "C3.ai",
        "gcp": "GCP",
        "glean": "Glean AI",
        "k2view": "K2view",
        "salesforce": "Salesforce",
        "servicenow": "ServiceNow",
        "signzy": "Signzy",
        "writerai": "Writer AI",
    }

    return vendor_mapping.get(
        vendor_key.lower(),
        vendor_key.replace("_", " ").title()
    )


# ---------------------------------------------------------
# SOURCE URL CLEANING
# ---------------------------------------------------------

def clean_url(value):
    """
    Clean URL values while preserving the original URL.
    """

    value = clean_text(value)

    if not value:
        return ""

    # Remove accidental surrounding brackets
    value = value.strip("[]")

    return value.strip()


# ---------------------------------------------------------
# CONFIDENCE NORMALIZATION
# ---------------------------------------------------------

def normalize_confidence(value):
    """
    Normalize evidence confidence labels.
    """

    value = clean_text(value)

    if not value:
        return ""

    normalized = value.lower()

    confidence_mapping = {
        "high": "High",
        "high confidence": "High",
        "medium": "Medium",
        "medium confidence": "Medium",
        "moderate": "Medium",
        "low": "Low",
        "low confidence": "Low",
    }

    return confidence_mapping.get(normalized, value)


# ---------------------------------------------------------
# SOURCE TYPE NORMALIZATION
# ---------------------------------------------------------

def normalize_source_type(value):
    """
    Standardize common source-type labels.
    """

    value = clean_text(value)

    if not value:
        return ""

    normalized = value.lower()

    source_mapping = {
        "official documentation": "Official Documentation",
        "official product documentation": "Official Documentation",
        "technical documentation": "Technical Documentation",
        "vendor documentation": "Official Documentation",
        "official website": "Official Website",
        "product website": "Official Website",
        "analyst report": "Analyst Report",
        "third party report": "Third-Party Report",
        "third-party report": "Third-Party Report",
        "customer review": "Customer Review",
        "public review": "Public Review",
    }

    return source_mapping.get(normalized, value)


# ---------------------------------------------------------
# CATEGORY NORMALIZATION
# ---------------------------------------------------------

def normalize_category(value):
    """
    Standardize evaluation category formatting.
    """

    value = clean_text(value)

    if not value:
        return ""

    # Normalize common dash characters
    value = value.replace("–", "-").replace("—", "-")

    # Remove accidental repeated spaces
    value = re.sub(r"\s+", " ", value)

    return value.strip()


# ---------------------------------------------------------
# CRITERION NORMALIZATION
# ---------------------------------------------------------

def normalize_criterion(value):
    """
    Standardize evaluation criterion formatting.
    """

    value = clean_text(value)

    if not value:
        return ""

    # Normalize common dash characters
    value = value.replace("–", "-").replace("—", "-")

    # Remove accidental repeated spaces
    value = re.sub(r"\s+", " ", value)

    return value.strip()


# ---------------------------------------------------------
# LOAD ONE RAW FILE
# ---------------------------------------------------------

def load_raw_file(file_path):
    """
    Read and clean one raw vendor CSV.
    """

    print(f"Reading: {file_path.name}")

    try:
        df = pd.read_csv(
            file_path,
            encoding="utf-8-sig"
        )
    except UnicodeDecodeError:
        df = pd.read_csv(
            file_path,
            encoding="latin-1"
        )

    if df.empty:
        print(f"  WARNING: {file_path.name} is empty.")
        return pd.DataFrame(columns=STANDARD_COLUMNS)

    # Standardize column names
    df.columns = [
        standardize_column_name(column)
        for column in df.columns
    ]

    # Add Vendor column if it does not exist
    if "Vendor" not in df.columns:
        df["Vendor"] = extract_vendor_name(file_path)
    else:
        df["Vendor"] = df["Vendor"].apply(clean_text)

        # Fill missing vendor values using filename
        vendor_name = extract_vendor_name(file_path)

        df["Vendor"] = df["Vendor"].replace(
            "",
            vendor_name
        )

    # Make sure all expected columns exist
    for column in STANDARD_COLUMNS:
        if column not in df.columns:
            df[column] = ""

    # Keep only the standard columns
    df = df[STANDARD_COLUMNS].copy()

    # -----------------------------------------------------
    # FIELD-SPECIFIC CLEANING
    # -----------------------------------------------------

    df["Vendor"] = df["Vendor"].apply(clean_text)

    df["Evaluation Category"] = (
        df["Evaluation Category"]
        .apply(normalize_category)
    )

    df["Evaluation Criterion"] = (
        df["Evaluation Criterion"]
        .apply(normalize_criterion)
    )

    df["Evidence Summary"] = (
        df["Evidence Summary"]
        .apply(clean_text)
    )

    df["Source Type"] = (
        df["Source Type"]
        .apply(normalize_source_type)
    )

    df["Source URL"] = (
        df["Source URL"]
        .apply(clean_url)
    )

    df["Evidence Confidence"] = (
        df["Evidence Confidence"]
        .apply(normalize_confidence)
    )

    df["Evaluation Notes"] = (
        df["Evaluation Notes"]
        .apply(clean_text)
    )

    return df


# ---------------------------------------------------------
# VALIDATE REQUIRED STRUCTURE
# ---------------------------------------------------------

def validate_structure(df):
    """
    Check that the cleaned dataset contains
    the required standard columns.
    """

    missing_columns = [
        column
        for column in STANDARD_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )


# ---------------------------------------------------------
# MAIN CLEANING PIPELINE
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("STEP 19 - CLEAN AND NORMALIZE RAW DATA")
    print("=" * 60)

    # Create cleaned directory if necessary
    CLEANED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Find raw CSV files
    raw_files = sorted(
        RAW_DIR.glob("*.csv")
    )

    if not raw_files:
        raise FileNotFoundError(
            f"No CSV files found in: {RAW_DIR}"
        )

    print(f"\nRaw files found: {len(raw_files)}")

    all_dataframes = []

    # Process every raw vendor file
    for file_path in raw_files:

        df = load_raw_file(file_path)

        if not df.empty:
            all_dataframes.append(df)

        print(f"  Rows loaded: {len(df)}")
        print()

    if not all_dataframes:
        raise ValueError(
            "No usable data was found in the raw CSV files."
        )

    # Combine all vendors
    combined_df = pd.concat(
        all_dataframes,
        ignore_index=True
    )

    print("-" * 60)
    print("COMBINED DATA")
    print("-" * 60)

    print(f"Rows before duplicate removal: {len(combined_df)}")

    # -----------------------------------------------------
    # REMOVE EXACT DUPLICATES
    # -----------------------------------------------------

    before_duplicates = len(combined_df)

    combined_df = combined_df.drop_duplicates()

    duplicates_removed = (
        before_duplicates - len(combined_df)
    )

    print(
        f"Duplicate rows removed: {duplicates_removed}"
    )

    # -----------------------------------------------------
    # SORT DATA
    # -----------------------------------------------------

    combined_df = combined_df.sort_values(
        by=[
            "Vendor",
            "Evaluation Category",
            "Evaluation Criterion",
        ],
        kind="stable"
    ).reset_index(drop=True)

    # -----------------------------------------------------
    # VALIDATE STRUCTURE
    # -----------------------------------------------------

    validate_structure(combined_df)

    # -----------------------------------------------------
    # SAVE CLEANED DATASET
    # -----------------------------------------------------

    combined_df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    print("-" * 60)
    print("CLEANING COMPLETE")
    print("-" * 60)

    print(f"Final rows: {len(combined_df)}")
    print(f"Final columns: {len(combined_df.columns)}")
    print(f"Output file: {OUTPUT_FILE}")

    print("\nColumns:")
    for column in combined_df.columns:
        print(f"  - {column}")

    print("\nVendor counts:")
    print(
        combined_df["Vendor"]
        .value_counts()
        .to_string()
    )

    print("\nMissing values:")
    print(
        combined_df.isna()
        .sum()
        .to_string()
    )

    print("\nStep 19 completed successfully.")


# ---------------------------------------------------------
# SCRIPT ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":
    main()