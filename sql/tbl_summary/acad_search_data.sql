SELECT
    customer
    --,timestamp_date
    ,DATE(timestamp_date) AS daily
    ,DATE_SUB(DATE(timestamp_date), INTERVAL EXTRACT(DAYOFWEEK FROM DATE(timestamp_date))-2 DAY) AS weekly
    ,DATE(EXTRACT(YEAR FROM DATE(timestamp_date)), EXTRACT(MONTH FROM DATE(timestamp_date)), 1) AS monthly
    ,DATE(EXTRACT(YEAR FROM DATE(timestamp_date)), 
                    CASE EXTRACT(Quarter FROM DATE(timestamp_date))
                            WHEN 1 THEN 1
                            WHEN 2 THEN 4
                            WHEN 3 THEN 7
                            ELSE 9
                    END, 1) AS quarterly
    ,DATE(EXTRACT(YEAR FROM DATE(timestamp_date)), 1, 1) AS yearly
    ,session_id
    ,app_instance_id
    ,permanent_id
    ,action
    ,search_term
    ,link_to
    ,page_url
    ,event_category
    ,ip_address
FROM analytics_gds.acad_search
WHERE
    timestamp_date BETWEEN '2023-12-31' AND '2024-01-06'
    AND customer = 'docomopacific'