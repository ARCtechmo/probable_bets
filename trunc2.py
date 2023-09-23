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
    current_season_data = data.get('currentSeason', {})
    season_type_data = current_season_data.get('type', {})
    type_id_tuple = tuple(season_type_data.get(k, None) for k in season_keys)
    if type_id_tuple not in season_type_ids:
        season_type_list.append(list(filter_data_by_keys(season_type_data, season_keys).values()))
        season_type_ids.add(type_id_tuple)
    return season_type_list

def extract_week_data(data, week_keys, week_numbers):
    week_list = []
    current_season_data = data.get('currentSeason', {})
    week_data = current_season_data.get('type', {}).get('week', {})
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
    athlete_ids = set()
    team_ids = set()
    week_numbers = set()
    season_type_ids = set()

    # Keys to extract
    league_keys = ["id", "name"]
    athlete_keys = ["id", "uid", "guid", "type", "firstName", "lastName"]
    position_keys = ["id", "name", "abbreviation"]
    status_keys = ["id", "name"]
    team_keys = ["teamId", "teamUId", "teamName", "teamShortName"]
    season_keys = ["id", "type", "name"]
    week_keys = ["number", "startDate", "endDate", "text"]

    # Extract data
    league_list.append(list(extract_league_data(data).values()))
    athletes_list.extend(extract_athlete_data(data, athlete_keys, athlete_ids))
    positions_list.extend(extract_positions_data(data, position_keys))
    status_list.extend(extract_status_data(data, status_keys))
    teams_list.extend(extract_teams_data(data, team_keys, team_ids))
    season_type_list.extend(extract_seasons_data(data, season_keys, season_type_ids))
    week_list.extend(extract_week_data(data, week_keys, week_numbers))

    # Output results
    # print("=== League List ===")
    # print(league_keys )
    # print(league_list)
    
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
    
    # print("\n=== Season Type List ===")
    # print(season_keys)
    # print(season_type_list)
    
    # print("\n=== Week List ===")
    # print(week_keys)
    # print(week_list)
   
if __name__ == "__main__":
    main()
