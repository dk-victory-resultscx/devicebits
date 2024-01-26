CREATE TABLE analytics_rpt.ca_pageviews AS (
    SELECT
        customer
        ,timestamp_date
        ,timestamp_weekbegin
        ,timestamp_month
        ,timestamp_quarter
        ,timestamp_year

        ,page_url
        ,name AS content_name
        ,content_id
        ,COUNT(content_id) AS content_id_count
        ,COUNT(page_url) AS pageview_count
        ,COUNT(DISTINCT(user_email)) AS user_count
        ,COUNT(DISTINCT(session_id)) AS session_count
        
    FROM analytics_gds.ca_pageviews
    WHERE
        (
        customer IS NOT NULL
        OR LOWER(user_email) not like '%@results-cx.com%'
        OR LOWER(user_email) not like '%@supportpredict.com%'
        OR LOWER(user_email) not like '%@deviceibits.com%'
        )
        AND timestamp_date > CAST('2020-12-31' AS DATE)
    GROUP BY
        customer
        ,timestamp_date
        ,timestamp_weekbegin
        ,timestamp_month
        ,timestamp_quarter
        ,timestamp_year
        ,page_url
        ,content_name
        ,content_id
)