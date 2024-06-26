/*sql query returns cumulative TE / WR stats by week*/
SELECT
    ps.weekStart,
    ps.weekEnd,
    ps.week,
    a.firstName,
    a.lastName,
    pos.abbr AS position,
    ps.Receptions AS receptions,
	ps.ReceivingTargets AS receiving_targets,
    ps.ReceivingYards AS receiving_yards,
    ps.ReceivingTouchdowns AS receiving_touchdowns,
    ps.ReceivingYardsAfterCatch AS receiving_yards_after_catch,
    ps.ReceivingFirstDowns AS receiving_first_downs,
    ps.Yards20PlusReceivingPlays AS twenty_plus_yards_receiving_plays
FROM
    playerStatistics ps
JOIN 
    athletes a ON ps.playerFK = a.id
JOIN 
    positions pos ON ps.PlayerPositionFK = pos.id
JOIN 
    athleteStatus ast ON ps.playerStatusFK = ast.id
WHERE
    pos.abbr IN ('WR', 'TE')
    AND strftime('%Y', ps.weekStart) = '2023' /*input the year*/
    AND ps.week IN ('Week 10')  /*input the week*/
    AND NOT (
        ps.Receptions IS NULL AND
        ps.ReceivingYards IS NULL AND
        ps.ReceivingTouchdowns IS NULL AND
        ps.ReceivingTargets IS NULL AND
        ps.ReceivingYardsAfterCatch IS NULL AND
        ps.ReceivingFirstDowns IS NULL AND
        ps.Yards20PlusReceivingPlays IS NULL
    )
ORDER BY
    ps.ReceivingTouchdowns DESC;
