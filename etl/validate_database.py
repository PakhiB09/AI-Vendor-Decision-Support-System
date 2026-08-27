"""
STEP 24 - VALIDATE MYSQL DATABASE

Validates the complete relational database for the
Vendor Evaluation & Decision-Support System.

Tables validated:

    vendors
    categories
    criteria
    evaluations
    personas
    persona_weights
"""

from pathlib import Path
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ENV_FILE = PROJECT_ROOT / ".env"

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
# DATABASE CONNECTION
# ============================================================

def create_database_engine():
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
# HELPER
# ============================================================

def get_count(connection, table_name):
    """
    Return the number of records in a table.
    """

    query = text(
        f"SELECT COUNT(*) FROM {table_name}"
    )

    return connection.execute(query).scalar()


# ============================================================
# TABLE COUNT VALIDATION
# ============================================================

def validate_table_counts(connection):

    print("\n" + "-" * 60)
    print("TABLE COUNT VALIDATION")
    print("-" * 60)

    expected_counts = {
        "vendors": 8,
        "categories": 5,
        "criteria": 17,
        "evaluations": 136,
        "personas": 5,
        "persona_weights": 25,
    }

    for table_name, expected_count in expected_counts.items():

        actual_count = get_count(
            connection,
            table_name
        )

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
# VENDOR COVERAGE
# ============================================================

def validate_vendor_coverage(connection):

    print("\n" + "-" * 60)
    print("VENDOR COVERAGE VALIDATION")
    print("-" * 60)

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

    rows = connection.execute(query).fetchall()

    if len(rows) != 8:

        raise ValueError(
            f"Expected 8 vendors, found {len(rows)}"
        )

    invalid = [
        row
        for row in rows
        if row.evaluation_count != 17
    ]

    if invalid:

        raise ValueError(
            "One or more vendors do not contain "
            "exactly 17 evaluation records."
        )

    print(
        "[PASS] All 8 vendors contain "
        "17 evaluation records"
    )


# ============================================================
# CRITERIA COVERAGE
# ============================================================

def validate_criteria_coverage(connection):

    print("\n" + "-" * 60)
    print("CRITERIA COVERAGE VALIDATION")
    print("-" * 60)

    query = text("""
        SELECT
            c.criterion_id,
            c.criterion_name,
            COUNT(e.evaluation_id) AS evaluation_count
        FROM criteria c
        LEFT JOIN evaluations e
            ON c.criterion_id = e.criterion_id
        GROUP BY
            c.criterion_id,
            c.criterion_name
        ORDER BY
            c.criterion_id
    """)

    rows = connection.execute(query).fetchall()

    if len(rows) != 17:

        raise ValueError(
            f"Expected 17 criteria, found {len(rows)}"
        )

    invalid = [
        row
        for row in rows
        if row.evaluation_count != 8
    ]

    if invalid:

        raise ValueError(
            "One or more criteria do not contain "
            "exactly 8 evaluation records."
        )

    print(
        "[PASS] All 17 criteria contain "
        "8 evaluation records"
    )


# ============================================================
# DUPLICATE VALIDATION
# ============================================================

def validate_duplicates(connection):

    print("\n" + "-" * 60)
    print("DUPLICATE VALIDATION")
    print("-" * 60)

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

    duplicates = connection.execute(query).fetchall()

    if duplicates:

        raise ValueError(
            f"Found {len(duplicates)} duplicate "
            "vendor-criterion combinations."
        )

    print(
        "[PASS] No duplicate vendor-criterion combinations"
    )


# ============================================================
# EVALUATION STATUS VALIDATION
# ============================================================

def validate_evaluation_status(connection):

    print("\n" + "-" * 60)
    print("EVALUATION STATUS VALIDATION")
    print("-" * 60)

    query = text("""
        SELECT
            evaluation_status,
            COUNT(*) AS record_count
        FROM evaluations
        GROUP BY evaluation_status
    """)

    rows = connection.execute(query).fetchall()

    status_counts = {
        row.evaluation_status: row.record_count
        for row in rows
    }

    expected = {
        "Evaluated": 130,
        "Not Evaluated": 6,
    }

    for status, expected_count in expected.items():

        actual_count = status_counts.get(
            status,
            0
        )

        if actual_count != expected_count:

            raise ValueError(
                f"{status}: expected "
                f"{expected_count}, found "
                f"{actual_count}"
            )

        print(
            f"[PASS] {status} records: "
            f"{actual_count}"
        )


