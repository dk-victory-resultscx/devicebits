SELECT
    customer
    --,event_date
    ,event_timestamp
    ,wbinfo_hostname
    ,evnt_cat_name
    ,content_type
    ,evnt_url
    ,evnt_page_title
    ,evnt_session_engaged
    ,evnt_ga_session_id
    ,user_pseudo_id
    ,trfi_name
    ,trfi_medium
    ,trfi_source
    ,trfi_channel_grouping_user
    ,wbinfo_browser
    ,wbinfo_browser_version
    ,geo_continent
    ,geo_sub_continent
    ,geo_country
    ,geo_city
    ,geo_metro
    ,dvce_category
    ,dvce_is_limited_ad_tracking
    ,dvce_mobile_brand_name
    ,dvce_mobile_marketing_name
    ,dvce_operating_system
    ,dvce_operating_system_version
    ,language
FROM analytics_gds.ga4_events
WHERE
    event_date BETWEEN '2023-12-31' AND '2024-01-06'
    AND customer = 'docomopacific'
