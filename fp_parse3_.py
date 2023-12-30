# parse the fantasypros json files #
from database import create_connection
import json
import os
import glob
from datetime import datetime

def read_json(file):
    with open(file, 'r') as f:
        return json.load(f)

# Helper function to get athlete ID based on name
# def get_athlete_id(conn, name):
#     first_name, last_name = name.split(" ", 1)
#     cur = conn.cursor()
#     cur.execute("SELECT id FROM athletes WHERE firstName = ? AND lastName = ?", (first_name, last_name))
#     result = cur.fetchone()
#     return result[0] if result else None

def get_athlete_id(conn, name, position_abbr, team_short_name):
    first_name, last_name = name.split(" ", 1)
    cur = conn.cursor()
    query = '''
        SELECT a.id 
        FROM athletes a
        JOIN playerStatistics ps ON a.id = ps.playerFK
        JOIN positions p ON ps.PlayerPositionFK = p.id
        JOIN teams t ON ps.playerTeamFK = t.id
        WHERE a.firstName = ? AND a.lastName = ? 
        AND p.abbr = ? AND t.teamShortName = ?
    '''
    cur.execute(query, (first_name, last_name, position_abbr, team_short_name))
    result = cur.fetchone()
    return result[0] if result else None


# Helper function to get position ID based on position abbreviation
def get_position_id(conn, position_abbr):
    cur = conn.cursor()
    cur.execute("SELECT id FROM positions WHERE abbr = ?", (position_abbr,))
    result = cur.fetchone()
    return result[0] if result else None

# Helper function to get team ID based on team short name
def get_team_id(conn, team_short_name):
    cur = conn.cursor()
    cur.execute("SELECT id FROM teams WHERE teamShortName = ?", (team_short_name,))
    result = cur.fetchone()
    return result[0] if result else None

# extract required player data into a list of lists.
# each inner list contains details for a unique player based on fpid.
# def extract_player_data(conn, season, week, players):
#     extracted_data = []
#     unique_fpids = set()
#     unique_rows = set()
    
#     for player in players:
#         fpid = player['fpid']
        
#         # skip duplicate players
#         if fpid in unique_fpids:
#             continue
#         unique_fpids.add(fpid)

#         # Extract required data and replace with corresponding IDs
#         athlete_id = get_athlete_id(conn, player['name'])
#         position_id = get_position_id(conn, player['position_id'])
#         team_id = get_team_id(conn, player['team_id'])
#         stats = player['stats']

#         # Compile the player data with the IDs
#         player_data = [season, week, athlete_id, position_id, team_id] + [stats[key] for key in stats.keys()]
                
#         # Skip duplicate rows based on player_data
#         player_data_tuple = tuple(player_data)
#         if player_data_tuple in unique_rows:
#             continue
#         unique_rows.add(player_data_tuple)
#         extracted_data.append(player_data)
    
#     return extracted_data

def extract_player_data(conn, season, week, players):
    extracted_data = []
    unique_fpids = set()

    for player in players:
        fpid = player['fpid']
        if fpid in unique_fpids:
            continue
        unique_fpids.add(fpid)

        name = player['name']
        position_abbr = player['position_id']
        team_short_name = player['team_id']
        athlete_id = get_athlete_id(conn, name, position_abbr, team_short_name)

        # Assuming get_position_id and get_team_id functions are unchanged
        position_id = get_position_id(conn, position_abbr)
        team_id = get_team_id(conn, team_short_name)

        stats = player['stats']
        player_data = [season, week, athlete_id, position_id, team_id] + [stats[key] for key in stats.keys()]
        extracted_data.append(player_data)

    return extracted_data


# gets the key values based on a sample player dictionary.
def get_key_values(sample_player):
    return ['season', 'week', 'name', 'position_id', 'team_id'] + list(sample_player['stats'].keys())

# start here next: 
# continue TESTING: the 'name', 'position_id', and 'team_id' in the lists should matches the corresponding foreign key values in the db
# create the tables for each position (NOTE:  the stat categories vary by position)

