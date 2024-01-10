SELECT
  *
FROM  (
  SELECT
    asearch.customer
    ,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', asearch.timestamp, 'America/New_York') AS DATE) AS timestamp
    ,asearch.link_to
    ,asearch.search_term
    ,COUNT(asearch.search_term) AS search_count
  FROM analytics.acad_search asearch
  WHERE
    LOWER(TRIM(action)) != 'revise'
  GROUP BY
    asearch.customer
    ,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', asearch.timestamp, 'America/New_York') AS DATE)
    ,asearch.link_to
    ,asearch.search_term
)
ORDER BY 2 DESC