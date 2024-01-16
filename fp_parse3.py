# parse the fantasypros json files #
from database import create_connection
import json
import os
import glob
from datetime import datetime

def read_json(file):
    with open(file, 'r') as f:
        return json.load(f)

## NOTE: the functions that implement exception handling: extract_player_data(), get_athlete_id(), enhanced_parse_name()
## NOTE: edge cases captured are the following:     
# 1) players with the same attributes:
# first and / or last name and same position and same team (no solution)
# first or last name and same position and same team (solved)
# 2) hyphenated last names fname-lname
# 3) players with Sr., Jr., II, III last name 
# 4) other name variations: O'Connell, St. John, etc...

# start here next
### NOTE: approach for next coding session ###
## I am going to have to use both 'name' and 'filename' keys to get this right
## Review each exception in the database to see how the actual names resides in the table
## focus on improving the enhanced_parse_name() function as it is currently implemented
## 1) do not remove the ".", the "-", or the "'" i.e. caputre the entire 1st and second index of the 'name' key
## 2) use the indexes to determine first and last names: 1st, 2nd, 3rd indexes of each key
## 3) the datbase include jr, sr. as part of the last names (e.g beckham jr. )
## 4) Amon-Ra St. Brown is a good example
## 5) modification to  the sql query get_athlete_id() may be needed by usings "startswith" or "endswith"
## provide GPT4 with one or two examples of name variations at a time to fix then test ##
## also provide it with the specific json snippet of that exception

# TEST RESULTS: additional modifications needed
#####  TEST RESULTS #####
# QB: Aidan O'Connell, C.J. Beathard 
# WR: Amon-Ra St. Brown, A.J. Brown, Odell Beckham Jr., Jaxon Smith-Njigba, Wan'Dale Robinson
# WR: Marquez Valdes-Scantling, Marvin Mims Jr., Allen Robinson II, Cedrick Wilson Jr.
# WR: Ihmir Smith-Marsette, Lil'Jordan Humphrey, John Metchie III, Donovan Peoples-Jones
# WR: Calvin Austin III, elus Jones Jr.
# TE: T.J. Hockenson, Mo Alie-Cox, Travis Etienne Jr., Kenneth Walker III, 
# RB: D'Andre Swift, De'Von Achane, Chris Rodriguez Jr., Clyde Edwards-Helaire,
# RB: D'Onta Foreman, D'Ernest Johnson, Melvin Gordon III", Pierre Strong Jr.
##### TEST RESULTS #####

# TASK: NOTE: possible solution to caputre more name variations
# need another loop to caputre all of the 'none' values 
# use the 'filename' key to try to capture additional name variations
        
# TASK
# create the tables for each position in database.py
# NOTE:  the stat categories vary by position so they require separate tables
    
# function handles name variations
# function integrates with extract_player_data() to handle name variations
def enhanced_parse_name(name, filename=None):
   
    # Helper function to remove special characters
    def remove_special_chars(s):
        return s.replace("'", "").replace("-", "").replace(".", "")

    # Lowercase the name for standardization
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

    # Identify suffix and remove special characters
    original_suffix = original_parts[-1] if original_parts[-1] in suffixes else None
    file_suffix = file_parts[-1] if file_parts[-1] in suffixes else None

    # Create name variations
    original_name = [remove_special_chars(part) for part in original_parts if part not in suffixes]
    file_name = [remove_special_chars(part) for part in file_parts if part not in suffixes]

    return {
        'original_name': original_name,
        'original_suffix': original_suffix,
        'file_name': file_name,
        'file_suffix': file_suffix
    }

# NOTE: DO NOT DELETE UNTIL TESTING IS COMPLETE
# NOTE: function is partially correct but does not handle edge cases
# Helper function to get athlete ID based on name
# def get_athlete_id(conn, name, position_abbr, team_short_name):
#     first_name, last_name = name.split(" ", 1)
#     cur = conn.cursor()
#     query = '''
#         SELECT a.id 
#         FROM athletes a
#         JOIN playerStatistics ps ON a.id = ps.playerFK
#         JOIN positions p ON ps.PlayerPositionFK = p.id
#         JOIN teams t ON ps.playerTeamFK = t.id
#         WHERE a.firstName = ? AND a.lastName = ? 
#         AND p.abbr = ? AND t.teamShortName = ?
#     '''
#     cur.execute(query, (first_name, last_name, position_abbr, team_short_name))
#     result = cur.fetchone()
#     return result[0] if result else None

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

# NOTE: do not delete until testing is complete
# NOTE: function is partially correct but does not handle edge cases
# def extract_player_data(conn, season, week, players):
#     extracted_data = []
#     unique_fpids = set()

#     for player in players:
#         fpid = player['fpid']
#         if fpid in unique_fpids:
#             continue
#         unique_fpids.add(fpid)

#         name = player['name']
#         position_abbr = player['position_id']
#         team_short_name = player['team_id']
#         athlete_id = get_athlete_id(conn, name, position_abbr, team_short_name)

#         # Assuming get_position_id and get_team_id functions are unchanged
#         position_id = get_position_id(conn, position_abbr)
#         team_id = get_team_id(conn, team_short_name)

#         stats = player['stats']
#         player_data = [season, week, athlete_id, position_id, team_id] + [stats[key] for key in stats.keys()]
#         extracted_data.append(player_data)

#     return extracted_data


# gets the key values based on a sample player dictionary.
def get_key_values(sample_player):
    return ['season', 'week', 'name', 'position_id', 'team_id'] + list(sample_player['stats'].keys())


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

            #### testing ####
            # for list in K_extracted_data:
            #     print(list)
            #### testing ####

        elif position == 'QB':
            QB_key_values = get_key_values(data['players'][0])
            QB_extracted_data = extract_player_data(conn, season, week, data['players'])

            # Check if key length matches data length for each player
            if all(len(QB_key_values) == len(player_data) for player_data in QB_extracted_data):
                print(f"\nKey lengths match value lengths for {position}.")
            else:
                print(f"\nKey lengths do NOT match value lengths for {position}.")

            # print(f"Key Values for {position}:", QB_key_values)  
            # print(f"Extracted Data for {position}:", QB_extracted_data)

            #### testing ####
            # for list in QB_extracted_data:
            #     print(list)
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
                
            #### testing ####
            # for list in RB_extracted_data:
            #     print(list)
            #### testing ####

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

    conn.close()
if __name__ == "__main__":
    main()


