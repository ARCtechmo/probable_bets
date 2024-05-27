/*sql query to return results by K position and fp betting line by week*/
SELECT 
    ps.playerFK AS player_id,
    a.firstName,
    a.lastName,
    ps.week,
    ps.weekStart,
    ps.weekEnd,
    ps.GamesPlayed,
    fp.fga AS fp_projected_Field_Goals_attempts,
    ROUND((ps.FieldGoalAttempts * 1.0 / ps.GamesPlayed), 2) AS Field_Goals_Attempts_per_game,
    fp.fg AS fp_projected_Field_Goals,
    ROUND((ps.FieldGoalMade * 1.0 / ps.GamesPlayed), 2) AS Field_Goals_Made_per_game,
    fp.xpt AS fp_projected_Extra_points,
    ROUND((ps.ExtraPointsMade * 1.0 / ps.GamesPlayed), 2) AS Extra_Points_per_game
FROM 
    playerStatistics ps
JOIN 
    fantasy_pros_K fp 
ON 
    ps.playerFK = fp.player_id 
    AND ps.week = 'Week ' || fp.week
    AND strftime('%Y', ps.weekStart) = fp.season
JOIN 
    athletes a 
ON 
    ps.playerFK = a.id
WHERE 
    ps.PlayerPositionFK = 22 
    AND ps.week = 'Week 10'
    AND strftime('%Y', ps.weekStart) = '2023'
    AND fp.week = 10
    AND fp.fga IS NOT NULL
    AND fp.fg IS NOT NULL
    AND fp.xpt IS NOT NULL
    AND (
        ps.FieldGoalAttempts IS NOT NULL
        OR ps.FieldGoalMade IS NOT NULL
        OR ps.ExtraPointsMade IS NOT NULL
    )
    AND (
        ROUND((ps.FieldGoalAttempts * 1.0 / ps.GamesPlayed), 2) IS NOT NULL
        OR ROUND((ps.FieldGoalMade * 1.0 / ps.GamesPlayed), 2) IS NOT NULL
        OR ROUND((ps.ExtraPointsMade * 1.0 / ps.GamesPlayed), 2) IS NOT NULL
    )
ORDER BY 
    fp.fga DESC;
