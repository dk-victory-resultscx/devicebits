CREATE TABLE analytics_rpt.ca_feedbackshares AS (
    SELECT
        customer
        ,timestamp_date
        ,timestamp_weekbegin
        ,timestamp_month
        ,timestamp_quarter
        ,timestamp_year

        ,action
        ,helpful
        ,rating_percent
        ,content_type
        ,content_id
        ,COUNT(content_id) AS content_id_count
        ,COUNT(DISTINCT(content_id)) AS distinct_content_id_count
        ,COUNT(DISTINCT(user_email)) AS user_count
        ,COUNT(DISTINCT(session_id)) AS session_count
        
    FROM analytics_gds.ca_feedbackshares
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
        ,action
        ,helpful
        ,rating_percent
        ,content_type
        ,content_id
)