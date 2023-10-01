# parse the fantasypros json files #
# Notes on the json file
# NOTE: player and team ids do not match ESPN ids so do not use these for fk


# Task: loop through the players list of dictionaries to extract keys:
# - "players" is a list of dictionaries: "name", "position_id", "team_id"
# - "stats" is a dictionary of k,v pairs: 

# "points", "points_ppr", "points_half", "pass_att", "pass_cmp", 
# "pass_yds",  "pass_tds", "pass_ints", "pass_yds_300", "pass_yds_400",
# "rush_att", "rush_yds", "rush_tds", "rush_yds_100", "rush_yds_200", 
# "scrimage_yards_100", "scrimage_yards_200", "fumbles", "ret_tds", "2pt_tds"

# loop over the dictionary and pull the keys and values
import json

def read_json(file):
    with open(file, 'r') as f:
        return json.load(f)

def filter_data_by_keys(data, keys):
    return {k: v for k, v in data.items() if k in keys}


def main():
    file = 'fantasy_pros_QB_projections_2023_STD.json'
    data = read_json(file)

if __name__ == "__main__":
    main()
