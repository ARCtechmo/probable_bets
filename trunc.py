### Key, Values Items to Capture ###
### ESPN JSON ###
import json


# file = 'trunc_espn.json'
file = 'espn_passing_passingYards_page1_2022.json'
# read JSON files
with open(file, 'r') as f:
    data = json.load(f)

# initialize empty lists 
league_list = []
athletes_list = []
positions_list = []
status_list = []
teams_list = []
season_type_list = [] 
player_statistics_list = []
week_list = []

# initialize sets for uniqueness checks
team_ids = set()
season_type_ids = set()
athlete_ids = set()
week_numbers = set()

# extract Key-Value pairs for 'league' and put them in a list
league_data = data.get('league', {})
if league_data:
    filtered_league_data = {k: v for k, v in league_data.items() if k not in ['slug', 'shortName']}
    league_list.append(list(filtered_league_data.values()))

# extract Key-Value pairs for 'athletes' and put them in a list
athletes_data = data.get('athletes', [])
athlete_keys = ["id", "uid", "guid", "type", "firstName", "lastName"]
position_keys = ["id", "name", "abbreviation"]
status_keys = ["id", "name"]
team_keys = ["teamId", "teamUId", "teamName", "teamShortName"]

for athlete in athletes_data:
    athlete_info = athlete.get('athlete', {})
    if athlete_info:
        id_tuple = tuple(athlete_info.get(key, None) for key in ['id', 'uid', 'guid'])

        # check for uniqueness
        if id_tuple not in athlete_ids:  
            filtered_athlete_data = {k: v for k, v in athlete_info.items() if k in athlete_keys}
            athletes_list.append(list(filtered_athlete_data.values()))

            # add to the set for future checks
            athlete_ids.add(id_tuple)  

        position_info = athlete_info.get('position', {})
        filtered_position_data = {k: v for k, v in position_info.items() if k in position_keys}
        positions_list.append(list(filtered_position_data.values()))

        status_info = athlete_info.get('status', {})
        filtered_status_data = {k: v for k, v in status_info.items() if k in status_keys}
        status_list.append(list(filtered_status_data.values()))

    # filter team information with a uniqueness check
    team_data = {k: athlete_info.get(k, '') for k in team_keys}
    team_id = team_data.get('teamId', None)
    team_uid = team_data.get('teamUId', None)

    if team_id not in team_ids and team_uid not in team_ids:
        teams_list.append(list(team_data.values()))
        team_ids.add(team_id)
        team_ids.add(team_uid)

# extract key-value pairs 
current_season_data = data.get('currentSeason', {})
season_type_data = current_season_data.get('type', {})
season_type_keys = ["id", "type", "name"]  
week_keys = ["number", "startDate", "endDate", "text"] 

# create a tuple from values of 'id', 'type', and 'name'
type_id_tuple = tuple(season_type_data.get(k, None) for k in season_type_keys)

# add to list if this particular type hasn't been added before
if type_id_tuple not in season_type_ids:
    filtered_season_type_data = {k: v for k, v in season_type_data.items() if k in season_type_keys}
    season_type_list.append(list(filtered_season_type_data.values()))
    season_type_ids.add(type_id_tuple)

# loop through 'currentSeason' to extract 'week' information
for key, value in current_season_data.items():
    if key == 'type':
        week_data = value.get('week', {})
        week_number = week_data.get('number', None)

        # check for uniqueness based on 'number'
        if week_number not in week_numbers:
            filtered_week_data = {k: v for k, v in week_data.items() if k in week_keys}

            # Modify date format: keep only the date part
            if 'startDate' in filtered_week_data:
                filtered_week_data['startDate'] = filtered_week_data['startDate'].split('T')[0]
            
            if 'endDate' in filtered_week_data:
                filtered_week_data['endDate'] = filtered_week_data['endDate'].split('T')[0]

            week_list.append(list(filtered_week_data.values()))

            # add to the set for future checks
            week_numbers.add(week_number)

# the keys will serve as column headers
league_columns = [k for k in league_data.keys() if k not in ['slug', 'shortName']]
athletes_columns = athlete_keys
positions_columns = position_keys
status_columns = status_keys
week_columns = week_keys


# Print the column headers and the lists
# print(f"League Foreign Key Table Columns: {league_columns}")
# print(f"Athletes Foreign Key Table Columns: {athletes_columns}")
# print(f"Positions Foreign Key Table Columns: {positions_columns}")
# print(f"Player Status Foreign Key Table Columns: {status_columns}")
# print(f"Teams Foreign Key Table Columns: {team_keys}")
# print(f"Season Type Foreign Key Table Columns: {season_type_keys}")
# print(f"Week Columns: {week_columns}")

# print(f"League Foreign Key Data (Values): {league_list}")
# print(f"Athletes Foreign Key Data (Values): {athletes_list}")
# print(f"Positions Foreign Key Data (Values): {positions_list}")
# print(f"Status Foreign Key Data (Values): {status_list}")
# print(f"Teams Data (Values): {teams_list}")
# print(f"Season Type Data (Values): {season_type_list}")
# print(f"Week Data (Values): {week_list}")

