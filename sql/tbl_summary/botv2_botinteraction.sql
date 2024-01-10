SELECT
  *
FROM  (
  SELECT
    b_interaction.botname
    ,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', b_interaction.timestamp, 'America/New_York') AS DATE) AS pageview_date
    ,b_interaction.module_title
    ,b_interaction.reply
    ,COUNT(b_interaction.reply) AS replay_count
  FROM analytics.botv2_botinteraction b_interaction
  GROUP BY
    b_interaction.botname
    ,SAFE_CAST(FORMAT_TIMESTAMP('%Y-%m-%d', b_interaction.timestamp, 'America/New_York') AS DATE)
    ,b_interaction.module_title
    ,b_interaction.reply
)
ORDER BY 2 DESC