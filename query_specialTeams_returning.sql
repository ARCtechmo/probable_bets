SELECT 
a.firstName || ' ' || a.lastName AS PlayerName,
p.position,
ps.KickReturns,
ps.KickReturnYards,
ps.YardsPerKickReturn,
ps.LongKickReturn,
ps.KickReturnTouchdowns,
ps.PuntReturns,
ps.PuntReturnYards,
ps.YardsPerPuntReturn,
ps.LongPuntReturn,
ps.PuntReturnTouchdowns,
ps.PuntReturnFairCatches
FROM playerStatistics ps
JOIN athletes a ON ps.playerFK = a.id
JOIN positions p ON ps.PlayerPositionFK = p.id
WHERE 
	p.id IN (1,4,7,9,8,10,22,23,29,30,31,32,36,37,46,73,78)
	AND LOWER(ps.week) = 'week 13'
ORDER BY ps.KickReturnYards DESC
