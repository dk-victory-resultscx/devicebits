------------------------------------------------------------------------------------------------
---------------------------------- Query Information ------------------------------------------- 
------------------------------------------------------------------------------------------------
-- Project ID: analytics-238714
-- Dataset: analytics_rpt
-- View/Table Name: acad_404s
-- Created: January 12, 2024
-- Created by: Dk Victory
------------------------------------------------------------------------------------------------
BEGIN 
	BEGIN TRANSACTION; 
	IF EXISTS (
		SELECT
			DISTINCT event_date
		FROM analytics_rpt.acad_404s
		WHERE
			event_date > (CURRENT_DATE - 4)
	) 
	THEN 
		DELETE FROM analytics_rpt.acad_404s
		WHERE
			event_date > (CURRENT_DATE - 4)
	END IF; 
	
	INSERT INTO analytics_rpt.acad_404s (
		SELECT
			a404.customer
			,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', a404.timestamp, 'America/New_York') AS DATE) AS event_date
			,DATE(SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', a404.timestamp, 'America/New_York') AS DATE)) AS daily
			,DATE_SUB(DATE(SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', a404.timestamp, 'America/New_York') AS DATE)), INTERVAL EXTRACT(DAYOFWEEK FROM DATE(SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', a404.timestamp, 'America/New_York') AS DATE)))-2 DAY) AS weekly
			,DATE(EXTRACT(YEAR FROM DATE(SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', a404.timestamp, 'America/New_York') AS DATE))), EXTRACT(MONTH FROM DATE(SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', a404.timestamp, 'America/New_York') AS DATE))), 1) AS monthly
			,DATE(EXTRACT(YEAR FROM DATE(SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', a404.timestamp, 'America/New_York') AS DATE))), 
							CASE EXTRACT(Quarter FROM DATE(SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', a404.timestamp, 'America/New_York') AS DATE)))
									WHEN 1 THEN 1
									WHEN 2 THEN 4
									WHEN 3 THEN 7
									ELSE 9
							END, 1) AS quarterly
			,DATE(EXTRACT(YEAR FROM DATE(SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', a404.timestamp, 'America/New_York') AS DATE))), 1, 1) AS yearly
			,CASE
			  WHEN TRIM(a404.originating_link) = ''
			  THEN NULL
			  ELSE a404.originating_link
			END AS originating_link
			,a404.page_url
			,COUNT(a404.page_url) AS pageview_count
		FROM analytics.acad_404s a404
		GROUP BY
			a404.customer
			--,a404.timestamp
			,event_date
			,a404.originating_link
			,a404.page_url
		WHERE
			event_date > (CURRENT_DATE - 4)
	);
	
	COMMIT TRANSACTION; 
	EXCEPTION 
		WHEN ERROR 
		THEN -- Roll back the transaction inside the exception handler. 
			SELECT @@error.message; 
	ROLLBACK TRANSACTION; 
    END;