/*sql query to return predicted game scores*/
SELECT 
    dk.gameID,
    dk.gameDate,
    ht.teamShortName AS homeTeam,
    at.teamShortName AS awayTeam,
    dk.predictedHomeTeamScore AS dk_HomeScore,
    fd.predictedHomeTeamScore AS fd_HomeScore,
    mgm.predictedHomeTeamScore AS mgm_HomeScore,
    pb.predictedHomeTeamScore AS pb_HomeScore,
    dk.predictedOpponentTeamScore AS dk_AwayScore,  
    fd.predictedOpponentTeamScore AS fd_AwayScore, 
    mgm.predictedOpponentTeamScore AS mgm_AwayScore,
    pb.predictedOpponentTeamScore AS pb_AwayScore
FROM 
    draft_kings_lines dk
JOIN 
    fanduel_lines fd ON dk.gameID = fd.gameID AND dk.gameDate = fd.gameDate
JOIN 
    mgm_lines mgm ON dk.gameID = mgm.gameID AND dk.gameDate = mgm.gameDate
JOIN 
    pointsbet_lines pb ON dk.gameID = pb.gameID AND dk.gameDate = pb.gameDate
JOIN 
    teams ht ON dk.homeTeam = ht.id
JOIN 
    teams at ON dk.awayTeam = at.id
GROUP BY 
    dk.gameID
ORDER BY 
    dk.gameID, homeTeam;
