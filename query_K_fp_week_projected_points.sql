/*sql query to return results by K position and fp projected points by week*/
SELECT 
    ps.playerFK AS player_id,
    a.firstName,
    a.lastName,
    ps.week,
    ps.weekStart,
    ps.weekEnd,
    ps.GamesPlayed,
    fp.points AS fp_projected_points,
    ps.TotalPointsPerGame
	
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
    AND fp.points IS NOT NULL
    AND fp.fga IS NOT NULL
    AND fp.fg IS NOT NULL
    AND fp.xpt IS NOT NULL
    AND ps.TotalPointsPerGame IS NOT NULL
  
ORDER BY 
    fp_projected_points DESC;
