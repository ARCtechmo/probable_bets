# parse the rotowire json files #
from database import(
    create_connection
)
import json
import os
import glob
from datetime import datetime

def read_json(file):
    with open(file, 'r') as f:
        return json.load(f)

def process_json(data):

    # Initialize arrays to 
    # arrays will hold data for each betting site and game/team info
    game_info = []
    draftkings = []
    fanduel = []
    mgm = []
    pointsbet = []

    # Extract game and team information 
    # Organize betting information for each site
    for game in data:
        # Game and team information
        game_team_info = [
            game['gameID'],
            game['gameDate'],
            game['gameDay'],
            game['gameDateTime'],
            game['homeAway'],
            game['abbr'],
            game['oppAbbr']
        ]
        game_info.append(game_team_info)

        # DraftKings betting information
        draftkings_info = game_team_info + [
            game['draftkings_moneyline'],
            game['draftkings_moneylineWinPct'],
            game['draftkings_spread'],
            game['draftkings_spreadML'],
            game['draftkings_spreadWinPct'],
            game['draftkings_ou'],
            game['draftkings_ouML'],
            game['draftkings_ouWinPct'],
            game['draftkings_score'],
            game['draftkings_oppScore'],
        ]
        draftkings.append(draftkings_info)

        # FanDuel betting information
        fanduel_info = game_team_info + [

            game['fanduel_moneyline'],
            game['fanduel_moneylineWinPct'],
            game['fanduel_spread'],
            game['fanduel_spreadML'],
            game['fanduel_spreadWinPct'],
            game['fanduel_ou'],
            game['fanduel_ouML'],
            game['fanduel_ouWinPct'],
            game['fanduel_score'],
            game['fanduel_oppScore'],
        ]
        fanduel.append(fanduel_info)

        # MGM betting information
        mgm_info = game_team_info + [

            game['mgm_moneyline'],
            game['mgm_moneylineWinPct'],
            game['mgm_spread'],
            game['mgm_spreadML'],
            game['mgm_spreadWinPct'],
            game['mgm_ou'],
            game['mgm_ouML'],
            game['mgm_ouWinPct'],
            game['mgm_score'],
            game['mgm_oppScore'],
        ]
        mgm.append(mgm_info)

        # PointsBet betting information
        pointsbet_info = game_team_info + [

            game['pointsbet_moneyline'],
            game['pointsbet_moneylineWinPct'],
            game['pointsbet_spread'],
            game['pointsbet_spreadML'],
            game['pointsbet_spreadWinPct'],
            game['pointsbet_ou'],
            game['pointsbet_ouML'],
            game['pointsbet_ouWinPct'],
            game['pointsbet_score'],
            game['pointsbet_oppScore'],
        ]
        pointsbet.append(pointsbet_info)

    return game_info, draftkings, fanduel, mgm, pointsbet

## task standardize the abbr
# Helper function to get team ID based on team short name
# def get_team_id(conn, team_short_name):

#     # JAX vs JAC, WSH vs WAS, CLE vs CLV
#     if team_short_name == 'CLV':
#         team_short_name = 'CLE'
    
#     elif team_short_name == 'JAC':
#         team_short_name = 'JAX'
    
#     elif team_short_name =='WAS':
#         team_short_name ='WSH'

#     cur = conn.cursor()
#     cur.execute("SELECT id FROM teams WHERE teamShortName = ?", (team_short_name,))
#     result = cur.fetchone()
#     return result[0] if result else None

def main():

    # Create a database connection
    conn = create_connection()

    # Pattern to match files for the current and previous year
    file_pattern = f'rotowire_odds_lines_week_*.json'

    # List all matching files
    files = glob.glob(file_pattern) 
    for file in files:

        # Check if the file exists in the current directory
        if not os.path.exists(file):
            print(f"{file} not in the directory.")
            continue  # Skip the rest of the loop for this file

        # file = 'fantasy_pros_QB_projections_2023_STD.json'
        data = read_json(file)

        # Assuming process_json is defined
        draftkings_data = process_json(data)  
        for line in draftkings_data[:1]:
            print(line)

    conn.close()
if __name__ == "__main__":
    main()