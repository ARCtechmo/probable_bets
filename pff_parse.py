## parse the pff json file ##

# Notes on the json file
# NOTE: you will need two tables: pff_player_props, pff_team_props
# NOTE: the json file has two sections: game props and player props 
# NOTE: some player "projections" props missing becuase odds are available 24 to 36 hours prior to kickoff.


## task: test to ensure all of the foreign keys match the players, teams, positions with multiple json files
## task: create the tables and functions in database.py
## NOTE: you will need to allow NULL values for the athlete

# loop over the dictionary and pull the keys and values
from database import create_connection
import json
import os
import re

def read_json(file):
    with open(file, 'r') as f:
        return json.load(f)

def filter_data_by_keys(data, keys):
    return {k: v for k, v in data.items() if k in keys}

def extract_props_last_updated_at(data):
    props_last_updated_at_str = data.get('props_last_updated_at', None)
    if props_last_updated_at_str:

        # Splitting the datetime string at 'T' and keeping the date part
        return props_last_updated_at_str.split('T')[0]
    return None

def extract_player_props(data):
    keys_order = ["props_last_updated_at", "player_full_name", "position", "team_name", "opponent_team_name",
                  "prop_type", "projection", "line", "over", "under"]

    player_props_list = []
    for player_prop in data.get('player_props', []):
        filtered_player_prop = filter_data_by_keys(player_prop, keys_order[1:])
        values_list = [filtered_player_prop.get(k, None) for k in keys_order[1:]]
        
        # Replace 'None' values with 'null'
        values_list = ["null" if v is None else v for v in values_list]
        player_props_list.append(values_list)

    props_last_updated_at = extract_props_last_updated_at(data)

    # Replace 'None' value of props_last_updated_at with 'null'
    props_last_updated_at = "null" if props_last_updated_at is None else props_last_updated_at
    for values_list in player_props_list:
        values_list.insert(0, props_last_updated_at)

    return keys_order, player_props_list


# match the player to the athlete foriegn keys
def query_athlete_id(conn, standardized_name, suffix='', team=None, position=None):
    # Initialize cursor
    cursor = conn.cursor()

    # Helper function to toggle periods in abbreviations
    def toggle_periods(name_part):
        if '.' in name_part:  
            
            # Remove periods if present
            return name_part.replace('.', '')
        if len(name_part) <= 2:  
            
            # Assume it's an abbreviation if 1 or 2 characters long
            return f"{name_part[0]}.{name_part[1]}." if len(name_part) == 2 else f"{name_part}."  # Add periods
        return name_part

    # Split the standardized name into first and last names
    name_parts = standardized_name.split()
    first_name = name_parts[0]
    first_name_alternate = toggle_periods(first_name)
    last_name = " ".join(name_parts[1:])

    # Initial query based on name
    query = """
    SELECT id FROM athletes
    WHERE (LOWER(firstName) = LOWER(?) OR LOWER(firstName) = LOWER(?)) AND LOWER(lastName) = LOWER(?)
    """
    params = (first_name, first_name_alternate, last_name)
    cursor.execute(query, params)
    results = cursor.fetchall()

    # If one match is found, return the athlete ID
    if len(results) == 1:
        return results[0][0]
    
    # If no direct match, try stripping common suffixes and querying again
    if not results:
        suffixes = ['Jr.', 'Sr.', 'II', 'III', 'IV']
        for suffix in suffixes:
            if last_name.endswith(suffix):
                last_name_without_suffix = last_name.rsplit(' ', 1)[0]
                cursor.execute(query, (first_name, first_name_alternate, last_name_without_suffix))
                results = cursor.fetchall()
                if len(results) == 1:
                    return results[0][0]
                
                # Exit the loop after trying with the first found suffix
                break  

    # If still no match, perform enhanced query considering team and position
    if len(results) > 1 and (team or position):
        enhanced_query = """
        SELECT id FROM athletes
        WHERE LOWER(firstName) = (?) AND LOWER(lastName) = (?) AND (teamCode = (?) OR position = (?))
        """
        enhanced_params = (
            first_name, last_name, team.lower() 
            if team else None, position.lower() if position else None
            )
        cursor.execute(enhanced_query, enhanced_params)
        enhanced_results = cursor.fetchall()

        # If one match is found with enhanced criteria, return the athlete ID
        if len(enhanced_results) == 1:
            return enhanced_results[0][0]
    
    # No match found or multiple ambiguous matches
    return None

# NOTE: this function must be placed after the query_athlete_id() function
def insert_athlete_id(conn, player_props_list):
    # Iterate over player_props_list and update with athlete IDs
    updated_player_props_list = []
    for player_prop in player_props_list:
        player_name = player_prop[1]  

        # Query for athlete ID using the player name directly
        athlete_id = query_athlete_id(conn, player_name)

        # Replace player name with athlete ID in the list
        updated_prop = player_prop.copy()

        # Keep original name if ID not found
        # updated_prop[1] = athlete_id if athlete_id else player_prop[1]

        # Return None if ID not found
        updated_prop[1] = athlete_id if athlete_id is not None else None    

        updated_player_props_list.append(updated_prop)
    return updated_player_props_list

