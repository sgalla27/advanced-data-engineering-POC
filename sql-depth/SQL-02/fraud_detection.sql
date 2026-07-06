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