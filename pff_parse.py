## parse the pff json file ##

# Notes on the json file
# NOTE: the json file has two sections: game props and player props 
# NOTE: some player "projections" props missing becuase odds are available 24 to 36 hours prior to kickoff.
# NOTE: player and team ids do not match ESPN ids so do not use these for fk
# NOTE: you will need two tables: pff_player_props, pff_team_props

## task: we will only use player_props
## task: create the lists from the keys
## task: "player props" keys: player_full_name, team_name, opponent_team_name, prop_type, line, over, under, 
## task: create functions similar to the functions in fp_parse4.py to get player and team ids
## task: create the lists with the correct foreign keys
## task: create the tables and functions in database.py

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


# fixme: function mostly works but some names with Jr. are left out
def query_athlete_id(conn, standardized_name, suffix='', team=None, position=None):
    # Initialize cursor
    cursor = conn.cursor()

    # Split the standardized name into first and last names
    name_parts = standardized_name.split()
    first_name = name_parts[0]
    last_name = name_parts[-1] if len(name_parts) > 1 else ''

    # Initial query based on name
    query = """
    SELECT id FROM athletes
    WHERE LOWER(firstName) = LOWER(?) AND LOWER(lastName) = LOWER(?)
    """
    params = (first_name, last_name)
    cursor.execute(query, params)
    results = cursor.fetchall()

    # If one match is found, return the athlete ID
    if len(results) == 1:
        return results[0][0]

    # If no direct match, perform enhanced query considering team and position
    if len(results) > 1 and (team or position):
        enhanced_query = """
        SELECT id FROM athletes
        WHERE LOWER(firstName) = ? AND LOWER(lastName) = ? AND (teamCode = ? OR position = ?)
        """
        enhanced_params = (first_name, last_name, team, position)
        cursor.execute(enhanced_query, enhanced_params)
        enhanced_results = cursor.fetchall()

        # If one match is found with enhanced criteria, return the athlete ID
        if len(enhanced_results) == 1:
            return enhanced_results[0][0]

    # No match found or multiple ambiguous matches
    return None

def insert_athlete_id(conn, player_props_list):
    # Iterate over player_props_list and update with athlete IDs
    updated_player_props_list = []
    for player_prop in player_props_list:
        player_name = player_prop[1]  

        # Query for athlete ID using the player name directly
        athlete_id = query_athlete_id(conn, player_name)

        # Replace player name with athlete ID in the list
        updated_prop = player_prop.copy()
        updated_prop[1] = athlete_id if athlete_id else player_prop[1]  # Keep original name if ID not found

        updated_player_props_list.append(updated_prop)
    return updated_player_props_list

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

    # updated_player_props_list
    updated_player_props_list = insert_athlete_id(conn, player_props_list)
    # print("\nUpdated Values:", updated_player_props_list[0])

    ## test loop ##
    for player in updated_player_props_list:
        print(player)

if __name__ == "__main__":
    main()