# ============================================================
# SCORE VALIDATION
# ============================================================

def validate_scores(connection):

    print("\n" + "-" * 60)
    print("SCORE VALIDATION")
    print("-" * 60)

    invalid_evaluated = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM evaluations
            WHERE evaluation_status = 'Evaluated'
              AND (
                    assigned_score IS NULL
                    OR assigned_score < 1
                    OR assigned_score > 5
                  )
        """)
    ).scalar()

    if invalid_evaluated != 0:

        raise ValueError(
            "Found evaluated records with "
            "invalid scores."
        )

    print(
        "[PASS] Evaluated scores are within 1-5"
    )

    invalid_not_evaluated = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM evaluations
            WHERE evaluation_status = 'Not Evaluated'
              AND assigned_score IS NOT NULL
        """)
    ).scalar()

    if invalid_not_evaluated != 0:

        raise ValueError(
            "Found Not Evaluated records "
            "containing scores."
        )

    print(
        "[PASS] Not Evaluated records contain no scores"
    )


# ============================================================
# RELATIONSHIP VALIDATION
# ============================================================

def validate_relationships(connection):

    print("\n" + "-" * 60)
    print("RELATIONSHIP VALIDATION")
    print("-" * 60)

    # --------------------------------------------------------
    # Evaluation -> Vendor
    # --------------------------------------------------------

    invalid_vendor_refs = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM evaluations e
            LEFT JOIN vendors v
                ON e.vendor_id = v.vendor_id
            WHERE v.vendor_id IS NULL
        """)
    ).scalar()

    if invalid_vendor_refs != 0:

        raise ValueError(
            "Found evaluations with invalid "
            "vendor references."
        )

    print(
        "[PASS] All evaluation vendor references are valid"
    )

    # --------------------------------------------------------
    # Evaluation -> Criterion
    # --------------------------------------------------------

    invalid_criterion_refs = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM evaluations e
            LEFT JOIN criteria c
                ON e.criterion_id = c.criterion_id
            WHERE c.criterion_id IS NULL
        """)
    ).scalar()

    if invalid_criterion_refs != 0:

        raise ValueError(
            "Found evaluations with invalid "
            "criterion references."
        )

    print(
        "[PASS] All evaluation criterion references are valid"
    )

    # --------------------------------------------------------
    # Criterion -> Category
    # --------------------------------------------------------

    invalid_category_refs = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM criteria c
            LEFT JOIN categories cat
                ON c.category_id = cat.category_id
            WHERE cat.category_id IS NULL
        """)
    ).scalar()

    if invalid_category_refs != 0:

        raise ValueError(
            "Found criteria with invalid "
            "category references."
        )

    print(
        "[PASS] All criterion category references are valid"
    )


# ============================================================
# PERSONA VALIDATION
# ============================================================

def validate_personas(connection):

    print("\n" + "-" * 60)
    print("PERSONA VALIDATION")
    print("-" * 60)

    # --------------------------------------------------------
    # Persona count
    # --------------------------------------------------------

    persona_count = get_count(
        connection,
        "personas"
    )

    if persona_count != 5:

        raise ValueError(
            f"Expected 5 personas, found "
            f"{persona_count}"
        )

    print("[PASS] 5 personas present")

    # --------------------------------------------------------
    # Required fields
    # --------------------------------------------------------

    missing_fields = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM personas
            WHERE persona_id IS NULL
               OR persona_name IS NULL
               OR TRIM(persona_name) = ''
        """)
    ).scalar()

    if missing_fields != 0:

        raise ValueError(
            "Found personas with missing "
            "required fields."
        )

    print(
        "[PASS] Persona required fields are complete"
    )

    # --------------------------------------------------------
    # Duplicate persona IDs
    # --------------------------------------------------------

    duplicate_ids = connection.execute(
        text("""
            SELECT
                persona_id,
                COUNT(*) AS duplicate_count
            FROM personas
            GROUP BY persona_id
            HAVING COUNT(*) > 1
        """)
    ).fetchall()

    if duplicate_ids:

        raise ValueError(
            "Duplicate persona IDs found."
        )

    print(
        "[PASS] Persona IDs are unique"
    )

    # --------------------------------------------------------
    # Duplicate persona names
    # --------------------------------------------------------

    duplicate_names = connection.execute(
        text("""
            SELECT
                persona_name,
                COUNT(*) AS duplicate_count
            FROM personas
            GROUP BY persona_name
            HAVING COUNT(*) > 1
        """)
    ).fetchall()

    if duplicate_names:

        raise ValueError(
            "Duplicate persona names found."
        )

    print(
        "[PASS] Persona names are unique"
    )


