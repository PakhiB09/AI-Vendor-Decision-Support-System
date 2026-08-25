-- ============================================================
-- VENDOR DECISION-SUPPORT DATABASE SCHEMA
-- STEP 23.2
-- ============================================================

CREATE DATABASE IF NOT EXISTS vendor_decision_support;

USE vendor_decision_support;


-- ============================================================
-- 1. VENDORS
-- ============================================================

CREATE TABLE IF NOT EXISTS vendors (
    vendor_id VARCHAR(10) PRIMARY KEY,
    vendor_name VARCHAR(100) NOT NULL UNIQUE
);


-- ============================================================
-- 2. EVALUATION CATEGORIES
-- ============================================================

CREATE TABLE IF NOT EXISTS categories (
    category_id VARCHAR(10) PRIMARY KEY,
    category_name VARCHAR(150) NOT NULL UNIQUE
);


-- ============================================================
-- 3. EVALUATION CRITERIA
-- ============================================================

CREATE TABLE IF NOT EXISTS criteria (
    criterion_id VARCHAR(10) PRIMARY KEY,
    category_id VARCHAR(10) NOT NULL,
    criterion_name VARCHAR(150) NOT NULL UNIQUE,

    CONSTRAINT fk_criteria_category
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
);


-- ============================================================
-- 4. VENDOR EVALUATIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS evaluations (
    evaluation_id VARCHAR(10) PRIMARY KEY,

    vendor_id VARCHAR(10) NOT NULL,
    criterion_id VARCHAR(10) NOT NULL,

    evaluation_status VARCHAR(30) NOT NULL,

    assigned_score DECIMAL(3,1) NULL,

    rating VARCHAR(50) NULL,

    score_justification TEXT,

    evidence_summary TEXT,

    source_type VARCHAR(255),

    source_url TEXT,

    evidence_confidence VARCHAR(30),

    evaluation_notes TEXT,

    CONSTRAINT fk_evaluations_vendor
        FOREIGN KEY (vendor_id)
        REFERENCES vendors(vendor_id),

    CONSTRAINT fk_evaluations_criterion
        FOREIGN KEY (criterion_id)
        REFERENCES criteria(criterion_id),

    CONSTRAINT uq_vendor_criterion
        UNIQUE (vendor_id, criterion_id),

    CONSTRAINT chk_evaluation_status
        CHECK (
            evaluation_status IN (
                'Evaluated',
                'Not Evaluated'
            )
        ),

    CONSTRAINT chk_assigned_score
        CHECK (
            assigned_score IS NULL
            OR assigned_score BETWEEN 1 AND 5
        )
);


-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX idx_criteria_category
    ON criteria(category_id);

CREATE INDEX idx_evaluations_vendor
    ON evaluations(vendor_id);

CREATE INDEX idx_evaluations_criterion
    ON evaluations(criterion_id);

CREATE INDEX idx_evaluations_status
    ON evaluations(evaluation_status);