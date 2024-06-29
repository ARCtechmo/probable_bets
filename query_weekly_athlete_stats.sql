/*query returns weekly athlete stats */
SELECT
    ps.weekStart,
    ps.weekEnd,
    ps.week,
    a.firstName,
    a.lastName,
    pos.abbr AS position,
    ps.PassingTouchdowns AS passing_touchdowns,
    ps.TotalQBR,
    ps.PassingYards AS passing_yards,
    ps.PassingAttempts AS passing_attempts,
    ps.Completions AS completions,
    ps.Interceptions AS interceptions,
    ps.RushingAttempts AS rushing_attempts,
    ps.RushingYards AS rushing_yards,
    ps.RushingTouchdowns AS rushing_touchdowns,
    ps.Rushing1stDowns AS rushing_first_downs,
    ps.RushingFumbles AS rushing_fumbles,
    ps.RushingFumblesLost AS rushing_fumbles_lost,
    ps.Receptions AS receptions,
    ps.ReceivingYards AS receiving_yards,
    ps.ReceivingTouchdowns AS receiving_touchdowns,
    ps.ReceivingTargets AS receiving_targets,
    ps.ReceivingYardsAfterCatch AS receiving_yards_after_catch,
    ps.ReceivingFirstDowns AS receiving_first_downs,
    ps.Yards20PlusReceivingPlays AS twenty_plus_yards_receiving_plays,
    ps.FieldGoalAttempts AS field_goal_attempts,
    ps.FieldGoalMade AS field_goals_made,
    ps.ExtraPointsMade AS extra_points_made
FROM
    playerStatistics ps
JOIN 
    athletes a ON ps.playerFK = a.id
JOIN 
    positions pos ON ps.PlayerPositionFK = pos.id
WHERE
    LOWER(a.firstName) = LOWER('patrick') /*manually change last name*/
    AND LOWER(a.lastName) = LOWER('mahomes') /*manually change first name*/
    AND strftime('%Y', ps.weekStart) = '2023' /*manually change year*/
    AND NOT (
        ps.PassingTouchdowns IS NULL AND
        ps.TotalQBR IS NULL AND
        ps.PassingYards IS NULL AND
        ps.PassingAttempts IS NULL AND
        ps.Completions IS NULL AND
        ps.Interceptions IS NULL AND
        ps.RushingAttempts IS NULL AND
        ps.RushingYards IS NULL AND
        ps.RushingTouchdowns IS NULL AND
        ps.Rushing1stDowns IS NULL AND
        ps.RushingFumbles IS NULL AND
        ps.RushingFumblesLost IS NULL AND
        ps.Receptions IS NULL AND
        ps.ReceivingYards IS NULL AND
        ps.ReceivingTouchdowns IS NULL AND
        ps.ReceivingTargets IS NULL AND
        ps.ReceivingYardsAfterCatch IS NULL AND
        ps.ReceivingFirstDowns IS NULL AND
        ps.Yards20PlusReceivingPlays IS NULL AND
        ps.FieldGoalAttempts IS NULL AND
        ps.FieldGoalMade IS NULL AND
        ps.ExtraPointsMade IS NULL
    )
ORDER BY
    CAST(SUBSTR(ps.week, 6) AS INTEGER);
