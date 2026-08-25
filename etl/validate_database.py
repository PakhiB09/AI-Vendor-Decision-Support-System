"""
STEP 24 - VALIDATE MYSQL DATABASE

Validates the vendor decision-support database after
the Step 23 database loading process.

Checks:

    - Table record counts
    - Vendor coverage
    - Criterion coverage
    - Vendor-criterion uniqueness
    - Evaluation status integrity
    - Score integrity
    - Foreign-key relationships
    - Category coverage
    - Full relational join
"""

from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv(
    "DB_NAME",
    "vendor_decision_support"
)
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")


# ============================================================
# EXPECTED DATABASE STRUCTURE
# ============================================================

EXPECTED_COUNTS = {
    "vendors": 8,
    "categories": 5,
    "criteria": 17,
    "evaluations": 136,
}


# ============================================================
# DATABASE CONNECTION
# ============================================================

def create_database_engine():
    """
    Create a safe SQLAlchemy connection URL.

    URL.create() safely handles special characters
    contained in the database password.
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
# CHECK TABLE COUNTS
# ============================================================

def validate_table_counts(connection):

    print("\n------------------------------------------------------------")
    print("TABLE COUNT VALIDATION")
    print("------------------------------------------------------------")

    for table_name, expected_count in EXPECTED_COUNTS.items():

        query = text(
            f"SELECT COUNT(*) FROM {table_name}"
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
# CHECK VENDOR COVERAGE
# ============================================================

def validate_vendor_coverage(connection):

    print("\n------------------------------------------------------------")
    print("VENDOR COVERAGE VALIDATION")
    print("------------------------------------------------------------")

    query = text("""
        SELECT
            v.vendor_id,
            v.vendor_name,
            COUNT(e.evaluation_id) AS evaluation_count
        FROM vendors v
        LEFT JOIN evaluations e
            ON v.vendor_id = e.vendor_id
        GROUP BY
            v.vendor_id,
            v.vendor_name
        ORDER BY
            v.vendor_id
    """)

    df = pd.read_sql(
        query,
        connection
    )

    invalid = df[
        df["evaluation_count"] != 17
    ]

    if not invalid.empty:
        raise ValueError(
            "Vendor coverage validation failed:\n"
            + invalid.to_string(index=False)
        )

    print(
        "[PASS] All 8 vendors contain "
        "17 evaluation records"
    )


# ============================================================
# CHECK DUPLICATES
# ============================================================

def validate_duplicates(connection):

    print("\n------------------------------------------------------------")
    print("DUPLICATE VALIDATION")
    print("------------------------------------------------------------")

    query = text("""
        SELECT
            vendor_id,
            criterion_id,
            COUNT(*) AS duplicate_count
        FROM evaluations
        GROUP BY
            vendor_id,
            criterion_id
        HAVING COUNT(*) > 1
    """)

    df = pd.read_sql(
        query,
        connection
    )

    if not df.empty:
        raise ValueError(
            "Duplicate vendor-criterion combinations found:\n"
            + df.to_string(index=False)
        )

    print(
        "[PASS] No duplicate vendor-criterion combinations"
    )


# ============================================================
# CHECK EVALUATION STATUSES
# ============================================================

def validate_statuses(connection):

    print("\n------------------------------------------------------------")
    print("EVALUATION STATUS VALIDATION")
    print("------------------------------------------------------------")

    query = text("""
        SELECT
            evaluation_status,
            COUNT(*) AS record_count
        FROM evaluations
        GROUP BY evaluation_status
    """)

    df = pd.read_sql(
        query,
        connection
    )

    status_counts = dict(
        zip(
            df["evaluation_status"],
            df["record_count"]
        )
    )

    evaluated = status_counts.get(
        "Evaluated",
        0
    )

    not_evaluated = status_counts.get(
        "Not Evaluated",
        0
    )

    if evaluated != 130:
        raise ValueError(
            f"Expected 130 Evaluated records, "
            f"found {evaluated}"
        )

    if not_evaluated != 6:
        raise ValueError(
            f"Expected 6 Not Evaluated records, "
            f"found {not_evaluated}"
        )

    print(
        "[PASS] Evaluated records: 130"
    )

    print(
        "[PASS] Not Evaluated records: 6"
    )


# ============================================================
# CHECK SCORE INTEGRITY
# ============================================================

def validate_scores(connection):

    print("\n------------------------------------------------------------")
    print("SCORE VALIDATION")
    print("------------------------------------------------------------")

    invalid_evaluated = text("""
        SELECT
            evaluation_id,
            assigned_score
        FROM evaluations
        WHERE evaluation_status = 'Evaluated'
          AND (
                assigned_score IS NULL
                OR assigned_score < 1
                OR assigned_score > 5
              )
    """)

    df_invalid = pd.read_sql(
        invalid_evaluated,
        connection
    )

    if not df_invalid.empty:
        raise ValueError(
            "Invalid evaluated scores found:\n"
            + df_invalid.to_string(index=False)
        )

    print(
        "[PASS] Evaluated scores are within 1-5"
    )

    invalid_na = text("""
        SELECT
            evaluation_id,
            assigned_score
        FROM evaluations
        WHERE evaluation_status = 'Not Evaluated'
          AND assigned_score IS NOT NULL
    """)

    df_na = pd.read_sql(
        invalid_na,
        connection
    )

    if not df_na.empty:
        raise ValueError(
            "Not Evaluated records contain scores:\n"
            + df_na.to_string(index=False)
        )

    print(
        "[PASS] Not Evaluated records contain no scores"
    )


# ============================================================
# CHECK FOREIGN-KEY RELATIONSHIPS
# ============================================================

def validate_relationships(connection):

    print("\n------------------------------------------------------------")
    print("RELATIONSHIP VALIDATION")
    print("------------------------------------------------------------")

    invalid_vendors = text("""
        SELECT COUNT(*)
        FROM evaluations e
        LEFT JOIN vendors v
            ON e.vendor_id = v.vendor_id
        WHERE v.vendor_id IS NULL
    """)

    invalid_vendor_count = connection.execute(
        invalid_vendors
    ).scalar()

    if invalid_vendor_count != 0:
        raise ValueError(
            "Found evaluations with invalid vendor references"
        )

    print(
        "[PASS] All evaluation vendor references are valid"
    )

    invalid_criteria = text("""
        SELECT COUNT(*)
        FROM evaluations e
        LEFT JOIN criteria c
            ON e.criterion_id = c.criterion_id
        WHERE c.criterion_id IS NULL
    """)

    invalid_criterion_count = connection.execute(
        invalid_criteria
    ).scalar()

    if invalid_criterion_count != 0:
        raise ValueError(
            "Found evaluations with invalid criterion references"
        )

    print(
        "[PASS] All evaluation criterion references are valid"
    )

    invalid_categories = text("""
        SELECT COUNT(*)
        FROM criteria c
        LEFT JOIN categories cat
            ON c.category_id = cat.category_id
        WHERE cat.category_id IS NULL
    """)

    invalid_category_count = connection.execute(
        invalid_categories
    ).scalar()

    if invalid_category_count != 0:
        raise ValueError(
            "Found criteria with invalid category references"
        )

    print(
        "[PASS] All criterion category references are valid"
    )


# ============================================================
# CHECK FULL JOIN
# ============================================================

def validate_full_join(connection):

    print("\n------------------------------------------------------------")
    print("RELATIONAL JOIN VALIDATION")
    print("------------------------------------------------------------")

    query = text("""
        SELECT COUNT(*)
        FROM evaluations e
        INNER JOIN vendors v
            ON e.vendor_id = v.vendor_id
        INNER JOIN criteria c
            ON e.criterion_id = c.criterion_id
        INNER JOIN categories cat
            ON c.category_id = cat.category_id
    """)

    joined_count = connection.execute(
        query
    ).scalar()

    if joined_count != 136:
        raise ValueError(
            f"Expected 136 records after full join, "
            f"found {joined_count}"
        )

    print(
        "[PASS] All 136 evaluation records "
        "successfully join across all tables"
    )


# ============================================================
# VENDOR SCORE SUMMARY
# ============================================================

def print_vendor_summary(connection):

    print("\n------------------------------------------------------------")
    print("VENDOR SCORE SUMMARY")
    print("------------------------------------------------------------")

    query = text("""
        SELECT
            v.vendor_name,

            COUNT(
                CASE
                    WHEN e.evaluation_status = 'Evaluated'
                    THEN 1
                END
            ) AS evaluated_criteria,

            COUNT(
                CASE
                    WHEN e.evaluation_status = 'Not Evaluated'
                    THEN 1
                END
            ) AS not_evaluated_criteria,

            ROUND(
                AVG(
                    CASE
                        WHEN e.evaluation_status = 'Evaluated'
                        THEN e.assigned_score
                    END
                ),
                2
            ) AS average_score

        FROM vendors v
        INNER JOIN evaluations e
            ON v.vendor_id = e.vendor_id

        GROUP BY
            v.vendor_id,
            v.vendor_name

        ORDER BY
            average_score DESC
    """)

    df = pd.read_sql(
        query,
        connection
    )

    print(
        df.to_string(index=False)
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("STEP 24 - VALIDATE MYSQL DATABASE")
    print("=" * 60)

    print(
        f"\nDatabase: {DB_NAME}"
    )

    engine = create_database_engine()

    try:

        with engine.connect() as connection:

            validate_table_counts(
                connection
            )

            validate_vendor_coverage(
                connection
            )

            validate_duplicates(
                connection
            )

            validate_statuses(
                connection
            )

            validate_scores(
                connection
            )

            validate_relationships(
                connection
            )

            validate_full_join(
                connection
            )

            print_vendor_summary(
                connection
            )

    finally:

        engine.dispose()

    print(
        "\n------------------------------------------------------------"
    )

    print(
        "FINAL STATUS: PASS"
    )

    print(
        "MySQL database validation completed successfully."
    )

    print(
        "Step 24 completed successfully."
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()