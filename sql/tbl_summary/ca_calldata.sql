SELECT
  *
FROM  (
  SELECT
    ccalldata.customer
    ,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', ccalldata.timestamp, 'America/New_York') AS DATE) AS pageview_date
    ,ccalldata.action
    ,ccalldata.first_article_name --include?
    ,ccalldata.last_article_name --include?
    ,ccalldata.page_url
    ,COUNT(ccalldata.page_url) AS pageview_count
  FROM analytics.ca_calldata ccalldata
  WHERE
    ccalldata.customer IS NOT NULL
    OR LOWER(ccalldata.user_email) not like '%@results-cx.com%'
    OR LOWER(ccalldata.user_email) not like '%@supportpredict.com%'
    OR LOWER(ccalldata.user_email) not like '%@deviceibits.com%'
  GROUP BY
    ccalldata.customer
    ,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', ccalldata.timestamp, 'America/New_York') AS DATE)
    ,ccalldata.action
    ,ccalldata.first_article_name
    ,ccalldata.last_article_name
    ,ccalldata.page_url
)
ORDER BY 2 DESC