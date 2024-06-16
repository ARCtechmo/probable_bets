/*sql query returns airyards*/
SELECT
    ps.weekStart,
    ps.weekEnd,
    ps.week,
    a.firstName,
    a.lastName,
    pos.abbr AS position,
	ps.ReceivingYards AS receiving_yards,
    ps.Receptions AS receptions,
    ps.ReceivingTargets AS receiving_targets,
    ps.ReceivingYardsAfterCatch AS receiving_yards_after_catch,
    (ps.ReceivingYards - ps.ReceivingYardsAfterCatch) AS air_yards
FROM
    playerStatistics ps
JOIN 
    athletes a ON ps.playerFK = a.id
JOIN 
    positions pos ON ps.PlayerPositionFK = pos.id
WHERE
    pos.abbr = 'WR'
    AND strftime('%Y', ps.weekStart) = '2023'
    AND NOT (
        ps.Receptions IS NULL AND
        ps.ReceivingTargets IS NULL AND
        ps.ReceivingYards IS NULL AND
        ps.ReceivingYardsAfterCatch IS NULL
    )
ORDER BY
    CAST(SUBSTR(ps.week, 6) AS INTEGER) DESC;