## function to match teams
# NOTE: this function must be placed after the insert_athlete_id() function
def match_and_replace_team_abbreviations(conn, player_props_list):

    # First, insert athlete IDs into the player props list
    updated_player_props_list_athlete_id = insert_athlete_id(conn, player_props_list)

    # Dictionary to handle variations in team abbreviations
    # ARI vs ARZ, CLE vs CLV, HOU vs HST, JAX VS JAC, LAR vs LA, WSH vs WAS
    team_abbreviation_variations = {
        "ARZ": "ARI",
        "CLV": "CLE",
        "HST": "HOU",
        "JAC": "JAX",
        "LA": "LAR",
        "WAS": "WSH"
    }

    # Query the database for team short names and their corresponding IDs
    cursor = conn.cursor()
    cursor.execute("SELECT id, teamShortName FROM teams")
    team_data = cursor.fetchall()
    
    # Map teamShortName to team ID
    team_id_map = {team[1]: team[0] for team in team_data}  

    # Function to get the team ID using abbreviation
    def get_team_id(abbreviation):

        # Correct the abbreviation if there's a known variation
        corrected_abbreviation = team_abbreviation_variations.get(abbreviation, abbreviation)
        
        # Return the team ID for the corrected abbreviation
        return team_id_map.get(corrected_abbreviation)

    # Replace team abbreviations in the list with corresponding team IDs
    for prop in updated_player_props_list_athlete_id:
        team_abbr = prop[3]  
        opponent_abbr = prop[4]  

        # Get the team ID for both team and opponent
        team_id = get_team_id(team_abbr)
        opponent_team_id = get_team_id(opponent_abbr)

        # Replace the abbreviations with team IDs in the list
        prop[3] = team_id
        prop[4] = opponent_team_id

    return updated_player_props_list_athlete_id


## function to match positions
# NOTE: this function must be placed after the match_and_replace_team_abbreviations() function
def match_and_replace_position_abbreviations(conn, player_props_list):

    # insert athlete and team IDs into the player props list
    updated_player_props_list_athlete_team_id = match_and_replace_team_abbreviations(conn, player_props_list)

    # Mapping to handle variations in position abbreviations
    # position abbreviation variations: K vs PK
    position_abbreviation_variations = {"K": "PK"}

    # Query the database for position names and their corresponding IDs
    cursor = conn.cursor()
    cursor.execute("SELECT id, abbr FROM positions")
    position_data = cursor.fetchall()

    # Mapping of team abbreviation to position ID
    position_id_map = {position[1]: position[0] for position in position_data} 

    # Function to get the position ID using abbreviation
    def get_position_id(abbreviation):

        # Correct the abbreviation if there's a known variation
        corrected_abbreviation = position_abbreviation_variations.get(abbreviation, abbreviation)
        
        # Return the position ID for the corrected abbreviation
        return position_id_map.get(corrected_abbreviation)

    # Replace position abbreviations in the list with corresponding position IDs
    for prop in updated_player_props_list_athlete_team_id:
        position_abbr = prop[2]  

        # Get the position ID
        position_id = get_position_id(position_abbr)

        # Replace the abbreviation with the position ID in the list
        prop[2] = position_id

    return updated_player_props_list_athlete_team_id

def main():
    conn = create_connection()

    # Pattern to match files like 
    file_pattern = re.compile(r'pff_prop_bets.*\.json$')

    matched_files = [f for f in os.listdir('.') if file_pattern.match(f)]
    if not matched_files:
        print("No matching 'pff_prop_bets' file found in the directory.")
        return

    # sort the files to get the most recent one, if needed
    latest_file = sorted(matched_files, reverse=True)[0]

    # use the first matched file
    # file = matched_files[0]
    
    data = read_json(latest_file)
    keys_order, player_props_list = extract_player_props(data)


    # test to make sure key, value lengths match
    # print("props columns length:", len(keys_order))
    # print(("props values length: "),len(player_props_list[0]))

    # print("\nKeys:", keys_order)
    # print("\nValues:", player_props_list[0])

    ## test loop ##
    # updated_player_props_list
    # updated_player_props_list_athlete_id = insert_athlete_id(conn, player_props_list)
    # for player in updated_player_props_list_athlete_id:
    #     print(player)
    
    ## test loop ##
    # updated_player_props_list
    # updated_player_props_list_athlete_team_id = match_and_replace_team_abbreviations(conn, player_props_list)
    # for player in updated_player_props_list_athlete_team_id:
    #     print(player)

    ## test loop ##
    # final_updated_player_props_list
    final_updated_player_props_list_athlete_team_position_id = match_and_replace_position_abbreviations(conn, player_props_list)
    for player in final_updated_player_props_list_athlete_team_position_id:
        print(player)

if __name__ == "__main__":
    main()



