CREATE TABLE analytics_rpt.acad_content_usage AS (
    SELECT
        customer
        ,event_date
        ,DATE(event_date) AS daily
        ,DATE_SUB(DATE(event_date), INTERVAL EXTRACT(DAYOFWEEK FROM DATE(event_date))-2 DAY) AS weekly
        ,DATE(EXTRACT(YEAR FROM DATE(event_date)), EXTRACT(MONTH FROM DATE(event_date)), 1) AS monthly
        ,DATE(EXTRACT(YEAR FROM DATE(event_date)), 
                        CASE EXTRACT(Quarter FROM DATE(event_date))
                                WHEN 1 THEN 1
                                WHEN 2 THEN 4
                                WHEN 3 THEN 7
                                ELSE 9
                        END, 1) AS quarterly
        ,DATE(EXTRACT(YEAR FROM DATE(event_date)), 1, 1) AS yearly
        ,content_type
        ,evnt_url
        ,SUM(CASE WHEN evnt_cat_name='page_view' THEN 1 ELSE 0 END) AS overall_pageview        
        ,COUNT(DISTINCT(CONCAT(user_pseudo_id,evnt_ga_session_id))) AS sessions_count  
        ,SUM(CASE WHEN evnt_cat_name = 'session_start' THEN evnt_engaged_session_event ELSE NULL END) AS engaged_sessions      
        
        ,COUNT(DISTINCT(user_pseudo_id)) AS total_users
        ,SUM(CASE WHEN evnt_cat_name = 'first_visit' THEN 1 ELSE 0 END) AS new_users

        ,(SUM(CASE WHEN evnt_cat_name = 'session_start' THEN evnt_engaged_session_event ELSE NULL END) - 
            COUNT(DISTINCT(CASE WHEN evnt_cat_name='Contact Us' THEN CONCAT(user_pseudo_id,evnt_ga_session_id) ELSE NULL END))) / 
            SUM(CASE WHEN evnt_cat_name = 'session_start' THEN evnt_engaged_session_event ELSE NULL END) AS containment_rate               
        ,COUNT(DISTINCT(CASE WHEN evnt_cat_name='Contact Us' THEN CONCAT(user_pseudo_id,evnt_ga_session_id) ELSE NULL END)) AS contact_us
        
        ,SUM(CASE WHEN evnt_cat_name = 'Positive' THEN 1 ELSE 0 END) AS feedback_postive
        ,SUM(CASE WHEN evnt_cat_name = 'Negative' THEN 1 ELSE 0 END) AS feedback_negative
        ,(SUM(CASE WHEN evnt_cat_name = 'Positive' THEN 1 ELSE 0 END) + SUM(CASE WHEN evnt_cat_name = 'Negative' THEN 1 ELSE 0 END)) AS feedback_count 

        ,SUM(CASE WHEN evnt_cat_name = 'session_start' THEN evnt_engaged_session_event ELSE NULL END) / COUNT(DISTINCT((CONCAT(user_pseudo_id,evnt_ga_session_id)))) AS engagement_rate
        ,(SUM(evnt_engagement_time_msec)/1000) AS engagement_time
        ,(SUM(evnt_engagement_time_msec)/1000) / SUM(CASE WHEN evnt_cat_name = 'session_start' THEN evnt_engaged_session_event ELSE NULL END) AS avg_engagement_time
    FROM analytics_gds.ga4_events
    WHERE
        TRIM(LOWER(content_type)) = 'device home'
        OR LOWER(content_type) not like '%home'
    GROUP BY
        customer
        ,event_date
        ,content_type
        ,evnt_url
)