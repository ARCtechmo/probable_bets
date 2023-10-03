# parse the fantasypros json files #
# Notes on the json file
# NOTE: player and team ids do not match ESPN ids so do not use these for fk


# Task: modify the code to read multiple files

# loop over the dictionary and pull the keys and values
import json

def read_json(file):
    with open(file, 'r') as f:
        return json.load(f)

# extract required player data into a list of lists.
# each inner list contains details for a unique player based on fpid.
def extract_player_data(players):
    extracted_data = []
    unique_fpids = set()
    
    for player in players:
        fpid = player['fpid']
        
        # skip duplicate players
        if fpid in unique_fpids:
            continue
        
        unique_fpids.add(fpid)
        
        # extract required data
        name = player['name']
        position_id = player['position_id']
        team_id = player['team_id']
        stats = player['stats']
        
        player_data = [name, position_id, team_id] + [stats[key] for key in stats.keys()]
        extracted_data.append(player_data)
    
    return extracted_data

# gets the key values based on a sample player dictionary.
def get_key_values(sample_player):
    return ['name', 'position_id', 'team_id'] + list(sample_player['stats'].keys())

def main():
    files = [
    'fantasy_pros_DST_projections_2023_STD.json',
    'fantasy_pros_K_projections_2023_STD.json',
    'fantasy_pros_QB_projections_2023_STD.json',
    'fantasy_pros_RB_projections_2023_STD.json',
    'fantasy_pros_TE_projections_2023_STD.json',
    'fantasy_pros_WR_projections_2023_STD.json'
    ]

    # Task: add check to ensure key lenght equals value length
    for file in files:

        # file = 'fantasy_pros_QB_projections_2023_STD.json'
        data = read_json(file)

        # Extract position from the filename
        position = file.split('_')[2]
    
        if position == 'DST':
            DST_key_values = get_key_values(data['players'][0])
            DST_extracted_data = extract_player_data(data['players'])
            # print(f"Key Values for {position}:", DST_key_values)  
            # print(f"Extracted Data for {position}:", DST_extracted_data[:1])  
        

        elif position == 'K':
            K_key_values = get_key_values(data['players'][0])
            K_extracted_data = extract_player_data(data['players'])
            # print(f"Key Values for {position}:", K_key_values)  
            # print(f"\nExtracted Data for {position}:", K_extracted_data[:1]) 

        elif position == 'QB':
            QB_key_values = get_key_values(data['players'][0])
            QB_extracted_data = extract_player_data(data['players'])
            # print(f"Key Values for {position}:", QB_key_values)  
            # print(f"\nExtracted Data for {position}:", QB_extracted_data[:1])

        elif position == 'RB':
            RB_key_values = get_key_values(data['players'][0])
            RB_extracted_data = extract_player_data(data['players'])
            print(f"Key Values for {position}:", RB_key_values)  
            print(f"\nExtracted Data for {position}:", RB_extracted_data[:1])

        elif position == 'TE':
            TE_key_values = get_key_values(data['players'][0])
            TE_extracted_data = extract_player_data(data['players'])
            print(f"Key Values for {position}:", TE_key_values)  
            print(f"\nExtracted Data for {position}:", TE_extracted_data[:1])

        elif position == 'WR':
            WR_key_values = get_key_values(data['players'][0])
            WR_extracted_data = extract_player_data(data['players'])
            print(f"Key Values for {position}:", WR_key_values)  
            print(f"\nExtracted Data for {position}:", WR_extracted_data[:1])

        

if __name__ == "__main__":
    main()
