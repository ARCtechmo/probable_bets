# parse the fantasypros json files #

from database import (
    create_connection,
    insert_or_update_fantasy_pros_QB,
    insert_or_update_fantasy_pros_RB,
    insert_or_update_fantasy_pros_TE,
    insert_or_update_fantasy_pros_K,
    insert_or_update_fantasy_pros_Def,
    insert_or_update_fantasy_pros_WR,
)
import json
import os
import glob
from datetime import datetime

def read_json(file):
    with open(file, 'r') as f:
        return json.load(f)
  
# the functions that implement exception handling: extract_player_data(), get_athlete_id(), enhanced_parse_name()
## NOTE: function built to handle name variations edge cases   
def enhanced_parse_name(name, filename=None):
   
    # Lowercase the name for standardization, but do not remove special characters
    name = name.lower()
    if filename:
        # Extract name from filename if available, usually in a more standardized format
        name_from_file = filename.split('.')[0].replace('-', ' ').lower()
    else:
        name_from_file = name

    # Split names into parts
    original_parts = name.split()
    file_parts = name_from_file.split()

    # Suffixes to check
    suffixes = ['jr', 'sr', 'ii', 'iii','iv']

    # Identify suffix but include it as part of the original name
    original_name = [part for part in original_parts]
    file_name = [part for part in file_parts if part not in suffixes]

    return {
        'original_name': original_name,
        'file_name': file_name
    }

# function finds the athlete in the database
# function integrates with extract_player_data() to handle name variations
def get_athlete_id(conn, name, position_abbr, team_short_name):

    # Check if the position_abbr is 'K' and change it to 'PK' for database query
    if position_abbr == 'K':
        position_abbr = 'PK'
    
    # JAX vs JAC, WSH vs WAS, CLE vs CLV
    if team_short_name == 'CLV':
        team_short_name = 'CLE'
    
    elif team_short_name == 'JAC':
        team_short_name = 'JAX'
    
    elif team_short_name =='WAS':
        team_short_name ='WSH'

    first_name, last_name = name[0], ' '.join(name[1:]) if len(name) > 1 else ''
    
    # Expecting 'name' to be a list of name parts (first name and last name)
    cur = conn.cursor()
    query = """
        SELECT a.id 
        FROM athletes a
        JOIN playerStatistics ps ON a.id = ps.playerFK
        JOIN positions p ON ps.PlayerPositionFK = p.id
        JOIN teams t ON ps.playerTeamFK = t.id
        WHERE LOWER(a.firstName) = LOWER(?) AND LOWER(a.lastName) = LOWER(?) 
        AND p.abbr = ? AND t.teamShortName = ?
    """
  
    cur.execute(query, (first_name, last_name, position_abbr, team_short_name))
    result = cur.fetchone()

    return result[0] if result else None

# Helper function to get position ID based on position abbreviation
def get_position_id(conn, position_abbr):

    # Check if the position_abbr is 'K' and change it to 'PK' for database query
    if position_abbr == 'K':
        position_abbr = 'PK'

    cur = conn.cursor()
    cur.execute("SELECT id FROM positions WHERE abbr = ?", (position_abbr,))
    result = cur.fetchone()
    return result[0] if result else None

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

# function matches 'players' from the json file using the 'name' key to the 'athlete' id in the database
# function integrates the get_athlete_id() and enhanced_parse_name() functions to handle name variations
def extract_player_data(conn, season, week, players):
    extracted_data = []
    unique_fpids = set()

    for player in players:
        fpid = player['fpid']
        if fpid in unique_fpids:
            continue
        unique_fpids.add(fpid)

        # Using enhanced_parse_name() to process player names
        name_variations = enhanced_parse_name(player['name'], player.get('filename'))
        position_abbr = player['position_id']
        team_short_name = player['team_id']
        
        # use name variations in get_athlete_id()
        athlete_id = None
        for variation in [name_variations['original_name'], name_variations['file_name']]:
                        
            athlete_id = get_athlete_id(conn, variation, position_abbr, team_short_name)
            if athlete_id:
                break
        
        position_id = get_position_id(conn, position_abbr)
        team_id = get_team_id(conn, team_short_name)

        stats = player['stats']
        player_data = [season, week, athlete_id, position_id, team_id] + [stats[key] for key in stats.keys()]
        extracted_data.append(player_data)

    return extracted_data

