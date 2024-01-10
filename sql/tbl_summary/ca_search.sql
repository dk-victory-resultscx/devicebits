SELECT
  *
FROM  (
  SELECT
    csearch.customer
    ,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', csearch.timestamp, 'America/New_York') AS DATE) AS timestamp
    ,csearch.search_term
    ,COUNT(csearch.search_term) AS search_count
  FROM analytics.ca_search csearch
  WHERE
    LOWER(TRIM(action)) != 'revise'
  GROUP BY
    csearch.customer
    ,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', csearch.timestamp, 'America/New_York') AS DATE)
    ,csearch.search_term
)
ORDER BY 2 DESC