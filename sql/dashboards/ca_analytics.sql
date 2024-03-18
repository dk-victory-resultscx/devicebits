CREATE TABLE analytics_rpt.ca_analytics AS (
	SELECT
		CASE
			WHEN pageviews.customer IS NULL AND LOWER(pageviews.page_url) LIKE '%rms.devicebits.com%' 
			THEN 'resultsmsca'
			ELSE pageviews.customer
		END AS customer
		,DATE(pageviews.timestamp) AS timestamp_date
		,DATE_SUB(
			DATE(pageviews.timestamp), 
			INTERVAL EXTRACT(DAYOFWEEK FROM DATE(pageviews.timestamp)) -2 DAY
		) AS timestamp_week
		,DATE(
			EXTRACT(YEAR FROM DATE(pageviews.timestamp)), 
			EXTRACT(MONTH FROM DATE(pageviews.timestamp)), 1
		) AS timestamp_month
		,DATE(
			EXTRACT(YEAR FROM DATE(pageviews.timestamp)), 
			CASE 
				EXTRACT(Quarter FROM DATE(pageviews.timestamp))
				WHEN 1 THEN 1
				WHEN 2 THEN 4
				WHEN 3 THEN 7
				ELSE 9
			END, 1
		) AS timestamp_quarter
		,DATE(EXTRACT(YEAR FROM DATE(pageviews.timestamp)), 1, 1) AS timestamp_year
		
		,COUNT(
			SAFE_CAST(
				REGEXP_REPLACE(
					SPLIT(
						SPLIT(LOWER(pageviews.page_url), '/')[
						SAFE_OFFSET(
							ARRAY_LENGTH(
								SPLIT(LOWER(pageviews.page_url), '/')
							) -1
						)], '?'
					) [SAFE_OFFSET(0)], '[^0-9 ]', ''
				) AS INT64
			)
		) AS content_id_count
		,COUNT(pageviews.page_url) AS pageview_count
		,COUNT(DISTINCT(pageviews.user_email)) AS user_count
		,COUNT(DISTINCT(pageviews.session_id)) AS session_count
		,SUM(
			CASE
				WHEN LOWER(pageviews.page_url) LIKE '%/tutorial%/%' THEN 1
				WHEN LOWER(pageviews.page_url) LIKE '%/faq%/%' THEN 1
				WHEN LOWER(pageviews.page_url) LIKE '%/guide%/%' THEN 1
				WHEN LOWER(pageviews.page_url) LIKE '%/video%/%' THEN 1
			END
		) AS content_view_count
		,COUNT(searches.search_term)
	FROM analytics-238714.analytics.ca_pageviews pageviews
	LEFT JOIN analytics-238714.analytics.ca_search searches
		ON pageviews.customer = searches.customer
		AND DATE(pageviews.timestamp) = DATE(searches.timestamp)
		AND LOWER(searches.action) != 'revise'
	WHERE
		pageviews.customer IS NOT NULL
		AND LOWER(pageviews.user_email) NOT LIKE '%@results-cx%'
		AND LOWER(pageviews.user_email) NOT LIKE '%@supportpredict%'
		AND LOWER(pageviews.user_email) NOT LIKE '%@devicebits%'
		AND DATE(pageviews.timestamp) > CAST('2020-12-31' AS DATE)		
	GROUP BY
		pageviews.customer
		,DATE(pageviews.timestamp)
)