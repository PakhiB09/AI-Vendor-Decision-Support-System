-- ============================================================
-- STEP 24 - DATABASE VALIDATION QUERIES
-- ============================================================
-- Database: vendor_decision_support
--
-- Purpose:
-- Validate database structure, relationships, record counts,
-- scoring integrity, and vendor/criterion coverage.
-- ============================================================


USE vendor_decision_support;


-- ============================================================
-- 1. BASIC TABLE COUNTS
-- ============================================================

SELECT
    'vendors' AS table_name,
    COUNT(*) AS record_count
FROM vendors

UNION ALL

SELECT
    'categories',
    COUNT(*)
FROM categories

UNION ALL

SELECT
    'criteria',
    COUNT(*)
FROM criteria

UNION ALL

SELECT
    'evaluations',
    COUNT(*)
FROM evaluations;


-- ============================================================
-- 2. VENDOR COVERAGE
-- ============================================================

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
    v.vendor_id;


-- ============================================================
-- 3. CRITERION COVERAGE
-- ============================================================

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
    c.criterion_id;


-- ============================================================
-- 4. DUPLICATE VENDOR-CRITERION CHECK
-- ============================================================

SELECT
    vendor_id,
    criterion_id,
    COUNT(*) AS duplicate_count
FROM evaluations
GROUP BY
    vendor_id,
    criterion_id
HAVING COUNT(*) > 1;


-- ============================================================
-- 5. EVALUATION STATUS DISTRIBUTION
-- ============================================================

SELECT
    evaluation_status,
    COUNT(*) AS record_count
FROM evaluations
GROUP BY
    evaluation_status
ORDER BY
    evaluation_status;


-- ============================================================
-- 6. SCORE DISTRIBUTION
-- ============================================================

SELECT
    assigned_score,
    COUNT(*) AS record_count
FROM evaluations
WHERE evaluation_status = 'Evaluated'
GROUP BY
    assigned_score
ORDER BY
    assigned_score;


-- ============================================================
-- 7. INVALID SCORE CHECK
-- ============================================================

SELECT
    evaluation_id,
    vendor_id,
    criterion_id,
    evaluation_status,
    assigned_score
FROM evaluations
WHERE evaluation_status = 'Evaluated'
  AND (
        assigned_score IS NULL
        OR assigned_score < 1
        OR assigned_score > 5
      );


-- ============================================================
-- 8. INVALID N/A SCORE CHECK
-- ============================================================

SELECT
    evaluation_id,
    vendor_id,
    criterion_id,
    evaluation_status,
    assigned_score
FROM evaluations
WHERE evaluation_status = 'Not Evaluated'
  AND assigned_score IS NOT NULL;


-- ============================================================
-- 9. INVALID VENDOR REFERENCES
-- ============================================================

SELECT
    e.evaluation_id,
    e.vendor_id
FROM evaluations e
LEFT JOIN vendors v
    ON e.vendor_id = v.vendor_id
WHERE v.vendor_id IS NULL;


-- ============================================================
-- 10. INVALID CRITERION REFERENCES
-- ============================================================

SELECT
    e.evaluation_id,
    e.criterion_id
FROM evaluations e
LEFT JOIN criteria c
    ON e.criterion_id = c.criterion_id
WHERE c.criterion_id IS NULL;


-- ============================================================
-- 11. INVALID CATEGORY REFERENCES
-- ============================================================

SELECT
    c.criterion_id,
    c.category_id
FROM criteria c
LEFT JOIN categories cat
    ON c.category_id = cat.category_id
WHERE cat.category_id IS NULL;


-- ============================================================
-- 12. CATEGORY DISTRIBUTION
-- ============================================================

SELECT
    cat.category_id,
    cat.category_name,
    COUNT(DISTINCT c.criterion_id) AS criterion_count,
    COUNT(e.evaluation_id) AS evaluation_count
FROM categories cat
LEFT JOIN criteria c
    ON cat.category_id = c.category_id
LEFT JOIN evaluations e
    ON c.criterion_id = e.criterion_id
GROUP BY
    cat.category_id,
    cat.category_name
ORDER BY
    cat.category_id;


-- ============================================================
-- 13. FULL JOIN VALIDATION
-- ============================================================

SELECT
    e.evaluation_id,
    v.vendor_name,
    cat.category_name,
    c.criterion_name,
    e.evaluation_status,
    e.assigned_score,
    e.rating
FROM evaluations e
INNER JOIN vendors v
    ON e.vendor_id = v.vendor_id
INNER JOIN criteria c
    ON e.criterion_id = c.criterion_id
INNER JOIN categories cat
    ON c.category_id = cat.category_id
ORDER BY
    e.evaluation_id
LIMIT 20;


-- ============================================================
-- 14. VENDOR SCORE SUMMARY
-- ============================================================

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
    average_score DESC;