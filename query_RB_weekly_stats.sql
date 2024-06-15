/*sql query returns RB stats by week */
SELECT
    ps.weekStart,
    ps.weekEnd,
    ps.week,
    a.firstName,
    a.lastName,
    pos.abbr AS position,
    ps.RushingAttempts AS rushing_attempts,
    ps.RushingYards AS rushing_yards,
    ps.RushingTouchdowns AS rushing_touchdowns,
    ps.Rushing1stDowns AS rushing_first_downs,
    ps.RushingFumbles AS rushing_fumbles,
    ps.RushingFumblesLost AS rushing_fumbles_lost
FROM
    playerStatistics ps
JOIN 
    athletes a ON ps.playerFK = a.id
JOIN 
    positions pos ON ps.PlayerPositionFK = pos.id
JOIN 
    athleteStatus ast ON ps.playerStatusFK = ast.id
WHERE
    pos.abbr = 'RB'
    AND strftime('%Y', ps.weekStart) = '2023'
    AND ps.week IN ('Week 10')
    AND NOT (
        ps.RushingAttempts IS NULL AND
        ps.RushingYards IS NULL AND
        ps.RushingTouchdowns IS NULL AND
        ps.Rushing1stDowns IS NULL AND
        ps.RushingFumbles IS NULL AND
        ps.RushingFumblesLost IS NULL
    )
ORDER BY
    ps.RushingTouchdowns DESC;
