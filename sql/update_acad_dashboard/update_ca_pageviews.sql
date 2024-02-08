------------------------------------------------------------------------------------------------
---------------------------------- Query Information ------------------------------------------- 
------------------------------------------------------------------------------------------------
-- Project ID: analytics-238714
-- Dataset: analytics_rpt
-- View/Table Name: ca_pageviews
-- Created: January 26, 2024
-- Created by: Dk Victory
------------------------------------------------------------------------------------------------
BEGIN 
	BEGIN TRANSACTION; 
	IF EXISTS (
		SELECT
			DISTINCT
			timestamp_date
		FROM analytics_rpt.ca_pageviews
		WHERE
			timestamp_date > (CURRENT_DATE - 4)
			OR timestamp_date < DATE_SUB(CURRENT_DATE, INTERVAL 2 YEAR)
	) 
	THEN 
		DELETE FROM analytics_rpt.ca_pageviews
		WHERE
			timestamp_date > (CURRENT_DATE - 4)
			OR timestamp_date < DATE_SUB(CURRENT_DATE, INTERVAL 2 YEAR);
	END IF; 
	
	INSERT INTO analytics_rpt.ca_pageviews (
		SELECT
			customer
			,timestamp_date
			,timestamp_weekbegin
			,timestamp_month
			,timestamp_quarter
			,timestamp_year

			,page_url
			,name AS content_name
            ,content_type
            ,action
			,content_id
			,COUNT(content_id) AS content_id_count
			,COUNT(page_url) AS pageview_count
			,COUNT(DISTINCT(user_email)) AS user_count
			,COUNT(DISTINCT(session_id)) AS session_count
			
		FROM analytics_gds.ca_pageviews
		WHERE
			customer IS NOT NULL
            AND LOWER(user_email) not like '%@results-cx%'
            AND LOWER(user_email) not like '%@supportpredict%'
            AND LOWER(user_email) not like '%@devicebits%'
            AND timestamp_date > CAST('2020-12-31' AS DATE)
			AND timestamp_date > (CURRENT_DATE - 4)
		GROUP BY
			customer
			,timestamp_date
			,timestamp_weekbegin
			,timestamp_month
			,timestamp_quarter
			,timestamp_year
			,page_url
			,content_name
            ,content_type
            ,action
			,content_id
	);
	
	COMMIT TRANSACTION; 
	EXCEPTION 
		WHEN ERROR 
		THEN -- Roll back the transaction inside the exception handler. 
			SELECT @@error.message; 
	ROLLBACK TRANSACTION; 
END;