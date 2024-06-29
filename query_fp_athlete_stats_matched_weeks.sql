/*available weeks from playerStatistics and Fantasy Pros tables*/
SELECT DISTINCT ps.week
FROM playerStatistics ps
JOIN fantasy_pros_QB fp on ps.week = 'Week' || fp.week
WHERE ps.weekStart LIKE('%2023%') /*manually change the year*/
UNION ALL
SELECT DISTINCT week
FROM fantasy_pros_QB /*change the table for a different position (fantasy_pros_RB, fantasy_pros_WR,fantasy_pros_TE)*/
WHERE season = 2023 /*manually change the year*/
ORDER BY week;