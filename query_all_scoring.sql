SELECT 
a.firstName || ' ' || a.lastName AS PlayerName,
p.position,
ps.RushingTouchdowns,
ps.ReceivingTouchdowns,
ps.ReturnTouchdowns,
ps.TotalTouchdowns,
ps.FieldGoals,
ps.KickExtraPoints,
ps.TotalTwoPointConversions,
ps.TotalPoints,
ps.TotalPointsPerGame
FROM playerStatistics ps
JOIN athletes a ON ps.playerFK = a.id
JOIN positions p ON ps.PlayerPositionFK = p.id
WHERE 
	p.id IN (1,4,7,9,8,10,22,23,29,30,31,32,36,37,46,73,78)
	AND LOWER(ps.week) = 'week 13'
ORDER BY ps.TotalPoints DESC;
