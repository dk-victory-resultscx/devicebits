SELECT
  *
FROM  (
  SELECT
    cgenfbk.customer
    ,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', cgenfbk.timestamp, 'America/New_York') AS DATE) AS timestamp
    ,cgenfbk.page_url
    ,cgenfbk.comment
    ,cgenfbk.last_article
    ,COUNT(cgenfbk.page_url) AS pageview_count
  FROM analytics.ca_general_feedback cgenfbk
  GROUP BY
    cgenfbk.customer
    ,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', cgenfbk.timestamp, 'America/New_York') AS DATE)
    ,cgenfbk.page_url
    ,cgenfbk.comment
    ,cgenfbk.last_article
)
ORDER BY 2 DESC