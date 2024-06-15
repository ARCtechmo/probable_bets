/*sql query to return prop bets moneyline and odds*/
SELECT 
    pff.props_last_updated_at AS date,
    pff.player_id AS player,
    a.firstName AS player_first_name,
    a.lastName AS player_last_name,
    pff.position_id AS position,
    pos.position AS position_name,
    pff.team_id AS team,
    t.teamShortName AS team_name,
    pff.prop_type,
    pff.projection,
    pff.line,
    pff.over,
    ROUND(
        CASE 
            WHEN pff.over < 0 THEN (-1 * pff.over) / ((-1 * pff.over) + 100.0)
            ELSE 100.0 / (pff.over + 100.0)
        END, 
        3
    ) AS pff_over_odds,
    pff.under,
    ROUND(
        CASE 
            WHEN pff.under < 0 THEN (-1 * pff.under) / ((-1 * pff.under) + 100.0)
            ELSE 100.0 / (pff.under + 100.0)
        END, 
        3
    ) AS pff_under_odds
FROM 
    pro_football_focus pff
JOIN 
    athletes a ON pff.player_id = a.id
JOIN 
    positions pos ON pff.position_id = pos.id
JOIN 
    teams t ON pff.team_id = t.id;
