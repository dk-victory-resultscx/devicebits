SELECT
  *
FROM (
  SELECT
    apageviews.customer
    ,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', apageviews.timestamp, 'America/New_York') AS DATE) AS pageview_date
    ,apageviews.referrer_url --needed?
    ,apageviews.page_url
    ,COUNT(apageviews.page_url) AS pageview_count
  FROM analytics.acad_pageviews apageviews
  GROUP BY
    customer
    ,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', apageviews.timestamp, 'America/New_York') AS DATE)
    ,apageviews.referrer_url
    ,apageviews.page_url
)
ORDER BY 2 DESC