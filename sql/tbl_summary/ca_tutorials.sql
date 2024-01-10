SELECT
  *
FROM  (
  SELECT
    ctut.customer
    ,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', ctut.timestamp, 'America/New_York') AS DATE) AS timestamp
    ,ctut.page_url
    ,ctut.action
    ,ctut.helpful
    ,ctut.comment
    ,ctut.rating_percent
    ,COUNT(ctut.page_url) AS pageview_count
  FROM analytics.ca_tutorials ctut
  GROUP BY
    ctut.customer
    ,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', ctut.timestamp, 'America/New_York') AS DATE)
    ,ctut.page_url
    ,ctut.action
    ,ctut.helpful
    ,ctut.comment
    ,ctut.rating_percent
)
ORDER BY 2 DESC