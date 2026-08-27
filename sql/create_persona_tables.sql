USE vendor_decision_support;

-- ============================================================
-- STEP 23 - PERSONA AND WEIGHT TABLES
-- ============================================================

-- ============================================================
-- 1. PERSONAS
-- ============================================================

CREATE TABLE IF NOT EXISTS personas (
    persona_id VARCHAR(10) NOT NULL,
    persona_name VARCHAR(100) NOT NULL,
    persona_description TEXT,
    PRIMARY KEY (persona_id),
    UNIQUE KEY uq_persona_name (persona_name)
);


-- ============================================================
-- 2. PERSONA WEIGHTS
-- ============================================================

CREATE TABLE IF NOT EXISTS persona_weights (
    persona_id VARCHAR(10) NOT NULL,
    category_id VARCHAR(10) NOT NULL,
    weight DECIMAL(5,4) NOT NULL,
    weighting_rationale VARCHAR(500),

    PRIMARY KEY (persona_id, category_id),

    CONSTRAINT fk_persona_weights_persona
        FOREIGN KEY (persona_id)
        REFERENCES personas(persona_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_persona_weights_category
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_persona_weight
        CHECK (weight >= 0 AND weight <= 1)
);


-- ============================================================
-- 3. PERSONAS
-- ============================================================

INSERT INTO personas (
    persona_id,
    persona_name,
    persona_description
)
VALUES
(
    'P001',
    'Startup',
    'Prioritizes rapid development, agent capabilities, ease of implementation, and business value while maintaining practical enterprise safeguards.'
),
(
    'P002',
    'Enterprise',
    'Prioritizes balanced agent capabilities, integration, governance, security, scalability, and enterprise readiness.'
),
(
    'P003',
    'Healthcare',
    'Prioritizes governance, security, trust, compliance-oriented capabilities, and reliable enterprise deployment.'
),
(
    'P004',
    'Financial Services',
    'Prioritizes governance, security, trust, integration, reliability, and enterprise-grade operational capabilities.'
),
(
    'P005',
    'Public Sector',
    'Prioritizes governance, security, deployment flexibility, integration, scalability, and enterprise readiness.'
)
ON DUPLICATE KEY UPDATE
    persona_name = VALUES(persona_name),
    persona_description = VALUES(persona_description);


-- ============================================================
-- 4. PERSONA CATEGORY WEIGHTS
-- ============================================================
--
-- Category mapping:
--
-- CAT01 = Core Agent Intelligence
-- CAT02 = Agent Architecture & Development
-- CAT03 = Enterprise Integration & Deployment
-- CAT04 = Governance, Security & Trust
-- CAT05 = Enterprise Readiness & Business Value
--
-- Each persona totals 100%.
--


-- ------------------------------------------------------------
-- STARTUP
-- ------------------------------------------------------------

INSERT INTO persona_weights (
    persona_id,
    category_id,
    weight,
    weighting_rationale
)
VALUES
(
    'P001',
    'CAT01',
    0.30,
    'High priority on core agent intelligence and autonomous capabilities.'
),
(
    'P001',
    'CAT02',
    0.25,
    'High priority on development speed, agent creation, and implementation ease.'
),
(
    'P001',
    'CAT03',
    0.15,
    'Moderate priority on integration and deployment flexibility.'
),
(
    'P001',
    'CAT04',
    0.10,
    'Baseline governance and security requirements.'
),
(
    'P001',
    'CAT05',
    0.20,
    'Strong priority on business value, scalability, and practical outcomes.'
)
ON DUPLICATE KEY UPDATE
    weight = VALUES(weight),
    weighting_rationale = VALUES(weighting_rationale);


-- ------------------------------------------------------------
-- ENTERPRISE
-- ------------------------------------------------------------

INSERT INTO persona_weights (
    persona_id,
    category_id,
    weight,
    weighting_rationale
)
VALUES
(
    'P002',
    'CAT01',
    0.20,
    'Strong agent capabilities are important but balanced against enterprise requirements.'
),
(
    'P002',
    'CAT02',
    0.20,
    'Development flexibility and agent architecture are important for enterprise adoption.'
),
(
    'P002',
    'CAT03',
    0.20,
    'Integration and deployment across enterprise environments are important.'
),
(
    'P002',
    'CAT04',
    0.25,
    'Governance, security, trust, and operational controls receive elevated priority.'
),
(
    'P002',
    'CAT05',
    0.15,
    'Business value and scalability remain important decision factors.'
)
ON DUPLICATE KEY UPDATE
    weight = VALUES(weight),
    weighting_rationale = VALUES(weighting_rationale);


-- ------------------------------------------------------------
-- HEALTHCARE
-- ------------------------------------------------------------

INSERT INTO persona_weights (
    persona_id,
    category_id,
    weight,
    weighting_rationale
)
VALUES
(
    'P003',
    'CAT01',
    0.20,
    'Reliable agent intelligence is important for healthcare workflows.'
),
(
    'P003',
    'CAT02',
    0.15,
    'Development flexibility is relevant but secondary to trust and governance.'
),
(
    'P003',
    'CAT03',
    0.15,
    'Integration and deployment capabilities support healthcare environments.'
),
(
    'P003',
    'CAT04',
    0.35,
    'Highest priority is placed on governance, security, trust, and controlled operation.'
),
(
    'P003',
    'CAT05',
    0.15,
    'Enterprise readiness and business value remain important.'
)
ON DUPLICATE KEY UPDATE
    weight = VALUES(weight),
    weighting_rationale = VALUES(weighting_rationale);


-- ------------------------------------------------------------
-- FINANCIAL SERVICES
-- ------------------------------------------------------------

INSERT INTO persona_weights (
    persona_id,
    category_id,
    weight,
    weighting_rationale
)
VALUES
(
    'P004',
    'CAT01',
    0.20,
    'Strong agent intelligence is important for financial services automation.'
),
(
    'P004',
    'CAT02',
    0.15,
    'Agent architecture and development flexibility support controlled adoption.'
),
(
    'P004',
    'CAT03',
    0.15,
    'Integration and deployment capabilities are important for financial systems.'
),
(
    'P004',
    'CAT04',
    0.35,
    'Highest priority is placed on governance, security, trust, and control.'
),
(
    'P004',
    'CAT05',
    0.15,
    'Business value, scalability, and enterprise readiness remain important.'
)
ON DUPLICATE KEY UPDATE
    weight = VALUES(weight),
    weighting_rationale = VALUES(weighting_rationale);


-- ------------------------------------------------------------
-- PUBLIC SECTOR
-- ------------------------------------------------------------

INSERT INTO persona_weights (
    persona_id,
    category_id,
    weight,
    weighting_rationale
)
VALUES
(
    'P005',
    'CAT01',
    0.20,
    'Agent intelligence is important for automation and public-sector use cases.'
),
(
    'P005',
    'CAT02',
    0.15,
    'Development flexibility is useful but secondary to governance and deployment.'
),
(
    'P005',
    'CAT03',
    0.20,
    'Deployment flexibility and integration across government environments are important.'
),
(
    'P005',
    'CAT04',
    0.30,
    'High priority on governance, security, trust, and controlled deployment.'
),
(
    'P005',
    'CAT05',
    0.15,
    'Enterprise readiness, scalability, and business/public value remain relevant.'
)
ON DUPLICATE KEY UPDATE
    weight = VALUES(weight),
    weighting_rationale = VALUES(weighting_rationale);


-- ============================================================
-- FINAL CHECKS
-- ============================================================

SELECT
    'personas' AS table_name,
    COUNT(*) AS record_count
FROM personas

UNION ALL

SELECT
    'persona_weights',
    COUNT(*)
FROM persona_weights;