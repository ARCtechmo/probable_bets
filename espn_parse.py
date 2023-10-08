
# parse the json data

# Task: combine all of the list into a single row of data to be exported

import json
import os
import re
from glob import glob
from datetime import datetime

def read_json(file):
    with open(file, 'r') as f:
        return json.load(f)

def filter_data_by_keys(data, keys):
    return {k: v for k, v in data.items() if k in keys}

def extract_league_data(data):
    league_data = data.get('league', {})
    return filter_data_by_keys(league_data, ["id", "name"])

def extract_athlete_data_no_uniqueness_check(data, athlete_keys):
    athletes_list = []
    athletes_data = data.get('athletes', [])
    for athlete in athletes_data:
        athlete_info = athlete.get('athlete', {})
        if athlete_info:
            athletes_list.append(list(filter_data_by_keys(athlete_info, athlete_keys).values()))

    return athletes_list

# def extract_athlete_data_with_uniqueness_check(data, athlete_keys, athlete_ids):
#     athletes_list = []
#     athletes_data = data.get('athletes', [])
#     for athlete in athletes_data:
#         athlete_info = athlete.get('athlete', {})
#         if athlete_info:
#             id_tuple = tuple(athlete_info.get(key, None) for key in ['id', 'uid', 'guid'])
#             if id_tuple not in athlete_ids:
#                 athletes_list.append(list(filter_data_by_keys(athlete_info, athlete_keys).values()))
#                 athlete_ids.add(id_tuple)
#     return athletes_list

def extract_positions_data(data, position_keys):
    positions_list = []
    athletes_data = data.get('athletes', [])
    for athlete in athletes_data:
        athlete_info = athlete.get('athlete', {})
        if athlete_info:
            position_info = athlete_info.get('position', {})
            positions_list.append(list(filter_data_by_keys(position_info, position_keys).values()))
    return positions_list

def extract_status_data(data, status_keys):
    status_list = []
    athletes_data = data.get('athletes', [])
    for athlete in athletes_data:
        athlete_info = athlete.get('athlete', {})
        if athlete_info:
            status_info = athlete_info.get('status', {})
            status_list.append(list(filter_data_by_keys(status_info, status_keys).values()))
    return status_list

# def extract_teams_data_with_uniqueness_check(data, team_keys,team_ids): 
#     teams_list = []
#     athletes_data = data.get('athletes', [])
#     for athlete in athletes_data:
#         athlete_info = athlete.get('athlete', {})
#         if athlete_info:
#             team_data = {k: athlete_info.get(k, '') for k in team_keys}
#             team_id = team_data.get('teamId', None)
#             team_uid = team_data.get('teamUId', None)
#             if team_id not in team_ids and team_uid not in team_ids:
#                 teams_list.append(list(team_data.values()))
#                 team_ids.add(team_id)
#                 team_ids.add(team_uid)

#     return teams_list

def extract_teams_data_no_uniqueness_check(data, team_keys):  
    teams_list = []
    athletes_data = data.get('athletes', [])
    for athlete in athletes_data:
        athlete_info = athlete.get('athlete', {})
        if athlete_info:
            team_data = {k: athlete_info.get(k, '') for k in team_keys}
            teams_list.append(list(team_data.values()))  

    return teams_list  # Returning the list without uniqueness checks

def extract_seasons_data(data, season_keys, season_type_ids):
    season_type_list = []
    requested_season_data = data.get('requestedSeason', {})
    season_type_data = requested_season_data.get('type', {})
    type_id_tuple = tuple(season_type_data.get(k, None) for k in season_keys)
    if type_id_tuple not in season_type_ids:
        season_type_list.append(list(filter_data_by_keys(season_type_data, season_keys).values()))
        season_type_ids.add(type_id_tuple)
    return season_type_list

def extract_week_data(data, week_keys, week_numbers):
    week_list = []
    requested_season_data = data.get('requestedSeason', {})
    week_data = requested_season_data.get('type', {}).get('week', {})
    week_number = week_data.get('number', None)
    if week_number not in week_numbers:
        filtered_week_data = filter_data_by_keys(week_data, week_keys)
        if 'startDate' in filtered_week_data:
            filtered_week_data['startDate'] = filtered_week_data['startDate'].split('T')[0]
        if 'endDate' in filtered_week_data:
            filtered_week_data['endDate'] = filtered_week_data['endDate'].split('T')[0]
        week_list.append(list(filtered_week_data.values()))
        week_numbers.add(week_number)
    return week_list

