/*returns week-by-week stats for all RB*/
/*note: correctly reflects the weekly data*/
WITH cumulative_stats AS (
    SELECT
        ps1.weekStart,
        ps1.weekEnd,
        CAST(SUBSTR(ps1.week, 6) AS INTEGER) - 1 AS adjusted_week,
        a.firstName,
        a.lastName,
        pos.abbr AS position,
        ps1.RushingAttempts,
        ps1.RushingYards,
        ps1.RushingTouchdowns,
        ps1.Rushing1stDowns,
        ps1.RushingFumbles,
        ps1.RushingFumblesLost,
        ps1.Receptions,
        ps1.ReceivingYards,
        ps1.ReceivingTouchdowns,
        ps1.ReceivingTargets,
        ps1.ReceivingYardsAfterCatch,
        ps1.ReceivingFirstDowns,
        ps1.Yards20PlusReceivingPlays,
        ps1.playerFK
    FROM
        playerStatistics ps1
    JOIN 
        athletes a ON ps1.playerFK = a.id
    JOIN 
        positions pos ON ps1.PlayerPositionFK = pos.id
    WHERE
        pos.abbr = 'RB'
        AND strftime('%Y', ps1.weekStart) = '2023' /*input year*/
        AND ps1.week != 'Week 6'  /*PLACEHOLDER FOR 2023 DATA - REMOVE LATER*/
),
previous_stats AS (
    SELECT
        CAST(SUBSTR(ps1.week, 6) AS INTEGER) AS week,
        ps1.playerFK,
        SUM(ps1.RushingAttempts) AS RushingAttempts,
        SUM(ps1.RushingYards) AS RushingYards,
        SUM(ps1.RushingTouchdowns) AS RushingTouchdowns,
        SUM(ps1.Rushing1stDowns) AS Rushing1stDowns,
        SUM(ps1.RushingFumbles) AS RushingFumbles,
        SUM(ps1.RushingFumblesLost) AS RushingFumblesLost,
        SUM(ps1.Receptions) AS Receptions,
        SUM(ps1.ReceivingYards) AS ReceivingYards,
        SUM(ps1.ReceivingTouchdowns) AS ReceivingTouchdowns,
        SUM(ps1.ReceivingTargets) AS ReceivingTargets,
        SUM(ps1.ReceivingYardsAfterCatch) AS ReceivingYardsAfterCatch,
        SUM(ps1.ReceivingFirstDowns) AS ReceivingFirstDowns,
        SUM(ps1.Yards20PlusReceivingPlays) AS Yards20PlusReceivingPlays
    FROM
        playerStatistics ps1
    JOIN 
        athletes a ON ps1.playerFK = a.id
    JOIN 
        positions pos ON ps1.PlayerPositionFK = pos.id
    WHERE
        pos.abbr = 'RB'
        AND strftime('%Y', ps1.weekStart) = '2023' /*input year*/
        AND ps1.week != 'Week 6' /*PLACEHOLDER FOR 2023 DATA - REMOVE LATER*/
    GROUP BY
        week, ps1.playerFK
)
SELECT
    cs.weekStart,
    cs.weekEnd,
    'Week ' || cs.adjusted_week AS week,
    cs.firstName,
    cs.lastName,
    cs.position,
    cs.RushingAttempts - COALESCE(ps.RushingAttempts, 0) AS RushingAttempts,
    cs.RushingYards - COALESCE(ps.RushingYards, 0) AS RushingYards,
    cs.RushingTouchdowns - COALESCE(ps.RushingTouchdowns, 0) AS RushingTouchdowns,
    cs.Rushing1stDowns - COALESCE(ps.Rushing1stDowns, 0) AS Rushing1stDowns,
    cs.RushingFumbles - COALESCE(ps.RushingFumbles, 0) AS RushingFumbles,
    cs.RushingFumblesLost - COALESCE(ps.RushingFumblesLost, 0) AS RushingFumblesLost,
    cs.Receptions - COALESCE(ps.Receptions, 0) AS Receptions,
    cs.ReceivingYards - COALESCE(ps.ReceivingYards, 0) AS ReceivingYards,
    cs.ReceivingTouchdowns - COALESCE(ps.ReceivingTouchdowns, 0) AS ReceivingTouchdowns,
    cs.ReceivingTargets - COALESCE(ps.ReceivingTargets, 0) AS ReceivingTargets,
    cs.ReceivingYardsAfterCatch - COALESCE(ps.ReceivingYardsAfterCatch, 0) AS ReceivingYardsAfterCatch,
    cs.ReceivingFirstDowns - COALESCE(ps.ReceivingFirstDowns, 0) AS ReceivingFirstDowns,
    cs.Yards20PlusReceivingPlays - COALESCE(ps.Yards20PlusReceivingPlays, 0) AS Yards20PlusReceivingPlays
FROM
    cumulative_stats cs
LEFT JOIN 
    previous_stats ps ON cs.adjusted_week = ps.week AND cs.playerFK = ps.playerFK
WHERE
    cs.RushingAttempts IS NOT NULL OR
    cs.RushingYards IS NOT NULL OR
    cs.RushingTouchdowns IS NOT NULL OR
    cs.Rushing1stDowns IS NOT NULL OR
    cs.RushingFumbles IS NOT NULL OR
    cs.RushingFumblesLost IS NOT NULL OR
    cs.Receptions IS NOT NULL OR
    cs.ReceivingYards IS NOT NULL OR
    cs.ReceivingTouchdowns IS NOT NULL OR
    cs.ReceivingTargets IS NOT NULL OR
    cs.ReceivingYardsAfterCatch IS NOT NULL OR
    cs.ReceivingFirstDowns IS NOT NULL OR
    cs.Yards20PlusReceivingPlays IS NOT NULL
ORDER BY 
    cs.adjusted_week,
    cs.RushingYards DESC;