# function extract the key, values for the Defense json files
# separate function because 'name' and 'position_id' fields are not necessary
def extract_dst_player_data(conn, season, week, players):
    extracted_data = []
    unique_fpids = set()

    for player in players:
        team_short_name = player['team_id']
        team_id = get_team_id(conn, team_short_name)

        stats = player['stats']
        player_data = [season, week, team_id] + [stats[key] for key in stats.keys()]
        extracted_data.append(player_data)

    return extracted_data

# gets the key values based on players for K, QB, RB, TE, WR 
def get_key_values(sample_player):
    return ['season', 'week', 'name', 'position_id', 'team_id'] + list(sample_player['stats'].keys())

# gets the key values based on the team defenses 
def get_def_key_values(sample_player):
    return ['season', 'week', 'team_id'] + list(sample_player['stats'].keys())

def main():
    
    # Create a database connection
    conn = create_connection()

    # Get the current year in YYYY format
    current_year = datetime.now().strftime('%Y') 

    # Calculate the previous year
    previous_year = str(int(current_year) - 1)

    # Pattern to match files for the current and previous year
    pattern_current_year = f'fantasy_pros_*_projections_{current_year}_week*.json'
    pattern_previous_year = f'fantasy_pros_*_projections_{previous_year}_week*.json'

    # List all matching files
    files = glob.glob(pattern_current_year) + glob.glob(pattern_previous_year)

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
        season = int(season)

        week = data['week']
        week = int(week)

        if position == 'DST':
            DST_key_values = get_def_key_values(data['players'][0])
            DST_extracted_data = extract_dst_player_data(conn, season, week, data['players'])

            # Check if key length matches data length for each player
            if all(len(DST_key_values) == len(player_data) for player_data in DST_extracted_data):
                print(f"\nKey lengths match value lengths for {position}.")
            else:
                print(f"\nKey lengths do NOT match value lengths for {position}.")

            # print(f"Key Values for {position}:", DST_key_values)  
            # print(f"Extracted Data for {position}:", DST_extracted_data[:1])

            #### testing ####
            # for list in DST_extracted_data:
            #     print(list)
            #### testing ####  
                
            ## export the arrays for each position into the database ##
            ## export functions are from database.py ##
            insert_or_update_fantasy_pros_Def(conn, DST_extracted_data)
            
        
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

            #### testing ####
            # for list in K_extracted_data:
            #     print(list)
            #### testing ####
            
            ## export the arrays for each position into the database ##
            ## export functions are from database.py ##
            insert_or_update_fantasy_pros_K(conn, K_extracted_data) 

        elif position == 'QB':
            QB_key_values = get_key_values(data['players'][0])
            QB_extracted_data = extract_player_data(conn, season, week, data['players'])

            # Check if key length matches data length for each player
            if all(len(QB_key_values) == len(player_data) for player_data in QB_extracted_data):
                print(f"\nKey lengths match value lengths for {position}.")
            else:
                print(f"\nKey lengths do NOT match value lengths for {position}.")

            # print(f"Key Values for {position}:", QB_key_values)  
            # print(f"Extracted Data for {position}:", QB_extracted_data[:1])

            #### testing ####
            # for list in QB_extracted_data:
            #     print(list)
            #### testing ####

            ## export the arrays for each position into the database ##
            ## export functions are from database.py ##
            insert_or_update_fantasy_pros_QB(conn, QB_extracted_data)

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
                
            #### testing ####
            # for list in RB_extracted_data:
            #     print(list)
            #### testing ####
            
            ## export the arrays for each position into the database ##
            ## export functions are from database.py ##
            insert_or_update_fantasy_pros_RB(conn, RB_extracted_data)


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
                
            #### testing ####
            # for list in TE_extracted_data:
            #     print(list)
            #### testing ####
            
            ## export the arrays for each position into the database ##
            ## export functions are from database.py ##
            insert_or_update_fantasy_pros_TE(conn, TE_extracted_data) 

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

            #### testing ####
            # for list in WR_extracted_data:
            #     print(list)
            #### testing ####
            
            ## export the arrays for each position into the database ##
            ## export functions are from database.py ##
            insert_or_update_fantasy_pros_WR(conn, WR_extracted_data)


    conn.close()
if __name__ == "__main__":
    main()


