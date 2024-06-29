/*sql query to return results by RB position and fp betting line by week*/
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
	fp.rush_att AS fp_projected_rush_attempts,
	ROUND((ps.RushingAttempts * 1.0 / ps.GamesPlayed), 2) AS rushing_attempts_per_game,	
	fp.rush_yds AS fp_projected_rushing_yards,
	ps.RushingYardsPerGame,
	fp.rush_tds AS fp_projected_rush_tds,
	ROUND((ps.RushingTouchdowns * 1.0 / ps.GamesPlayed), 2) AS rushing_tds_per_game,	
	ROUND((ps.Rushing1stDowns * 1.0 / ps.GamesPlayed), 2) AS rushing_1st_Downs_per_game,	
	fp.rec_rec AS fp_projected_receptions,
	ROUND((ps.Receptions * 1.0 / ps.GamesPlayed), 2) AS receptions_per_game,
	fp.rec_yds AS fp_projected_rec_yards,
	ps.ReceivingYardsPerGame,
	fp.rec_tds AS fp_projected_rec_tds,
	ROUND((ps.ReceivingTouchdowns * 1.0 / ps.GamesPlayed), 2) AS receiving_tds_per_game
	
FROM 
    playerStatistics ps
JOIN 
    fantasy_pros_RB fp 
ON 
    ps.playerFK = fp.player_id 
    AND ps.week LIKE 'Week ' || fp.week
    AND strftime('%Y', ps.weekStart) = fp.season
JOIN 
    athletes a 
ON 
    ps.playerFK = a.id
WHERE 
    ps.PlayerPositionFK = 9
    AND ps.week LIKE 'Week 10'  /*manually change the week*/
    AND strftime('%Y', ps.weekStart) = '2023' /*manually change the year*/
    AND fp.week = 10  /*manually change the week*/
	AND fp.points IS NOT NULL
	AND fp.points_ppr IS NOT NULL
	AND fp.rush_att IS NOT NULL
	AND fp.rush_yds IS NOT NULL
	AND fp.rush_tds IS NOT NULL
	AND ps.RushingAttempts IS NOT NULL 
	AND ps.RushingTouchdowns IS NOT NULL
	AND ps.RushingYards IS NOT NULL

ORDER BY 
    fp_projected_points DESC;