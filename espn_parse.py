
# parse the json data

# Task: modify the code to read multiple files
# Task: combine all of the list into a single row of data to be exported

import json

def read_json(file):
    with open(file, 'r') as f:
        return json.load(f)

def filter_data_by_keys(data, keys):
    return {k: v for k, v in data.items() if k in keys}

def extract_league_data(data):
    league_data = data.get('league', {})
    return filter_data_by_keys(league_data, ["id", "name"])

def extract_athlete_data(data, athlete_keys, athlete_ids):
    athletes_list = []
    athletes_data = data.get('athletes', [])
    for athlete in athletes_data:
        athlete_info = athlete.get('athlete', {})
        if athlete_info:
            id_tuple = tuple(athlete_info.get(key, None) for key in ['id', 'uid', 'guid'])
            if id_tuple not in athlete_ids:
                athletes_list.append(list(filter_data_by_keys(athlete_info, athlete_keys).values()))
                athlete_ids.add(id_tuple)
    return athletes_list

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

def extract_teams_data(data, team_keys, team_ids):
    teams_list = []
    athletes_data = data.get('athletes', [])
    for athlete in athletes_data:
        athlete_info = athlete.get('athlete', {})
        if athlete_info:
            team_data = {k: athlete_info.get(k, '') for k in team_keys}
            team_id = team_data.get('teamId', None)
            team_uid = team_data.get('teamUId', None)
            if team_id not in team_ids and team_uid not in team_ids:
                teams_list.append(list(team_data.values()))
                team_ids.add(team_id)
                team_ids.add(team_uid)
    return teams_list

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
    file = 'espn_passing_passingYards_page1_2022.json'
    data = read_json(file)

    # Initialize empty lists
    league_list = []
    athletes_list = []
    positions_list = []
    status_list = []
    teams_list = []
    season_type_list = []
    week_list = []
    player_statistics_list = []
    player_rank_list = []

    # Initialize sets for uniqueness checks
    team_ids = set()
    season_type_ids = set()
    athlete_ids = set()
    week_ids = set()
    league_ids = set()

    # Keys to extract
    league_keys = ["id", "name"]
    athlete_keys = ["id", "uid", "guid", "type", "firstName", "lastName"]
    position_keys = ["id", "name", "abbreviation"]
    status_keys = ["id", "name"]
    team_keys = ["teamId", "teamUId", "teamName", "teamShortName"]
    season_keys = ["id", "type", "name"]
    week_keys = ["number", "startDate", "endDate", "text"]
    values_rank_keys = extract_categories_labels(data)

    # Extract data
    league_data = extract_league_data(data)
    league_id = league_data.get('id', None)
    if league_id not in league_ids:
        league_list.append(list(league_data.values()))
        league_ids.add(league_id)

    athletes_list.extend(extract_athlete_data(data, athlete_keys, athlete_ids))
    positions_list.extend(extract_positions_data(data, position_keys))
    status_list.extend(extract_status_data(data, status_keys))
    teams_list.extend(extract_teams_data(data, team_keys, team_ids))
    season_type_list.extend(extract_seasons_data(data, season_keys, season_type_ids))
    week_list.extend(extract_week_data(data, week_keys, week_ids))
    player_statistics_list.extend(extract_athlete_values(data))
    player_rank_list.extend(extract_athlete_ranks(data))
    display_names_list = extract_display_names(data)
    descriptions_list = extract_descriptions(data)
      
    # check to ensure NFL team list is correct
    if len(teams_list) == 32:
        print("Length of teams list is correct: ", len(teams_list))
    else:
        print("Number of teams imported is not correct")

    # Check if the lengths of the athlete data are equal
    if len(athletes_list) == len(positions_list) == len(status_list) == len(player_statistics_list) == len(player_rank_list):
        print("\nAll athlete lists are equal in length.")
        print("athletes length: ", len(athletes_list))
        print("positions length: ", len(positions_list))
        print("status length: ",len(status_list))
        print("values length: ", len(player_statistics_list))
        print("ranks length: ", len(player_rank_list))
    else:
        print("The athletes lists are not equal in length!!")

    # Check if the lengths of the athlete 'values' and 'ranks' data are equal to the 'labels' columns
    if len(values_rank_keys) == len(player_statistics_list[0]) == len(player_rank_list[0]) == len(display_names_list) == len(descriptions_list):
        print("\nPlayer statistics column and row lengths are equal.")
        print("# of value_rank columns: ", len(values_rank_keys))
        print("# of player statistics", len(player_statistics_list[0]))
        print("# of player ranks", len(player_rank_list[0]))
        print("# of displayNames columns: ",len(display_names_list))
        print("# of descriptions columns: ",len(descriptions_list))
    else:
        print("player statistics column and row lengths are not equal!!")
    
    # Output results

    print("=== League List ===")
    print(league_keys )
    print(league_list)

    print("\n=== Season Type List ===")
    print(season_keys)
    print(season_type_list)

    # print("\n=== Week List ===")
    # print(week_keys)
    # print(week_list)
    
    print("\n=== Athletes List ===")
    print(athlete_keys)
    print(athletes_list[0])
        
    print("\n=== Positions List ===")
    print(position_keys)
    print(positions_list[0])
    
    print("\n=== Status List ===")
    print(status_keys)
    print(status_list)
    
    print("\n=== Teams List ===")
    print(team_keys)
    print(teams_list[0])

    # print("\n=== Player Statistics List ===")
    # print(player_statistics_list[2])
    
    # print("\n=== Player Rank List ===")
    # print(player_rank_list[2])

    # print("\n=== Values Rank Keys ===")
    # print(values_rank_keys)

    # print("\n=== Display Names List ===")
    # print(display_names_list)
    
    # print("\n=== Descriptions List ===")
    # print(descriptions_list)
   
if __name__ == "__main__":
    main()


