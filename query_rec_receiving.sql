SELECT 
a.firstName || ' ' || a.lastName AS ReceiverName,
p.position,
ps.Receptions,
ps.ReceivingTargets,
ps.ReceivingYards,
ps.YardsPerReception,
ps.ReceivingTouchdowns,
ps.LongReception,
ps.Yards20PlusReceivingPlays,
ps.ReceivingYardsPerGame,
ps.ReceivingFumbles,
ps.ReceivingFumblesLost,
ps.ReceivingYardsAfterCatch,
ps.ReceivingFirstDowns
FROM playerStatistics ps
JOIN athletes a ON ps.playerFK = a.id
JOIN positions p ON ps.PlayerPositionFK = p.id
WHERE 
    p.id IN (1,4,7,9,8,10,22,23,29,30,31,32,36,37,46,73,78)
	AND LOWER(ps.week) = 'week 13'
ORDER BY ReceivingYards DESC