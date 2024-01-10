SELECT
  *
FROM (
	SELECT
		pageviews.customer
		,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', pageviews.timestamp, 'America/New_York') AS DATE) AS pageview_date
		,pageviews.page_url
		,COUNT(pageviews.page_url) AS pageview_count
	FROM analytics.ca_pageviews pageviews
	WHERE
		pageviews.customer IS NOT NULL
		OR LOWER(pageviews.user_email) not like '%@results-cx.com%'
		OR LOWER(pageviews.user_email) not like '%@supportpredict.com%'
		OR LOWER(pageviews.user_email) not like '%@deviceibits.com%'
	GROUP BY
		pageviews.customer
		,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', pageviews.timestamp, 'America/New_York') AS DATE)
		,pageviews.page_url
)
ORDER BY 2 DESC