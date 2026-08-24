"""
Step 21B Layer 1 - Validate Scoring Rubric

Validates the machine-readable scoring rubric configuration
before it is used for vendor score assignment.
"""

from pathlib import Path
import json


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RUBRIC_FILE = (
    PROJECT_ROOT
    / "config"
    / "scoring_rubric.json"
)


# ---------------------------------------------------------
# EXPECTED VALUES
# ---------------------------------------------------------

EXPECTED_SCORES = {
    "1",
    "2",
    "3",
    "4",
    "5",
}

EXPECTED_RATINGS = {
    "Poor",
    "Limited",
    "Adequate",
    "Strong",
    "Excellent",
}

EXPECTED_STATUSES = {
    "Evaluated",
    "Not Evaluated",
}

EXPECTED_CONFIDENCE_VALUES = {
    "High",
    "Medium",
    "Low",
    "High / Medium",
    "Medium / Low",
}


# ---------------------------------------------------------
# MAIN VALIDATION
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("STEP 21B - LAYER 1 - VALIDATE SCORING RUBRIC")
    print("=" * 60)

    # -----------------------------------------------------
    # CHECK FILE
    # -----------------------------------------------------

    if not RUBRIC_FILE.exists():

        raise FileNotFoundError(
            f"Scoring rubric not found: {RUBRIC_FILE}"
        )

    # -----------------------------------------------------
    # LOAD JSON
    # -----------------------------------------------------

    with open(
        RUBRIC_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        rubric = json.load(file)

    print(
        f"\nLoaded rubric: {RUBRIC_FILE}"
    )

    # -----------------------------------------------------
    # CHECK FRAMEWORK INFORMATION
    # -----------------------------------------------------

    assert rubric["framework_name"]
    assert rubric["framework_version"]

    print(
        "[PASS] Framework name and version"
    )

    # -----------------------------------------------------
    # CHECK SCORING SCALE
    # -----------------------------------------------------

    scale = rubric["scoring_scale"]

    assert scale["type"] == "five_point"
    assert scale["minimum_score"] == 1
    assert scale["maximum_score"] == 5
    assert scale["not_evaluated_value"] is None

    print(
        "[PASS] Five-point scoring scale"
    )

    # -----------------------------------------------------
    # CHECK RATING DEFINITIONS
    # -----------------------------------------------------

    ratings = rubric["ratings"]

    actual_scores = set(
        ratings.keys()
    )

    assert actual_scores == EXPECTED_SCORES

    actual_ratings = {
        definition["rating"]
        for definition in ratings.values()
    }

    assert actual_ratings == EXPECTED_RATINGS

    print(
        "[PASS] All five score/rating definitions"
    )

    # -----------------------------------------------------
    # CHECK RATING DESCRIPTIONS
    # -----------------------------------------------------

    for score, definition in ratings.items():

        assert definition["rating"]
        assert definition["description"]

    print(
        "[PASS] Rating descriptions"
    )

    # -----------------------------------------------------
    # CHECK NOT EVALUATED RULE
    # -----------------------------------------------------

    not_evaluated = rubric["not_evaluated"]

    assert (
        not_evaluated["status"]
        == "Not Evaluated"
    )

    assert (
        not_evaluated["rating"]
        == "N/A"
    )

    assert (
        not_evaluated["score"]
        is None
    )

    print(
        "[PASS] Not Evaluated / N/A rule"
    )

    # -----------------------------------------------------
    # CHECK EVALUATION STATUSES
    # -----------------------------------------------------

    statuses = set(
        rubric["evaluation_statuses"].values()
    )

    assert statuses == EXPECTED_STATUSES

    print(
        "[PASS] Evaluation statuses"
    )

    # -----------------------------------------------------
    # CHECK CONFIDENCE LEVELS
    # -----------------------------------------------------

    confidence_values = set(
        rubric["evidence_confidence"].keys()
    )

    assert (
        confidence_values
        == EXPECTED_CONFIDENCE_VALUES
    )

    print(
        "[PASS] Evidence confidence definitions"
    )

    # -----------------------------------------------------
    # CHECK SCORING PRINCIPLES
    # -----------------------------------------------------

    principles = rubric[
        "scoring_principles"
    ]

    assert len(principles) >= 5

    print(
        "[PASS] Scoring principles"
    )

    # -----------------------------------------------------
    # FINAL RESULT
    # -----------------------------------------------------

    print("\n" + "-" * 60)
    print(
        "FINAL STATUS: PASS"
    )
    print(
        "Scoring rubric is valid and ready "
        "for score assignment."
    )
    print(
        "-" * 60
    )

    print(
        "\nStep 21B Layer 1 completed successfully."
    )


# ---------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":
    main()