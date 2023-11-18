SELECT 
    a.firstName || ' ' || a.lastName AS QuarterbackName,
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
JOIN 
    athletes a ON ps.playerFK = a.id
WHERE 
    ps.PlayerPositionFK = 8 AND
    LOWER(ps.week) = 'week 11';