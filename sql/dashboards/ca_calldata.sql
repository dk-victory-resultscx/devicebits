CREATE TABLE analytics_rpt.ca_calldata AS (
    SELECT
        customer
        ,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', timestamp, 'America/New_York') AS DATE) AS timestamp_date
        ,timestamp_weekbegin
        ,timestamp_month
        ,timestamp_quarter
        ,timestamp_year

        ,action
        ,resolved
        ,COUNT(call_session_id) AS call_count
        ,COUNT(DISTINCT(call_session_id)) AS distinct_call_count
        ,SUM(duration) AS call_duration
        ,COUNT(DISTINCT(user_email)) AS user_count
        ,COUNT(DISTINCT(session_id)) AS session_count
        
    FROM analytics_gds.ca_calldata
    WHERE
        (
        customer IS NOT NULL
        OR LOWER(user_email) not like '%@results-cx.com%'
        OR LOWER(user_email) not like '%@supportpredict.com%'
        OR LOWER(user_email) not like '%@deviceibits.com%'
        )
        AND SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', timestamp, 'America/New_York') AS DATE) > CAST('2020-12-31' AS DATE)
    GROUP BY
        customer
        ,timestamp_date
        ,timestamp_weekbegin
        ,timestamp_month
        ,timestamp_quarter
        ,timestamp_year
        ,action
        ,resolved
)