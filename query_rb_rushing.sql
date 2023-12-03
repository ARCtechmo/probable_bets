SELECT 
    a.firstName || ' ' || a.lastName AS RunningBackName,
	p.position,
    ps.RushingAttempts,
	ps.RushingYards,
	ps.YardsPerRushAttempt,
	ps.LongRushing,
	ps.Yards20PlusRushingPlays,
	ps.RushingTouchdowns,
	ps.RushingYardsPerGame,
	ps.RushingFumbles,
	ps.RushingFumblesLost,
	ps.Rushing1stDowns
FROM 
    playerStatistics ps
JOIN athletes a ON ps.playerFK = a.id
JOIN positions p ON ps.PlayerPositionFK = p.id
WHERE 
    p.id IN (1,4,7,9,8,10,22,23,29,30,31,32,36,37,46,73,78)
    AND LOWER(ps.week) = 'week 13'
ORDER BY RushingYards DESC /* RushingYards is the default for ESPN*/