------------------------------------------------------------------------------------------------
---------------------------------- Query Information ------------------------------------------- 
------------------------------------------------------------------------------------------------
-- Project ID: analytics-238714
-- Dataset: analytics_rpt
-- View/Table Name: ca_kendrasearch
-- Created: January 26, 2024
-- Created by: Dk Victory
------------------------------------------------------------------------------------------------
BEGIN 
	BEGIN TRANSACTION; 
	IF EXISTS (
		SELECT
			DISTINCT
			timestamp_date
		FROM analytics_rpt.ca_kendrasearch
		WHERE
			timestamp_date > (CURRENT_DATE - 4)
			OR timestamp_date < DATE_SUB(CURRENT_DATE, INTERVAL 2 YEAR)
	) 
	THEN 
		DELETE FROM analytics_rpt.ca_kendrasearch
		WHERE
			timestamp_date > (CURRENT_DATE - 4)
			OR timestamp_date < DATE_SUB(CURRENT_DATE, INTERVAL 2 YEAR);
	END IF; 
	
	INSERT INTO analytics_rpt.ca_kendrasearch (
		SELECT
			customer
			,timestamp_date
			,timestamp_weekbegin
			,timestamp_month
			,timestamp_quarter
			,timestamp_year

			,action
			,search_term
			,COUNT(search_term) AS search_term_count
			,COUNT(DISTINCT(user_email)) AS user_count
			,COUNT(DISTINCT(session_id)) AS session_count
			
		FROM analytics_gds.ca_kendrasearch
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
			,action
			,search_term
	);
	
	COMMIT TRANSACTION; 
	EXCEPTION 
		WHEN ERROR 
		THEN -- Roll back the transaction inside the exception handler. 
			SELECT @@error.message; 
	ROLLBACK TRANSACTION; 
END;