# extract athlete 'values'
def extract_athlete_values(data):
    player_statistics_list = []
    athletes_data = data.get('athletes',[])
    for athlete in athletes_data:
        values_list = []
        categories = athlete.get('categories',[])
        for category in categories:
            values = category.get('values',[])
            for value in values:
                if value in [None, '-','']:
                    value = 'null'
                elif isinstance(value, float):
                    value = round(value, 1)
                values_list.append(value)
        player_statistics_list.append(values_list)
    return player_statistics_list            

# extract athlete 'ranks'
def extract_athlete_ranks(data):
    player_rank_list = []
    athletes_data = data.get('athletes', [])
    for athlete in athletes_data:
        ranks_list = []
        categories = athlete.get('categories', [])
        for category in categories:
            ranks = category.get('ranks', [])
            for rank in ranks:
                if rank in [None, '-','']:
                    rank = 'null'
                else:
                    rank = int(rank)
                ranks_list.append(rank)
        player_rank_list.append(ranks_list)
    return player_rank_list

# extract "labels" from the "categories" dictionary
def extract_categories_labels(data):
    values_rank_keys = []
    categories_data = data.get('categories', [])
    for category in categories_data:
        labels = category.get('labels', [])
        values_rank_keys.extend(labels)
    return values_rank_keys

# extract 'displayNames' from the 'categories' dictionary
def extract_display_names(data):
    display_names_list = []
    categories_data = data.get('categories', [])
    for category in categories_data:
        display_names = category.get('displayNames', [])
        if display_names:
            display_names_list.extend(display_names)
    return display_names_list

# extract 'descriptions' from the 'categories' dictionary
def extract_descriptions(data):
    descriptions_list = []
    categories_data = data.get('categories', [])
    for category in categories_data:
        description = category.get('descriptions', [])
        descriptions_list.extend(description)
    return descriptions_list

def main():

    # get the current year in YYYY format
    year = datetime.now().strftime('%Y')

    # use glob to get all JSON files in the current directory
    all_files = glob('*.json')
    
    # filter files using regular expression
    regex_pattern = r'espn_(defensive_totalTackles|kicking_fieldGoalsMade|passing_passingYards|punting_grossAvgPuntYards|receiving_receivingYards|returning_kickReturnYards|rushing_rushingYards|scoring_totalPoints)_page\d+_\d+.json'
    files = [f for f in all_files if re.match(regex_pattern, f)]
    
    # print the length of the files list to test it
    print(f"Number of files matching the regular expression: {len(files)}")

    # initialize empty lists
    week_list = []
    season_type_list = []
    league_list = []
    athletes_list = []
    positions_list = []
    teams_list = []
    status_list = []
    player_statistics_list = []
    player_rank_list = []

    # initialize sets for uniqueness checks
    week_ids = set()
    season_type_ids = set()
    athlete_ids = set()
    team_ids = set()
    league_ids = set()

    # Initialize nested lists
    nested_status_list = []  
    nested_player_statistics_list = []  
    nested_player_rank_list = []  
    nested_teams_list = []  
    nested_positions_list = []  
    nested_athletes_list = []  
    
    for file in files:

        # check if the file contains the current year
        if year not in file:
            proceed = input(f"The file {file} is not from the current year {year}. Do you want to proceed? (y/n): ")
            if proceed.lower() != 'y':
                continue  # skip to the next file if user says no

        # Reset the lists for each JSON file
        status_list = []
        player_statistics_list = []
        player_rank_list = []
        teams_list = [] 
        positions_list = [] 
        athletes_list = [] 

        data = read_json(file)

        # keys to extract
        league_keys = ["id", "name"]
        athlete_keys = ["id", "uid", "guid", "type", "firstName", "lastName"]
        position_keys = ["id", "name", "abbreviation"]
        status_keys = ["id", "name"]
        team_keys = ["teamId", "teamUId", "teamName", "teamShortName"]
        season_keys = ["id", "type", "name"]
        week_keys = ["number", "startDate", "endDate", "text"]
        values_rank_keys = extract_categories_labels(data)

        # extract data
        league_data = extract_league_data(data)
        league_id = league_data.get('id', None)
        if league_id not in league_ids:
            league_list.append(list(league_data.values()))
            league_ids.add(league_id)

        # only for uniqueness checks
        # athletes_list.extend(extract_athlete_data_with_uniqueness_check(data, athlete_keys, athlete_ids))
        # teams_list.extend(extract_teams_data_with_uniqueness_check(data, team_keys, team_ids)) 
        
        athletes_list.extend(extract_athlete_data_no_uniqueness_check(data, athlete_keys))
        positions_list.extend(extract_positions_data(data, position_keys))
        status_list.extend(extract_status_data(data, status_keys))
        teams_list.extend(extract_teams_data_no_uniqueness_check(data, team_keys)) # only use for no unique checks 
        season_type_list.extend(extract_seasons_data(data, season_keys, season_type_ids))
        week_list.extend(extract_week_data(data, week_keys, week_ids))
        player_statistics_list.extend(extract_athlete_values(data))
        player_rank_list.extend(extract_athlete_ranks(data))
        display_names_list = extract_display_names(data)
        descriptions_list = extract_descriptions(data)

        # Append the lists to the nested lists at the end of each file iteration
        nested_status_list.append(status_list) 
        nested_player_statistics_list.append(player_statistics_list) 
        nested_player_rank_list.append(player_rank_list) 
        nested_teams_list.append(teams_list) 
        nested_positions_list.append(positions_list) 
        nested_athletes_list.append(athletes_list)   


