SELECT 
a.firstName || ' ' || a.lastName AS ReceiverName,
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
JOIN 
    athletes a ON ps.playerFK = a.id
WHERE 
    ps.PlayerPositionFK = 1 AND
    LOWER(ps.week) = 'week 13'
ORDER BY ReceivingYards DESC