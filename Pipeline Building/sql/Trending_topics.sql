/*
This query gives quick insights like:

- Which publishers talk most about marketing
- Whether coverage is mostly positive or negative
- Which sources dominate the dataset 
*/
SELECT
    source_name,
    sentiment_bucket,
    COUNT(*) AS total_articles
FROM `project-id.marketlens_data.news_articles`
GROUP BY source_name, sentiment_bucket
ORDER BY total_articles DESC;
