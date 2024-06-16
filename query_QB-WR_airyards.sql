/*query reuturns QB-WR stats and airyards*/
WITH wr_stats AS (
    SELECT
        ps.weekStart,
        ps.weekEnd,
        ps.week,
        ps.playerTeamFK,
        ps.playerFK,
        a.firstName AS WR_firstName,
        a.lastName AS WR_lastName,
        pos.abbr AS WR_position,
        t.teamName AS team_name,
        SUM(ps.ReceivingYards) AS WR_receiving_yards,
        SUM(ps.Receptions) AS WR_receptions,
        SUM(ps.ReceivingTargets) AS WR_receiving_targets,
        SUM(ps.ReceivingYards - ps.ReceivingYardsAfterCatch) AS WR_air_yards
    FROM
        playerStatistics ps
    JOIN 
        athletes a ON ps.playerFK = a.id
    JOIN 
        positions pos ON ps.PlayerPositionFK = pos.id
    JOIN 
        teams t ON ps.playerTeamFK = t.id
    WHERE
        pos.abbr = 'WR'
        AND strftime('%Y', ps.weekStart) = '2023'
        AND ps.ReceivingYards IS NOT NULL
    GROUP BY
        ps.week, ps.playerTeamFK, ps.playerFK
),
qb_stats AS (
    SELECT
        ps.week,
        ps.playerTeamFK,
        SUM(ps.PassingYards) AS QB_passing_yards,
        SUM(ps.Completions) AS QB_completions,
        SUM(ps.PassingAttempts) AS QB_passing_attempts
    FROM
        playerStatistics ps
    JOIN 
        positions qb_pos ON ps.PlayerPositionFK = qb_pos.id
    WHERE
        qb_pos.abbr = 'QB'
        AND strftime('%Y', ps.weekStart) = '2023'
        AND ps.PassingYards IS NOT NULL
    GROUP BY
        ps.week, ps.playerTeamFK
)
SELECT
    wr_stats.weekStart,
    wr_stats.weekEnd,
    wr_stats.week,
    wr_stats.WR_firstName,
    wr_stats.WR_lastName,
    wr_stats.WR_position,
    wr_stats.team_name,
    qb_stats.QB_passing_yards,
    qb_stats.QB_completions,
    qb_stats.QB_passing_attempts,
    wr_stats.WR_receiving_yards,
    wr_stats.WR_receptions,
    wr_stats.WR_receiving_targets,
    ROUND((wr_stats.WR_receiving_yards * 1.0 / qb_stats.QB_passing_yards), 3) AS WR_pct_of_QB_passing_yards,
    ROUND((wr_stats.WR_receptions * 1.0 / qb_stats.QB_completions), 3) AS WR_pct_of_QB_completions,
    ROUND((wr_stats.WR_receiving_targets * 1.0 / qb_stats.QB_passing_attempts), 3) AS WR_pct_of_QB_passing_attempts,
    wr_stats.WR_air_yards
FROM
    wr_stats
JOIN 
    qb_stats ON wr_stats.week = qb_stats.week AND wr_stats.playerTeamFK = qb_stats.playerTeamFK
WHERE
    qb_stats.QB_passing_yards > 100
    AND ROUND((wr_stats.WR_receiving_yards * 1.0 / qb_stats.QB_passing_yards), 3) >= 0
    AND ROUND((wr_stats.WR_receptions * 1.0 / qb_stats.QB_completions), 3) >= 0
    AND ROUND((wr_stats.WR_receiving_targets * 1.0 / qb_stats.QB_passing_attempts), 3) >= 0
ORDER BY
    CAST(SUBSTR(wr_stats.week, 6) AS INTEGER) DESC;
