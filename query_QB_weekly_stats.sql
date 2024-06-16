/*sql query returns QB stats by week */
SELECT
    ps.weekStart,
    ps.weekEnd,
    ps.week,
    a.firstName,
    a.lastName,
    pos.abbr AS position,
    ps.PassingTouchdowns AS passing_touchdowns,   
    ps.PassingYards AS passing_yards,
	ps.Completions,
    ps.PassingAttempts AS passing_attempts,
	ps.Interceptions AS interceptions,
	ps.TotalQBR
FROM
    playerStatistics ps
JOIN 
    athletes a ON ps.playerFK = a.id
JOIN 
    positions pos ON ps.PlayerPositionFK = pos.id
JOIN 
    athleteStatus ast ON ps.playerStatusFK = ast.id
WHERE
    pos.abbr = 'QB'
    AND strftime('%Y', ps.weekStart) = '2023'
    AND ps.week IN ('Week 10')
    AND NOT (
        ps.PassingTouchdowns IS NULL AND
        ps.PassingYards IS NULL AND
        ps.PassingAttempts IS NULL AND
        ps.Completions IS NULL AND
        ps.PassingTouchdowns IS NULL
    )
ORDER BY
    ps.PassingTouchdowns DESC;
