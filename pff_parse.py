## parse the pff json file ##

# Notes on the json file
# Task: download the json data on Sunday morning to 
# NOTE: "projection" missing on player props becuase odds are available 24 to 36 hours prior to kickoff.
# NOTE: player and team ids do not match ESPN ids so do not use these for fk


# loop over the dictionary and pull the keys and values
import json

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
                  "prop_type", "projection", "line", "over", "over_value", "under", "under_value"]

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

def main():
    file = 'pff_prop_bets.json'
    data = read_json(file)

    keys_order, player_props_list = extract_player_props(data)

    print("props columns length:", len(keys_order))
    print(("props values length: "),len(player_props_list[0]))

    print("\nKeys:", keys_order)
    print("\nValues:", player_props_list[0])

if __name__ == "__main__":
    main()



