SELECT
    customer
    ,timestamp_date AS event_date
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
    ,action
    ,search_term
    ,count
    ,COUNT(action) AS action_count
FROM analytics_gds.acad_search
GROUP BY
    customer
    ,event_date
    ,action
    ,search_term
    ,count