def main():
    
    # Create a database connection
    conn = create_connection()

    # Get the current year in YYYY format
    year = datetime.now().strftime('%Y') 

    # Pattern to match files
    pattern = f'fantasy_pros_*_projections_{year}_week*.json'

    # List all matching files
    files = glob.glob(pattern)

    for file in files:

        # Check if the file exists in the current directory
        if not os.path.exists(file):
            print(f"{file} not in the directory.")
            continue  # Skip the rest of the loop for this file

        # file = 'fantasy_pros_QB_projections_2023_STD.json'
        data = read_json(file)

        # Extract position from the filename
        position = file.split('_')[2]

        # pass season and week to extract_player_data function
        season = data['season']
        week = data['week']

        if position == 'DST':
            DST_key_values = get_key_values(data['players'][0])
            DST_extracted_data = extract_player_data(conn, season, week, data['players'])

            # Check if key length matches data length for each player
            if all(len(DST_key_values) == len(player_data) for player_data in DST_extracted_data):
                print(f"Key lengths match value lengths for {position}.")
            else:
                print(f"Key lengths do NOT match value lengths for {position}.")

            # print(f"Key Values for {position}:", DST_key_values)  
            # print(f"Extracted Data for {position}:", DST_extracted_data[:1])  
        
        elif position == 'K':
            K_key_values = get_key_values(data['players'][0])
            K_extracted_data = extract_player_data(conn, season, week, data['players'])

            # Check if key length matches data length for each player
            if all(len(K_key_values) == len(player_data) for player_data in K_extracted_data):

                print(f"\nKey lengths match value lengths for {position}.")
            else:
                print(f"\nKey lengths do NOT match value lengths for {position}.")

            # print(f"Key Values for {position}:", K_key_values)  
            # print(f"Extracted Data for {position}:", K_extracted_data[:1]) 

        elif position == 'QB':
            QB_key_values = get_key_values(data['players'][0])
            QB_extracted_data = extract_player_data(conn, season, week, data['players'])

            # Check if key length matches data length for each player
            if all(len(QB_key_values) == len(player_data) for player_data in QB_extracted_data):
                print(f"\nKey lengths match value lengths for {position}.")
            else:
                print(f"\nKey lengths do NOT match value lengths for {position}.")

            print(f"Key Values for {position}:", QB_key_values)  
            # print(f"Extracted Data for {position}:", QB_extracted_data)

            #### testing ####
            for list in QB_extracted_data:
                print(list)
            #### testing ####

        elif position == 'RB':
            RB_key_values = get_key_values(data['players'][0])
            RB_extracted_data = extract_player_data(conn, season, week, data['players'])

            # Check if key length matches data length for each player
            if all(len(RB_key_values) == len(player_data) for player_data in RB_extracted_data):
                print(f"\nKey lengths match value lengths for {position}.")
            else:
                print(f"\nKey lengths do NOT match value lengths for {position}.")
            
            # print(f"Key Values for {position}:", RB_key_values)  
            # print(f"Extracted Data for {position}:", RB_extracted_data[:1])

        elif position == 'TE':
            TE_key_values = get_key_values(data['players'][0])
            TE_extracted_data = extract_player_data(conn, season, week, data['players'])

            # Check if key length matches data length for each player
            if all(len(TE_key_values) == len(player_data) for player_data in TE_extracted_data):
                print(f"\nKey lengths match value lengths for {position}.")
            else:
                print(f"\nKey lengths do NOT match value lengths for {position}.")
            
            # print(f"Key Values for {position}:", TE_key_values)  
            # print(f"Extracted Data for {position}:", TE_extracted_data[:1])

        elif position == 'WR':
            WR_key_values = get_key_values(data['players'][0])
            WR_extracted_data = extract_player_data(conn, season, week, data['players'])

            # Check if key length matches data length for each player
            if all(len(WR_key_values) == len(player_data) for player_data in WR_extracted_data):
                print(f"\nKey lengths match value lengths for {position}.")
            else:
                print(f"\nKey lengths do NOT match value lengths for {position}.")
            # print(f"Key Values for {position}:", WR_key_values)  
            # print(f"Extracted Data for {position}:", WR_extracted_data[:1])

    conn.close()

if __name__ == "__main__":
    main()


