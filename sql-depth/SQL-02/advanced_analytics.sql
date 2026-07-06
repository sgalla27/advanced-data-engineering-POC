--Recursive Cycles
WITH RECURSIVE ordered_events AS (
    SELECT
        claim_id,
        event_type,
        ROW_NUMBER() OVER (
            PARTITION BY claim_id
            ORDER BY event_date
        ) AS rn
    FROM claim_events
),
event_path AS (
  SELECT
    claim_id,
    rn,
    event_type::TEXT AS PATH
  FROM ordered_events
  WHERE rn = 1

  UNION ALL

  SELECT
    o.claim_id,
    o.rn,
    CONCAT(p.path, ' -> ', o.event_type)::TEXT

  FROM ordered_events o 
  JOIN event_path p
    ON o.claim_id = p.claim_id AND o.rn = p.rn + 1
)
SELECT *
FROM event_path;

--Pivot-style queries
SELECT
  SUM(CASE WHEN claim_status = 'OPEN' THEN 1 ELSE 0 END) AS open_count,
  SUM(CASE WHEN claim_status = 'CLOSED' THEN 1 ELSE 0 END) AS closed_count,
  SUM(CASE WHEN claim_status = 'PENDING' THEN 1 ELSE 0 END) AS pending_count
FROM claims;

--Create views for the queries 
CREATE VIEW vw_risk_summary AS
WITH claim_stats AS (
  SELECT policy_id,
    COUNT(*) FILTER (WHERE claim_date >= CURRENT_DATE - 30) AS claims_last_30d,
    SUM(amount) AS total_claimed
  FROM claims GROUP BY policy_id
),
policy_risk AS (
  SELECT p.policy_id, p.holder_name, p.premium * 12 AS annual_premium,
    cs.claims_last_30d, cs.total_claimed,
    CASE WHEN cs.claims_last_30d > 2 AND cs.total_claimed > p.premium * 24
         THEN 'HIGH RISK' ELSE 'OK' END AS fraud_risk_flag
  FROM policy p JOIN claim_stats cs USING(policy_id)
)
SELECT * FROM policy_risk WHERE fraud_risk_flag = 'HIGH RISK';



CREATE VIEW vw_claim_status_summary AS
SELECT
  SUM(CASE WHEN claim_status = 'OPEN' THEN 1 ELSE 0 END) AS open_count,
  SUM(CASE WHEN claim_status = 'CLOSED' THEN 1 ELSE 0 END) AS closed_count,
  SUM(CASE WHEN claim_status = 'PENDING' THEN 1 ELSE 0 END) AS pending_count
FROM claims;