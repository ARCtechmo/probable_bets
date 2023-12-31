SELECT 
	ps.week,
    a.firstName || ' ' || a.lastName AS QuarterbackName,
	ps.GamesPlayed,
    ps.Completions,
    ps.PassingAttempts,
    ps.CompletionPercentage,
    ps.PassingYards,
    ps.YardsPerPassAttempt,
    ps.PassingYardsPerGame,
    ps.LongestPass,
    ps.PassingTouchdowns,
    ps.Interceptions,
    ps.TotalSacks,
    ps.SackYardsLost,
    ps.AdjustedQBR,
    ps.PasserRating
FROM 
    playerStatistics ps
JOIN 
    athletes a ON ps.playerFK = a.id
WHERE 
    LOWER(a.firstName) = 'jalen' AND 
    LOWER(a.lastName) = 'hurts'
	
    