#################### BEGIN: Checks and Tests ##########################
    
    ## check if the lengths of the athlete data are equal
    if len(nested_teams_list) == len(nested_athletes_list) == len(nested_positions_list) == len(nested_status_list) == len(nested_player_statistics_list) == len(nested_player_rank_list):
        print("\nAll categtory lists of nested lists are equal in length.")
        print("athletes length: ", len(nested_athletes_list))
        print("positions length: ", len(nested_positions_list))
        print("status length: ",len(nested_status_list))
        print("values length: ", len(nested_player_statistics_list))
        print("ranks length: ", len(nested_player_rank_list))
    else:
        print("\nThe category lists of nested lists are not equal in length!!")
        print("athletes length: ", len(nested_athletes_list))
        print("positions length: ", len(nested_positions_list))
        print("status length: ",len(nested_status_list))
        print("values length: ", len(nested_player_statistics_list))
        print("ranks length: ", len(nested_player_rank_list))

    ## check if the lengths of the athlete 'values' and 'ranks' data are equal to the 'labels' columns
    if len(values_rank_keys) == len(player_statistics_list[0]) == len(player_rank_list[0]) == len(display_names_list) == len(descriptions_list):
        print("\nPlayer statistics column and row lengths are equal.")
        print("# of value_rank columns: ", len(values_rank_keys))
        print("# of player statistics", len(player_statistics_list[0]))
        print("# of player ranks", len(player_rank_list[0]))
        print("# of displayNames columns: ",len(display_names_list))
        print("# of descriptions columns: ",len(descriptions_list))
    else:
        print("player statistics column and row lengths are not equal!!")

    ## check if the lenghts of the nested list of players are equal
    for i in range(len(nested_player_statistics_list)):
        print(f"\nLengths of nested lists at index {i}:")
        print(f"  nested_status_list: {len(nested_status_list[i])}")
        print(f"  nested_player_statistics_list: {len(nested_player_statistics_list[i])}")
        print(f"  nested_player_rank_list: {len(nested_player_rank_list[i])}")
        print(f"  nested_teams_list: {len(nested_teams_list[i])}")
        print(f"  nested_positions_list: {len(nested_positions_list[i])}")
        print(f"  nested_athletes_list: {len(nested_athletes_list[i])}")
        print()
    
    ## test lines: dictionary to hold all the nested lists
    nested_lists_dict = {
    'nested_status_list': nested_status_list,
    'nested_player_statistics_list': nested_player_statistics_list,
    'nested_player_rank_list': nested_player_rank_list,
    'nested_teams_list': nested_teams_list,
    'nested_positions_list': nested_positions_list,
    'nested_athletes_list': nested_athletes_list
    }
    # test lines: 
    # Iterate through each main list and print the lengths of its nested lists
    for list_name, main_list in nested_lists_dict.items():
        print(f"Checking lengths for {list_name}:")
        for i, nested_list in enumerate(main_list):
            print(f"  Length of nested list at index {i}: {len(nested_list)}")
        print()

    ### Begin: league, season, and week lists ###
    # NOTE:  append to each player list
    # NOTE:  use as foreign keys for the db

    # NOTE: no changes required
    # print("=== League List ===")
    # print(league_keys )
    # print(league_list)

    # NOTE: no changes required
    # print("\n=== Season Type List ===")
    # print(season_keys)
    # print(season_type_list)

    # NOTE: no changes required
    # print("\n=== Week List ===")
    # print(week_keys)
    # print(week_list)
    ### End: league, season, and week lists ###
 

    ### BEGIN: tests for all of the categories nested lists ###
    ## test ##
    ## NOTE: test result: correct output ##
    # NOTE: the nested..._list will caputure the team for each player
    # NOTE: either use the nested---list or the teams_list as the fk table 
    # print("\n=== Teams List ===")
    # print(team_keys) # NOTE: no change to keys required
    # print(teams_list) # NOTE: no change required and can use as fk table
    #
    # print("\n----------player teams----------:")
    # count = 0
    # for n in nested_teams_list:
    #     print('\n',len(n))
    #     count += len(n)
    #     print(n)
    # print("total player teams:", count,"\n")

    ## test ##
    ## NOTE: test result: correct output ##
    # NOTE: the nested..._list will caputure the position for each player
    # NOTE: either use the nested---list or the positions_list as the fk table 
    # print("\n=== Positions List ===")
    # print(position_keys) # NOTE: no change to keys required
    # print(positions_list) # NOTE: no change needed but will not use the nested
    #
    # print("\n----------player positions----------:")
    # count = 0
    # for n in nested_positions_list:
    #     print('\n',len(n))
    #     count += len(n)
    #     print(n)
    # print("total player positions:", count,"\n")

    ## test ##
    ## NOTE: test result: correct output ##
    # NOTE: the nested..._list caputures each player to match with the stats
    # NOTE: the expanded nested..._list will serve as the fk table
    # print("\n=== Athletes List ===")
    # print(athlete_keys) # NOTE: no change to keys required
    # print(athletes_list) # NOTE: no change needed but will not use the nested
    # 
    # print("\n----------athletes----------:")
    # count = 0
    # for n in nested_athletes_list:
    #     print('\n',len(n))
    #     count += len(n)
    #     print(n)
    # print("total number of athletes:", count,"\n")
    
    ## test ##
    ## NOTE: test result: correct output ##
    # NOTE: the nested_status_list will serve as the fk table
    # print("\n=== Status List ===")
    # print(status_keys) # NOTE: no change to keys required
    # print(status_list) # NOTE: no change needed but will not use the nested
    # print('\nplayer status length:',len(nested_status_list))
    #
    # print("\n----------players' status----------:")
    # count = 0
    # for n in nested_status_list:
    #     print('\n',len(n))
    #     count += len(n)
    #     print(n)
    # print("total players' status:", count,"\n")

    ## test ##
    ## NOTE: test result: correct output ##
    # task: create loops to caputre the lists in the correct order w/enumerate
    # task: append league, season, week, athletes, teams, status and rank lists as fk numbers
    # task: append to the beginning of the list
    # print("\n=== Player Statistics List ===")
    # print("\nplayer stats length:",len(nested_player_statistics_list))
    #
    # print("----------players' stats----------:")
    # count = 0
    # for n in nested_player_statistics_list:
    #     print('\n', len(n))
    #     count += len(n)
    #     print(n)
    # print("total players' stats:", count,'\n')
    
    ## test ##
    # NOTE: test result: correct output ##
    # NOTE: player ranks is a separate table
    # NOTE: so essentially perform do the same thing as player stats
    # print("\n=== Values Rank Keys ===")
    # print(values_rank_keys)
    # print("\n=== Player Rank List ===")
    # print(player_rank_list)
    # print("player_rank_list length:",len(player_rank_list))
    # print("\nplayer rank length:",len(nested_player_rank_list))
    #
    # print("----------player ranks----------")
    # count = 0
    # for n in nested_player_rank_list:
    #     print('\n', len(n))
    #     count += len(n)
    #     print(n)
    # print("total player ranks:", count, '\n')
    ### END: tests for all of the categories nested lists ###
    
#################### END: Checks and Tests ##########################


    ### Begin: Names ,values, and descriptions of the statistical categories ###
    # NOTE: match these column names with the nested_player_statistics_list
    # NOTE: build a table: values_rank_keys (fk) display_names_list, descriptions_list
    # print("\n=== Name of Stats List ===")
    # print(display_names_list) # NOTE: no changes required
    
    # print("\n=== Descriptions List ===")
    # print(descriptions_list) # NOTE: no changes required
    ### End: Names and descriptions of the statistical categories ###
   
if __name__ == "__main__":
    main()


