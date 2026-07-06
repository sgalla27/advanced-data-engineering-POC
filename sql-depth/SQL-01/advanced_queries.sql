
-- Query 1
-- Rank policies by premium within each policy_type


SELECT
    policy_id,
    policy_type,
    premium,
    RANK() OVER (
        PARTITION BY policy_type
        ORDER BY premium DESC
    ) AS premium_rank
FROM policy;



-- Query 2
-- Running total of claim amounts per policy
-- ordered by claim_date


SELECT
    claim_id,
    policy_id,
    claim_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY policy_id
        ORDER BY claim_date
        ROWS BETWEEN UNBOUNDED PRECEDING
             AND CURRENT ROW
    ) AS running_total
FROM claims;



-- Current claim amount vs previous claim amount
-- using LAG


SELECT
    claim_id,
    policy_id,
    claim_date,
    amount AS current_claim_amount,
    LAG(amount) OVER (
        PARTITION BY policy_id
        ORDER BY claim_date
    ) AS previous_claim_amount
FROM claims;


-- Query 4
-- CTE: Policies with more than 1 OPEN claim
-- Potential fraud flag

WITH open_claims AS (
    SELECT
        policy_id,
        COUNT(*) AS open_claim_count
    FROM claims
    WHERE claim_status = 'OPEN'
    GROUP BY policy_id
)

SELECT
    policy_id,
    open_claim_count,
    'POTENTIAL_FRAUD' AS fraud_flag
FROM open_claims
WHERE open_claim_count > 1;



-- Query 5
-- Classify claims into LOW/MED/HIGH buckets
-- using NTILE(3)


WITH claim_buckets AS (
    SELECT
        claim_id,
        policy_id,
        amount,
        NTILE(3) OVER (
            ORDER BY amount
        ) AS bucket
    FROM claims
)

SELECT
    claim_id,
    policy_id,
    amount,
    CASE
        WHEN bucket = 1 THEN 'LOW'
        WHEN bucket = 2 THEN 'MED'
        WHEN bucket = 3 THEN 'HIGH'
    END AS claim_risk_level
FROM claim_buckets;