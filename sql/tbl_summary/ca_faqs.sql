SELECT
  *
FROM  (
  SELECT
    cfaq.customer
    ,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', cfaq.timestamp, 'America/New_York') AS DATE) AS timestamp
    ,cfaq.page_url
    ,cfaq.action
    ,cfaq.faq_name --tutorials?
    ,cfaq.comment
    ,cfaq.rating_percent
    ,COUNT(cfaq.page_url) AS pageview_count
  FROM analytics.ca_faqs cfaq
  GROUP BY
    cfaq.customer
    ,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', cfaq.timestamp, 'America/New_York') AS DATE)
    ,cfaq.page_url
    ,cfaq.action
    ,cfaq.faq_name
    ,cfaq.comment
    ,cfaq.rating_percent
)
ORDER BY 2 DESC