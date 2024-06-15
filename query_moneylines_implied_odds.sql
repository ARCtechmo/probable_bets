/*sql query to return moneylines and implied odds*/
SELECT DISTINCT
    dk.gameID,
    dk.gameDate,
    ht.teamShortName AS Team,
    dk.moneyline AS dk_moneyline,
    ROUND(
        CASE 
            WHEN dk.moneyline < 0 THEN (-1 * dk.moneyline) / ((-1 * dk.moneyline) + 100.0)
            ELSE 100.0 / (dk.moneyline + 100.0)
        END, 
        3
    ) AS dk_odds,
    fd.moneyline AS fd_moneyline,
    ROUND(
        CASE 
            WHEN fd.moneyline < 0 THEN (-1 * fd.moneyline) / ((-1 * fd.moneyline) + 100.0)
            ELSE 100.0 / (fd.moneyline + 100.0)
        END, 
        3
    ) AS fd_odds,
    mgm.moneyline AS mgm_moneyline,
    ROUND(
        CASE 
            WHEN mgm.moneyline < 0 THEN (-1 * mgm.moneyline) / ((-1 * mgm.moneyline) + 100.0)
            ELSE 100.0 / (mgm.moneyline + 100.0)
        END, 
        3
    ) AS mgm_odds,
    pb.moneyline AS pb_moneyline,
    ROUND(
        CASE 
            WHEN pb.moneyline < 0 THEN (-1 * pb.moneyline) / ((-1 * pb.moneyline) + 100.0)
            ELSE 100.0 / (pb.moneyline + 100.0)
        END, 
        3
    ) AS pb_odds
FROM 
    draft_kings_lines dk
JOIN 
    fanduel_lines fd ON dk.gameID = fd.gameID AND dk.gameDate = fd.gameDate AND dk.homeTeam = fd.homeTeam AND dk.awayTeam = fd.awayTeam
JOIN 
    mgm_lines mgm ON dk.gameID = mgm.gameID AND dk.gameDate = mgm.gameDate AND dk.homeTeam = mgm.homeTeam AND dk.awayTeam = mgm.awayTeam
JOIN 
    pointsbet_lines pb ON dk.gameID = pb.gameID AND dk.gameDate = pb.gameDate AND dk.homeTeam = pb.homeTeam AND dk.awayTeam = pb.awayTeam
JOIN 
    teams ht ON dk.homeTeam = ht.id
JOIN 
    teams at ON dk.awayTeam = at.id
ORDER BY 
    dk.gameID, Team;
