/*sql query to return results by WR position and fp betting line by week*/
SELECT 
    ps.playerFK AS player_id,
    a.firstName,
    a.lastName,
    ps.week,
    ps.weekStart,
    ps.weekEnd,
    ps.GamesPlayed,
    fp.points AS fp_projected_points,
    fp.points_ppr,
	fp.rec_rec AS fp_projected_receptions,
	ROUND((ps.Receptions * 1.0 / ps.GamesPlayed), 2) AS receptions_per_game,
	fp.rec_yds AS fp_projected_rec_yards,
	ps.ReceivingYardsPerGame,	
	ps.YardsPerReception,
	fp.rec_tds AS fp_projected_rec_tds,
	ROUND((ps.ReceivingTouchdowns * 1.0 / ps.GamesPlayed), 2) AS receiving_tds_per_game,	
	ROUND((ps.ReceivingTargets * 1.0 / ps.GamesPlayed), 2) AS targets_per_game,	
	ROUND((ps.ReceivingYardsAfterCatch  * 1.0 / ps.GamesPlayed),2) AS rec_yds_after_catch_per_game,
	ROUND((ps.ReceivingFirstDowns  * 1.0 / ps.GamesPlayed),2) AS rec_1st_downs_per_game,
	ROUND((ps.Yards20PlusReceivingPlays  * 1.0 / ps.GamesPlayed),2) AS rec_yds_20Plus_per_game
  
FROM 
    playerStatistics ps
JOIN 
    fantasy_pros_WR fp 
ON 
    ps.playerFK = fp.player_id 
    AND ps.week LIKE 'Week ' || fp.week
    AND strftime('%Y', ps.weekStart) = fp.season
JOIN 
    athletes a 
ON 
    ps.playerFK = a.id
WHERE 
    ps.PlayerPositionFK = 1
    AND ps.week LIKE 'Week 10'
    AND strftime('%Y', ps.weekStart) = '2023'
    AND fp.week = 10
	AND fp.points IS NOT NULL
	AND fp.points_ppr IS NOT NULL
	AND fp.rec_rec IS NOT NULL
	AND fp.rec_tds IS NOT NULL
	AND fp.rec_yds IS NOT NULL
	AND ps.Receptions IS NOT NULL
	AND ps.YardsPerReception IS NOT NULL
	AND ps.ReceivingTargets IS NOT NULL
	AND ps.ReceivingYards IS NOT NULL 
	AND ps.ReceivingYardsPerGame IS NOT NULL
	AND ps. ReceivingYardsAfterCatch IS NOT NULL
	AND ps.ReceivingFirstDowns IS NOT NULL 

ORDER BY 
    fp_projected_points DESC;