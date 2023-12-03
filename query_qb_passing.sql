SELECT 
    a.firstName || ' ' || a.lastName AS QuarterbackName,
	p.position,
    ps.Completions,
    ps.PassingAttempts,
    ps.CompletionPercentage,
    ps.PassingYards,
    ps.YardsPerPassAttempt,
    ps.PassingYardsPerGame,
    ps.LongestPass,
    ps.PassingTouchdowns,
    ps.Interceptions,
    ps.GamesPlayed,
	ps.TotalSacks,
	ps.SackYardsLost,
	ps.AdjustedQBR,
	ps.PasserRating
FROM 
    playerStatistics ps
JOIN athletes a ON ps.playerFK = a.id
JOIN positions p ON ps.PlayerPositionFK = p.id
WHERE 
    p.id IN (1,4,7,9,8,10,22,23,29,30,31,32,36,37,46,73,78)
    AND LOWER(ps.week) = 'week 13'
ORDER BY PassingYards DESC /* PassingYards is the default for ESPN*/