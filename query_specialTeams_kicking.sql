SELECT 
a.firstName || ' ' || a.lastName AS PlayerName,
p.position,
ps.FieldGoalMade,
ps.FieldGoalAttempts,
ps.FieldGoalPercentage,
ps.LongFieldGoalMade,
ps.FieldGoalsMade1_19,
ps.FieldGoalsMade20_29,
ps.FieldGoalsMade30_39,
ps.FieldGoalsMade40_49,
ps.FieldGoalsMade50Plus,
ps.ExtraPointsMade,
ps.ExtraPointAttempts,
ps.ExtraPointPercentage
FROM playerStatistics ps
JOIN athletes a ON ps.playerFK = a.id
JOIN positions p ON ps.PlayerPositionFK = p.id
WHERE 
	p.id IN (1,4,7,9,8,10,22,23,29,30,31,32,36,37,46,73,78)
	AND LOWER(ps.week) = 'week 13'
ORDER BY ps.FieldGoalMade DESC
