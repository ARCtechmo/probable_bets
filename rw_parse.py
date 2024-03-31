## task: complete testing for all json files input / output 
# (look in the file_dump)

# parse the rotowire json files #
from database import(
    create_connection,
    insert_or_update_draft_kings,
    insert_or_update_fanduels,
    insert_or_update_mgm,
    insert_or_update_pointsbet
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
            int(game['gameID']),
            game['gameDate'],
            game['abbr'],
            game['oppAbbr']
        ]
        game_info.append(game_team_info)

        # DraftKings betting information
        draftkings_info = game_team_info + [
            float(game['draftkings_moneyline']),
            float(game['draftkings_moneylineWinPct']),
            float(game['draftkings_spread']),
            float(game['draftkings_spreadML']),
            float(game['draftkings_spreadWinPct']),
            float(game['draftkings_ou']),
            float(game['draftkings_ouML']),
            float(game['draftkings_ouWinPct']),
            float(game['draftkings_score']),
            float(game['draftkings_oppScore']),
        ]
        draftkings.append(draftkings_info)

        # FanDuel betting information
        fanduel_info = game_team_info + [

            float(game['fanduel_moneyline']),
            float(game['fanduel_moneylineWinPct']),
            float(game['fanduel_spread']),
            float(game['fanduel_spreadML']),
            float(game['fanduel_spreadWinPct']),
            float(game['fanduel_ou']),
            float(game['fanduel_ouML']),
            float(game['fanduel_ouWinPct']),
            float(game['fanduel_score']),
            float(game['fanduel_oppScore']),
        ]
        fanduel.append(fanduel_info)

        # MGM betting information
        mgm_info = game_team_info + [

            float(game['mgm_moneyline']),
            float(game['mgm_moneylineWinPct']),
            float(game['mgm_spread']),
            float(game['mgm_spreadML']),
            float(game['mgm_spreadWinPct']),
            float(game['mgm_ou']),
            float(game['mgm_ouML']),
            float(game['mgm_ouWinPct']),
            float(game['mgm_score']),
            float(game['mgm_oppScore']),
        ]
        mgm.append(mgm_info)

        # PointsBet betting information
        pointsbet_info = game_team_info + [

            float(game['pointsbet_moneyline']),
            float(game['pointsbet_moneylineWinPct']),
            float(game['pointsbet_spread']),
            float(game['pointsbet_spreadML']),
            float(game['pointsbet_spreadWinPct']),
            float(game['pointsbet_ou']),
            float(game['pointsbet_ouML']),
            float(game['pointsbet_ouWinPct']),
            float(game['pointsbet_score']),
            float(game['pointsbet_oppScore']),
        ]
        pointsbet.append(pointsbet_info)

    return draftkings, fanduel, mgm, pointsbet

# Helper function to get team ID based on team short name
def get_team_id(conn, team_short_name):

    # JAX vs JAC, WSH vs WAS, CLE vs CLV
    if team_short_name == 'CLV':
        team_short_name = 'CLE'
    
    elif team_short_name == 'JAC':
        team_short_name = 'JAX'
    
    elif team_short_name =='WAS':
        team_short_name ='WSH'

    cur = conn.cursor()
    cur.execute("SELECT id FROM teams WHERE teamShortName = ?", (team_short_name,))
    result = cur.fetchone()
    return result[0] if result else None

# function
def replace_abbr_with_ids(conn, data_arrays):

    # Unpack the data arrays for each betting site
    draftkings, fanduel, mgm, pointsbet = data_arrays

    # Function to replace team abbreviations in a single game's data
    def replace_in_game(game_data):

        # Replace team and opponent abbreviations with IDs
        game_data[2] = get_team_id(conn, game_data[2])  # Team ID
        game_data[3] = get_team_id(conn, game_data[3])  # Opponent Team ID
        return game_data

    # Process each betting site's data
    draftkings = [replace_in_game(game) for game in draftkings]
    fanduel = [replace_in_game(game) for game in fanduel]
    mgm = [replace_in_game(game) for game in mgm]
    pointsbet = [replace_in_game(game) for game in pointsbet]

    return draftkings, fanduel, mgm, pointsbet

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
        draftkings_data, fanduel_data, mgm_data, pointsbet_data = process_json(data)
        draftkings_data, fanduel_data, mgm_data, pointsbet_data = replace_abbr_with_ids(conn, (draftkings_data, fanduel_data, mgm_data, pointsbet_data))

        # DraftKings data
        for line in draftkings_data:
            # print(line)
            insert_or_update_draft_kings(conn, line)
      
        # Fanduel data
        for line in fanduel_data:
            # print(line)
            insert_or_update_fanduels(conn, line)
      
        # MGM data
        for line in mgm_data:
            # print(line)
            insert_or_update_mgm(conn, line)
      
        # Pointsbet data
        for line in pointsbet_data:
            # print(line)
            insert_or_update_pointsbet(conn,line)
      
    conn.close()
if __name__ == "__main__":
    main()