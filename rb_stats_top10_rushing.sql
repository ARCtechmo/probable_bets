SELECT 
    a.firstName || ' ' || a.lastName AS RunningBackName,
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
JOIN 
    athletes a ON ps.playerFK = a.id
WHERE 
    ps.PlayerPositionFK = 9 AND
    LOWER(ps.week) = 'week 13'
ORDER BY RushingYards DESC /* RushingYards is the default for ESPN*/