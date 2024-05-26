/*sql query to return individual athlete stats and fp betting line*/
SELECT 
    ps.playerFK AS player_id,
    ps.week,
    ps.weekStart,
    ps.weekEnd,
    ps.GamesPlayed,
    fp.points AS fp_projected_points,
    fp.pass_tds AS fp_projected_tds,
    ROUND((ps.PassingTouchdowns * 1.0 / ps.GamesPlayed), 2) AS TD_per_game,
    fp.pass_yds AS fp_projected_pass_yards,
    ps.PassingYardsPerGame,    
    fp.pass_att AS fp_projected_pass_attempts,    
    ROUND((ps.PassingAttempts * 1.0 / ps.GamesPlayed),2) AS pass_attempts_per_game,
    fp.pass_cmp AS fp_projected_completions,
    ROUND((ps.Completions * 1.0 / ps.GamesPlayed),2) AS pass_completions_per_game,
    fp.pass_ints AS fp_projected_interceptions,
    ROUND((ps.Interceptions * 1.0 / ps.GamesPlayed),2) AS int_per_game
FROM 
    playerStatistics ps
JOIN 
    fantasy_pros_QB fp 
ON 
    ps.playerFK = fp.player_id 
    AND ps.week LIKE 'Week ' || fp.week
    AND strftime('%Y', ps.weekStart) = fp.season
WHERE 
    ps.playerFK = 12483
    AND strftime('%Y', ps.weekStart) = '2023'
    AND ps.PassingTouchdowns IS NOT NULL
    AND fp.pass_tds IS NOT NULL
    AND ps.PassingYards IS NOT NULL
    AND fp.pass_yds IS NOT NULL
    AND ps.PassingAttempts IS NOT NULL
    AND fp.pass_att IS NOT NULL
    AND ps.Completions IS NOT NULL
    AND fp.pass_cmp IS NOT NULL
    AND ps.Interceptions IS NOT NULL
    AND fp.pass_ints IS NOT NULL;