# ============================================================
# PERSONA WEIGHT VALIDATION
# ============================================================

def validate_persona_weights(connection):

    print("\n" + "-" * 60)
    print("PERSONA WEIGHT VALIDATION")
    print("-" * 60)

    # --------------------------------------------------------
    # Total weight records
    # --------------------------------------------------------

    weight_count = get_count(
        connection,
        "persona_weights"
    )

    if weight_count != 25:

        raise ValueError(
            f"Expected 25 persona weights, "
            f"found {weight_count}"
        )

    print(
        "[PASS] 25 persona weight records present"
    )

    # --------------------------------------------------------
    # Every persona must have exactly 5 weights
    # --------------------------------------------------------

    query = text("""
        SELECT
            p.persona_id,
            p.persona_name,
            COUNT(pw.category_id) AS category_count
        FROM personas p
        LEFT JOIN persona_weights pw
            ON p.persona_id = pw.persona_id
        GROUP BY
            p.persona_id,
            p.persona_name
        ORDER BY
            p.persona_id
    """)

    rows = connection.execute(query).fetchall()

    invalid_counts = [
        row
        for row in rows
        if row.category_count != 5
    ]

    if invalid_counts:

        raise ValueError(
            "One or more personas do not have "
            "exactly 5 category weights."
        )

    print(
        "[PASS] Every persona has 5 category weights"
    )

    # --------------------------------------------------------
    # No duplicate persona-category combinations
    # --------------------------------------------------------

    duplicate_weights = connection.execute(
        text("""
            SELECT
                persona_id,
                category_id,
                COUNT(*) AS duplicate_count
            FROM persona_weights
            GROUP BY
                persona_id,
                category_id
            HAVING COUNT(*) > 1
        """)
    ).fetchall()

    if duplicate_weights:

        raise ValueError(
            "Duplicate persona-category weight "
            "records found."
        )

    print(
        "[PASS] No duplicate persona-category weights"
    )

    # --------------------------------------------------------
    # Weight range
    # --------------------------------------------------------

    invalid_range = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM persona_weights
            WHERE weight IS NULL
               OR weight < 0
               OR weight > 1
        """)
    ).scalar()

    if invalid_range != 0:

        raise ValueError(
            "Found persona weights outside "
            "the valid range 0-1."
        )

    print(
        "[PASS] All persona weights are within 0-1"
    )

    # --------------------------------------------------------
    # Weight total
    # --------------------------------------------------------

    query = text("""
        SELECT
            p.persona_id,
            p.persona_name,
            ROUND(SUM(pw.weight), 4) AS total_weight
        FROM personas p
        JOIN persona_weights pw
            ON p.persona_id = pw.persona_id
        GROUP BY
            p.persona_id,
            p.persona_name
        ORDER BY
            p.persona_id
    """)

    rows = connection.execute(query).fetchall()

    invalid_totals = [
        row
        for row in rows
        if abs(float(row.total_weight) - 1.0) > 0.0001
    ]

    if invalid_totals:

        raise ValueError(
            "One or more persona weight profiles "
            "do not total 100%."
        )

    print(
        "[PASS] All persona weight profiles total 100%"
    )


# ============================================================
# PERSONA RELATIONSHIP VALIDATION
# ============================================================

def validate_persona_relationships(connection):

    print("\n" + "-" * 60)
    print("PERSONA RELATIONSHIP VALIDATION")
    print("-" * 60)

    # --------------------------------------------------------
    # Persona weight -> Persona
    # --------------------------------------------------------

    invalid_persona_refs = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM persona_weights pw
            LEFT JOIN personas p
                ON pw.persona_id = p.persona_id
            WHERE p.persona_id IS NULL
        """)
    ).scalar()

    if invalid_persona_refs != 0:

        raise ValueError(
            "Found persona weights with invalid "
            "persona references."
        )

    print(
        "[PASS] All persona references are valid"
    )

    # --------------------------------------------------------
    # Persona weight -> Category
    # --------------------------------------------------------

    invalid_category_refs = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM persona_weights pw
            LEFT JOIN categories c
                ON pw.category_id = c.category_id
            WHERE c.category_id IS NULL
        """)
    ).scalar()

    if invalid_category_refs != 0:

        raise ValueError(
            "Found persona weights with invalid "
            "category references."
        )

    print(
        "[PASS] All persona category references are valid"
    )


# ============================================================
# EVALUATION RELATIONAL JOIN VALIDATION
# ============================================================

def validate_evaluation_join(connection):

    print("\n" + "-" * 60)
    print("RELATIONAL JOIN VALIDATION")
    print("-" * 60)

    query = text("""
        SELECT COUNT(*)
        FROM evaluations e
        JOIN vendors v
            ON e.vendor_id = v.vendor_id
        JOIN criteria c
            ON e.criterion_id = c.criterion_id
        JOIN categories cat
            ON c.category_id = cat.category_id
    """)

    joined_count = connection.execute(query).scalar()

    if joined_count != 136:

        raise ValueError(
            f"Expected 136 joined evaluation records, "
            f"found {joined_count}"
        )

    print(
        "[PASS] All 136 evaluation records "
        "successfully join across evaluation tables"
    )


# ============================================================
# PERSONA RELATIONAL JOIN VALIDATION
# ============================================================

def validate_persona_join(connection):

    print("\n" + "-" * 60)
    print("PERSONA JOIN VALIDATION")
    print("-" * 60)

    query = text("""
        SELECT COUNT(*)
        FROM personas p
        JOIN persona_weights pw
            ON p.persona_id = pw.persona_id
        JOIN categories c
            ON pw.category_id = c.category_id
    """)

    joined_count = connection.execute(query).scalar()

    if joined_count != 25:

        raise ValueError(
            f"Expected 25 persona-weight-category "
            f"records, found {joined_count}"
        )

    print(
        "[PASS] All 25 persona weights successfully "
        "join to personas and categories"
    )


# ============================================================
# VENDOR SCORE SUMMARY
# ============================================================

def validate_vendor_score_summary(connection):

    print("\n" + "-" * 60)
    print("VENDOR SCORE SUMMARY")
    print("-" * 60)

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

        LEFT JOIN evaluations e
            ON v.vendor_id = e.vendor_id

        GROUP BY
            v.vendor_id,
            v.vendor_name

        ORDER BY
            average_score DESC
    """)

    rows = connection.execute(query).fetchall()

    print(
        f"{'vendor_name':<20}"
        f"{'evaluated':<12}"
        f"{'not_evaluated':<15}"
        f"average_score"
    )

    print("-" * 60)

    for row in rows:

        print(
            f"{row.vendor_name:<20}"
            f"{row.evaluated_criteria:<12}"
            f"{row.not_evaluated_criteria:<15}"
            f"{row.average_score}"
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

            # ------------------------------------------------
            # Core evaluation database
            # ------------------------------------------------

            validate_table_counts(
                connection
            )

            validate_vendor_coverage(
                connection
            )

            validate_criteria_coverage(
                connection
            )

            validate_duplicates(
                connection
            )

            validate_evaluation_status(
                connection
            )

            validate_scores(
                connection
            )

            validate_relationships(
                connection
            )

            # ------------------------------------------------
            # Persona weighting framework
            # ------------------------------------------------

            validate_personas(
                connection
            )

            validate_persona_weights(
                connection
            )

            validate_persona_relationships(
                connection
            )

            # ------------------------------------------------
            # Relational joins
            # ------------------------------------------------

            validate_evaluation_join(
                connection
            )

            validate_persona_join(
                connection
            )

            # ------------------------------------------------
            # Vendor summary
            # ------------------------------------------------

            validate_vendor_score_summary(
                connection
            )

    except SQLAlchemyError as error:

        print(
            "\n[FAIL] Database validation failed."
        )

        raise error

    print(
        "\n" + "-" * 60
    )

    print(
        "FINAL STATUS: PASS"
    )

    print(
        "Complete MySQL database validation "
        "completed successfully."
    )

    print(
        "Step 24 completed successfully."
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()