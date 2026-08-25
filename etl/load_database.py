"""
STEP 23.3 - LOAD FINAL DATASET INTO MYSQL

Loads the final structured vendor evaluation dataset into:

    vendors
    categories
    criteria
    evaluations

Source:
    data/processed/final_vendor_evaluation_dataset.csv
"""

from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "final_vendor_evaluation_dataset.csv"
)

ENV_FILE = PROJECT_ROOT / ".env"


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

load_dotenv(ENV_FILE)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv(
    "DB_NAME",
    "vendor_decision_support"
)
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")


# ============================================================
# REQUIRED COLUMNS
# ============================================================

REQUIRED_COLUMNS = [
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


# ============================================================
# DATABASE CONNECTION
# ============================================================

def create_database_engine():
    """
    Create SQLAlchemy engine for MySQL.

    SQLAlchemy URL.create() is used so special characters
    in the database password are handled safely.
    """

    if not DB_PASSWORD:
        raise ValueError(
            "DB_PASSWORD is missing from .env"
        )

    connection_url = URL.create(
        drivername="mysql+pymysql",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=int(DB_PORT),
        database=DB_NAME,
    )

    return create_engine(
        connection_url,
        pool_pre_ping=True
    )


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():
    """
    Load the final structured CSV dataset.
    """

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    print(
        f"Loaded final dataset: "
        f"{df.shape[0]} rows × {df.shape[1]} columns"
    )

    return df


# ============================================================
# VALIDATE DATASET
# ============================================================

def validate_dataset(df):
    """
    Validate dataset structure before loading.
    """

    print("\n------------------------------------------------------------")
    print("DATASET VALIDATION")
    print("------------------------------------------------------------")

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

    print("[PASS] Required columns present")

    if len(df) != 136:
        raise ValueError(
            f"Expected 136 rows, found {len(df)}"
        )

    print("[PASS] Row count: 136")

    if df["vendor_id"].nunique() != 8:
        raise ValueError(
            "Expected 8 unique vendors"
        )

    print("[PASS] Vendor count: 8")

    if df["criterion_id"].nunique() != 17:
        raise ValueError(
            "Expected 17 unique criteria"
        )

    print("[PASS] Criterion count: 17")

    if df["category_id"].nunique() != 5:
        raise ValueError(
            "Expected 5 unique categories"
        )

    print("[PASS] Category count: 5")

    duplicate_count = df.duplicated(
        subset=["vendor_id", "criterion_id"]
    ).sum()

    if duplicate_count != 0:
        raise ValueError(
            f"Found {duplicate_count} duplicate "
            "vendor-criterion records"
        )

    print("[PASS] Vendor-criterion uniqueness")

    valid_statuses = {
        "Evaluated",
        "Not Evaluated",
    }

    invalid_statuses = set(
        df["evaluation_status"].dropna().unique()
    ) - valid_statuses

    if invalid_statuses:
        raise ValueError(
            f"Invalid evaluation statuses: "
            f"{sorted(invalid_statuses)}"
        )

    print("[PASS] Evaluation statuses")

    evaluated = df[
        df["evaluation_status"] == "Evaluated"
    ]

    invalid_scores = evaluated[
        (evaluated["assigned_score"] < 1)
        | (evaluated["assigned_score"] > 5)
    ]

    if not invalid_scores.empty:
        raise ValueError(
            "Found evaluated records with "
            "invalid scores"
        )

    print("[PASS] Score values")

    print("\nDataset validation passed.")

# ============================================================
# CLEAR EXISTING DATA
# ============================================================

def clear_existing_data(connection):
    """
    Clear existing project data before reloading.

    This makes the ETL load repeatable and prevents
    duplicate primary-key errors when the script is
    executed more than once.
    """

    print("\n------------------------------------------------------------")
    print("CLEARING EXISTING DATA")
    print("------------------------------------------------------------")

    connection.execute(
        text("DELETE FROM evaluations")
    )

    connection.execute(
        text("DELETE FROM criteria")
    )

    connection.execute(
        text("DELETE FROM categories")
    )

    connection.execute(
        text("DELETE FROM vendors")
    )

    print("[PASS] Existing evaluation data cleared")
    print("[PASS] Existing criteria cleared")
    print("[PASS] Existing categories cleared")
    print("[PASS] Existing vendors cleared")

# ============================================================
# LOAD VENDORS
# ============================================================

def load_vendors(connection, df):
    """
    Load unique vendors.
    """

    vendors = (
        df[
            [
                "vendor_id",
                "vendor",
            ]
        ]
        .drop_duplicates()
        .rename(
            columns={
                "vendor": "vendor_name"
            }
        )
    )

    vendors.to_sql(
        "vendors",
        con=connection,
        if_exists="append",
        index=False,
        method="multi"
    )

    print(
        f"[PASS] Loaded vendors: "
        f"{len(vendors)}"
    )


# ============================================================
# LOAD CATEGORIES
# ============================================================

def load_categories(connection, df):
    """
    Load unique evaluation categories.
    """

    categories = (
        df[
            [
                "category_id",
                "evaluation_category",
            ]
        ]
        .drop_duplicates()
        .rename(
            columns={
                "evaluation_category":
                    "category_name"
            }
        )
    )

    categories.to_sql(
        "categories",
        con=connection,
        if_exists="append",
        index=False,
        method="multi"
    )

    print(
        f"[PASS] Loaded categories: "
        f"{len(categories)}"
    )


# ============================================================
# LOAD CRITERIA
# ============================================================

def load_criteria(connection, df):
    """
    Load unique evaluation criteria.
    """

    criteria = (
        df[
            [
                "criterion_id",
                "category_id",
                "evaluation_criterion",
            ]
        ]
        .drop_duplicates()
        .rename(
            columns={
                "evaluation_criterion":
                    "criterion_name"
            }
        )
    )

    criteria.to_sql(
        "criteria",
        con=connection,
        if_exists="append",
        index=False,
        method="multi"
    )

    print(
        f"[PASS] Loaded criteria: "
        f"{len(criteria)}"
    )


# ============================================================
# LOAD EVALUATIONS
# ============================================================

def load_evaluations(connection, df):
    """
    Load all vendor evaluation records.
    """

    evaluations = df[
        [
            "evaluation_id",
            "vendor_id",
            "criterion_id",
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
    ].copy()

    evaluations.to_sql(
        "evaluations",
        con=connection,
        if_exists="append",
        index=False,
        method="multi"
    )

    print(
        f"[PASS] Loaded evaluations: "
        f"{len(evaluations)}"
    )


# ============================================================
# VERIFY DATABASE
# ============================================================

def verify_database(connection):
    """
    Verify loaded record counts.
    """

    print("\n------------------------------------------------------------")
    print("DATABASE VALIDATION")
    print("------------------------------------------------------------")

    expected_counts = {
        "vendors": 8,
        "categories": 5,
        "criteria": 17,
        "evaluations": 136,
    }

    for table_name, expected_count in (
        expected_counts.items()
    ):

        query = text(
            f"SELECT COUNT(*) "
            f"FROM {table_name}"
        )

        actual_count = connection.execute(
            query
        ).scalar()

        if actual_count != expected_count:
            raise ValueError(
                f"{table_name}: expected "
                f"{expected_count}, found "
                f"{actual_count}"
            )

        print(
            f"[PASS] {table_name}: "
            f"{actual_count} rows"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("STEP 23.3 - LOAD FINAL DATASET INTO MYSQL")
    print("=" * 60)

    print(f"\nDatabase: {DB_NAME}")
    print(f"Source: {DATA_FILE}")

    df = load_dataset()

    validate_dataset(df)

    engine = create_database_engine()

    try:

        with engine.begin() as connection:

            print(
                "\n------------------------------------------------------------"
            )
            print("LOADING DATABASE")
            print(
                "------------------------------------------------------------"
            )
            
            clear_existing_data(
                connection
            )

            load_vendors(
                connection,
                df
            )

            load_categories(
                connection,
                df
            )

            load_criteria(
                connection,
                df
            )

            load_evaluations(
                connection,
                df
            )

            verify_database(
                connection
            )

    except SQLAlchemyError as error:

        print(
            "\n[FAIL] Database operation failed."
        )

        raise error

    print(
        "\n------------------------------------------------------------"
    )

    print("FINAL STATUS: PASS")

    print(
        "Final dataset successfully loaded into MySQL."
    )

    print(
        "Step 23.3 completed successfully."
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()