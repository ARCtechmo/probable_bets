/*sql query to return moneylines*/
SELECT DISTINCT
    dk.gameID,
    dk.gameDate,
    ht.teamShortName AS Team,
    dk.moneyline AS dk_moneyline,
    fd.moneyline AS fd_moneyline,
    mgm.moneyline AS mgm_moneyline,
    pb.moneyline AS pb_moneyline
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
