/*returns week-by-week stats for all QB*/
/*note: correctly reflects the weekly data*/
WITH cumulative_stats AS (
    SELECT
        ps1.weekStart,
        ps1.weekEnd,
        CAST(SUBSTR(ps1.week, 6) AS INTEGER) - 1 AS adjusted_week,
        a.firstName,
        a.lastName,
        pos.abbr AS position,
        ps1.PassingTouchdowns,
        ps1.PassingYards,
        ps1.PassingAttempts,
        ps1.Completions,
        ps1.Interceptions,
        ps1.RushingAttempts,
        ps1.RushingYards,
        ps1.RushingTouchdowns,
        ps1.Rushing1stDowns,
        ps1.RushingFumbles,
        ps1.RushingFumblesLost,
        ps1.playerFK
    FROM
        playerStatistics ps1
    JOIN 
        athletes a ON ps1.playerFK = a.id
    JOIN 
        positions pos ON ps1.PlayerPositionFK = pos.id
    WHERE
        pos.abbr = 'QB'
        AND strftime('%Y', ps1.weekStart) = '2023' /*input year*/
        AND ps1.week != 'Week 6'  /*PLACEHOLDER FOR 2023 DATA - REMOVE LATER*/
),
previous_stats AS (
    SELECT
        CAST(SUBSTR(ps1.week, 6) AS INTEGER) AS week,
        ps1.playerFK,
        SUM(ps1.PassingTouchdowns) AS PassingTouchdowns,
        SUM(ps1.PassingYards) AS PassingYards,
        SUM(ps1.PassingAttempts) AS PassingAttempts,
        SUM(ps1.Completions) AS Completions,
        SUM(ps1.Interceptions) AS Interceptions,
        SUM(ps1.RushingAttempts) AS RushingAttempts,
        SUM(ps1.RushingYards) AS RushingYards,
        SUM(ps1.RushingTouchdowns) AS RushingTouchdowns,
        SUM(ps1.Rushing1stDowns) AS Rushing1stDowns,
        SUM(ps1.RushingFumbles) AS RushingFumbles,
        SUM(ps1.RushingFumblesLost) AS RushingFumblesLost
    FROM
        playerStatistics ps1
    JOIN 
        athletes a ON ps1.playerFK = a.id
    JOIN 
        positions pos ON ps1.PlayerPositionFK = pos.id
    WHERE
        pos.abbr = 'QB'
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
    cs.PassingTouchdowns - COALESCE(ps.PassingTouchdowns, 0) AS PassingTouchdowns,
    cs.PassingYards - COALESCE(ps.PassingYards, 0) AS PassingYards,
    cs.PassingAttempts - COALESCE(ps.PassingAttempts, 0) AS PassingAttempts,
    cs.Completions - COALESCE(ps.Completions, 0) AS Completions,
    cs.Interceptions - COALESCE(ps.Interceptions, 0) AS Interceptions,
    cs.RushingAttempts - COALESCE(ps.RushingAttempts, 0) AS RushingAttempts,
    cs.RushingYards - COALESCE(ps.RushingYards, 0) AS RushingYards,
    cs.RushingTouchdowns - COALESCE(ps.RushingTouchdowns, 0) AS RushingTouchdowns,
    cs.Rushing1stDowns - COALESCE(ps.Rushing1stDowns, 0) AS Rushing1stDowns,
    cs.RushingFumbles - COALESCE(ps.RushingFumbles, 0) AS RushingFumbles,
    cs.RushingFumblesLost - COALESCE(ps.RushingFumblesLost, 0) AS RushingFumblesLost
FROM
    cumulative_stats cs
LEFT JOIN 
    previous_stats ps ON cs.adjusted_week = ps.week AND cs.playerFK = ps.playerFK
WHERE
    cs.PassingTouchdowns IS NOT NULL OR
    cs.PassingYards IS NOT NULL OR
    cs.PassingAttempts IS NOT NULL OR
    cs.Completions IS NOT NULL OR
    cs.Interceptions IS NOT NULL OR
    cs.RushingAttempts IS NOT NULL OR
    cs.RushingYards IS NOT NULL OR
    cs.RushingTouchdowns IS NOT NULL OR
    cs.Rushing1stDowns IS NOT NULL OR
    cs.RushingFumbles IS NOT NULL OR
    cs.RushingFumblesLost IS NOT NULL
ORDER BY 
    cs.adjusted_week,
	cs.PassingYards DESC;
