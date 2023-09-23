
# parse the json data
# tasks: create the player statsitics (write the table - see below)
# - use the lists and json "categories" dictionaries
# - don't worry about foreign keys; just create the rows as they should appear

# task
# import the entire glossary into a list that will be a table in the db.

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

     # Check if the lengths of the athlete data are equal
    if len(athletes_list) == len(positions_list) == len(status_list):
        print("All athlete lists are equal in length.")
        print("athletes length: ", len(athletes_list))
        print("positions length: ", len(positions_list))
        print("status length: ",len(status_list))
    else:
        print("The lists are not equal in length.")

    # check to ensure NFL team list is correct
    if len(teams_list) == 32:
        print("Length of teams list is correct: ", len(teams_list))
    else:
        print("Number of teams imported is not correct")
        
    # Output results

    # print("=== League List ===")
    # print(league_keys )
    # print(league_list)

    # print("\n=== Season Type List ===")
    # print(season_keys)
    # print(season_type_list)

    # print("\n=== Week List ===")
    # print(week_keys)
    # print(week_list)
    
    # print("\n=== Athletes List ===")
    # print(athlete_keys)
    # print(athletes_list)
        
    # print("\n=== Positions List ===")
    # print(position_keys)
    # print(positions_list)
    
    # print("\n=== Status List ===")
    # print(status_keys)
    # print(status_list)
    
    # print("\n=== Teams List ===")
    # print(team_keys)
    # print(teams_list)
    
    
   
if __name__ == "__main__":
    main()

## task: sketch out a table ##
# league_id, 
# year (get this from "requestedSeason": {"year": 2022,),
# seaon_type_id (get this from "requestedSeason": {"type": {id: },
# athlete_id, position_id, player_status_id, team_id,

# task: the next columns come from the "categories" dictionaries 
# "labels" are the column headers
# "GP","FF","FR","FTD"
# "CMP","ATT","CMP%","YDS","AVG","YDS/G","LNG","TD","INT","SACK","SYL","QBR","RTG","QBR"
# "CAR","YDS","AVG","LNG","BIG", "TD", "YDS/G", "FUM", "LST","FD"
# "REC","TGTS", "YDS", "AVG", "TD", "LNG", "BIG", "YDS/G", "FUM", "LST", "YAC", "FD"
# "SOLO","AST", "TOT", "SACK", "SCKYDS", "TFL", "PD", "LNG"
# "INT", "YDS", "TD"
# "RUSH", "REC", "RET", "TD", "FG", "PAT", "2PT", "PTS", "TP/G"
# "ATT", "YDS", "AVG", "LNG", "TD", "ATT", "YDS", "AVG", "LNG", "TD", "FC"
# "FGM", "FGA", "FG%", "LNG", "FGM 1-19", "FGM 20-29", "FGM 30-39", "FGM 40-49", "50+", "FGA 1-19", "FGA 20-29", "FGA 30-39", "FGA 40-49", "FGA 50+", "XPM", "XPA", "XP%"
# "PUNTS", "YDS", "LNG", "AVG", "NET", "PBLK", "IN20", "TB", "FC", "ATT", "YDS", "AVG"

# task:
# the values come from the "categories" dictionary: values and ranks 

# task add conditional checks to ensure there are no duplicate rows
# task add conditional checks for length of lists