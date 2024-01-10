SELECT
  *
FROM  (
  SELECT
    ckendrasearch.customer
    ,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', ckendrasearch.timestamp, 'America/New_York') AS DATE) AS timestamp
    ,ckendrasearch.search_term
    ,COUNT(ckendrasearch.search_term) AS search_count
  FROM analytics.ca_kendrasearch ckendrasearch
  WHERE
    LOWER(TRIM(action)) != 'revise'
  GROUP BY
    ckendrasearch.customer
    ,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', ckendrasearch.timestamp, 'America/New_York') AS DATE)
    ,ckendrasearch.search_term
)
ORDER BY 2 DESC