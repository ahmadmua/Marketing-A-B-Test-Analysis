-- Sanity check: row count + group split
SELECT test_group,
       COUNT(*)                                            AS users,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct_of_total
FROM ab_test
GROUP BY test_group;
-- 96% ad / 4% PSA — imbalance

-- Core conversion rates by group
SELECT test_group,
       COUNT(*)                                      AS total_users,
       SUM(converted::int)                           AS conversions,
       ROUND(AVG(converted::int) * 100, 4)           AS conversion_rate_pct
FROM ab_test
GROUP BY test_group;

-- Conversion rate by ad exposure frequency (segmentation)
SELECT test_group,
       total_ads,
       COUNT(*)                                      AS users,
       ROUND(AVG(converted::int) * 100, 2)           AS conversion_rate_pct
FROM ab_test
GROUP BY test_group, total_ads
ORDER BY test_group, total_ads;

--  Day-of-week pattern (the days users most often saw the ad)
SELECT most_ads_day,
       test_group,
       COUNT(*)                                      AS users,
       ROUND(AVG(converted::int) * 100, 2)           AS conversion_rate_pct
FROM ab_test
GROUP BY most_ads_day, test_group
ORDER BY most_ads_day;

-- Hour-of-day pattern
SELECT most_ads_hour,
       test_group,
       COUNT(*)                                      AS users,
       ROUND(AVG(converted::int) * 100, 2)           AS conversion_rate_pct
FROM ab_test
GROUP BY most_ads_hour, test_group
ORDER BY most_ads_hour;

