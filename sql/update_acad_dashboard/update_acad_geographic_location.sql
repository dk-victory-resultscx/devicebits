------------------------------------------------------------------------------------------------
---------------------------------- Query Information ------------------------------------------- 
------------------------------------------------------------------------------------------------
-- Project ID: analytics-238714
-- Dataset: analytics_rpt
-- View/Table Name: acad_geographic_location
-- Created: January 12, 2024
-- Created by: Dk Victory
------------------------------------------------------------------------------------------------
BEGIN 
	BEGIN TRANSACTION; 
	IF EXISTS (
		SELECT
			DISTINCT event_date
		FROM analytics_rpt.acad_geographic_location
		WHERE
			event_date > (CURRENT_DATE - 4)
	) 
	THEN 
		DELETE FROM analytics_rpt.acad_geographic_location
		WHERE
			event_date > (CURRENT_DATE - 4);
	END IF; 
	
	INSERT INTO analytics_rpt.acad_geographic_location (
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
			,geo_continent
			,geo_sub_continent
			,geo_country
			,CASE
			  WHEN TRIM(geo_city) = ''
			  THEN NULL
			  ELSE geo_city
			END AS geo_city
			,CASE
			  WHEN TRIM(geo_metro) = ''
			  THEN NULL
			  WHEN TRIM(geo_metro) = '(not set)'
			  THEN NULL
			  ELSE geo_metro
			END AS geo_metro
			,language
			,SUM(CASE WHEN evnt_cat_name='page_view' THEN 1 ELSE 0 END) AS pageview_count
			,COUNT(DISTINCT(CONCAT(user_pseudo_id,evnt_ga_session_id))) AS sessions_count
			,SUM(CASE WHEN evnt_cat_name = 'session_start' THEN evnt_engaged_session_event ELSE NULL END) / COUNT(DISTINCT((CONCAT(user_pseudo_id,evnt_ga_session_id)))) AS engagement_rate
			,COUNT(DISTINCT(user_pseudo_id)) AS total_users
			,SUM(CASE WHEN evnt_cat_name = 'first_visit' THEN 1 ELSE 0 END) AS new_users
			,(SUM(CASE WHEN evnt_cat_name = 'session_start' THEN evnt_engaged_session_event ELSE NULL END) - 
			COUNT(DISTINCT(CASE WHEN evnt_cat_name='Contact Us' THEN CONCAT(user_pseudo_id,evnt_ga_session_id) ELSE NULL END))) / 
			SUM(CASE WHEN evnt_cat_name = 'session_start' THEN evnt_engaged_session_event ELSE NULL END) AS containment_rate
			,(SUM(CASE WHEN evnt_cat_name = 'Positive' THEN 1 ELSE 0 END) + SUM(CASE WHEN evnt_cat_name = 'Negative' THEN 1 ELSE 0 END)) AS feedback_count
			,(SUM(evnt_engagement_time_msec)/1000) / SUM(CASE WHEN evnt_cat_name = 'session_start' THEN evnt_engaged_session_event ELSE NULL END) AS avg_engagement_time
		FROM analytics_gds.ga4_events
        WHERE
			event_date > (CURRENT_DATE - 4)
		GROUP BY
			customer
			,event_date
			,geo_continent
			,geo_sub_continent
			,geo_country
			,geo_city
			,geo_metro
			,language		
	);
	
	COMMIT TRANSACTION; 
	EXCEPTION 
		WHEN ERROR 
		THEN -- Roll back the transaction inside the exception handler. 
			SELECT @@error.message; 
	ROLLBACK TRANSACTION; 
END;