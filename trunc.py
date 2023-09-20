### Key, Values Items to Capture ###
### ESPN JSON ###
import json

# read JSON files
with open('trunc_espn.json', 'r') as f:
    data = json.load(f)

# initialize empty lists for 'league' and 'athletes'
league_list = []
athletes_list = []

# extract Key-Value pairs for 'league' and put them in a list
league_data = data.get('league', {})
if league_data:
    filtered_league_data = {k: v for k, v in league_data.items() if k not in ['slug', 'shortName']}
    league_list.append(list(filtered_league_data.values()))

# extract Key-Value pairs for 'athletes' and put them in a list
athletes_data = data.get('athletes', [])
desired_keys = ["id", "uid", "guid", "type", "firstName", "lastName"]
for athlete in athletes_data:
    athlete_info = athlete.get('athlete', {})
    if athlete_info:
        filtered_athlete_data = {k: v for k, v in athlete_info.items() if k in desired_keys}
        athletes_list.append(list(filtered_athlete_data.values()))

# the keys will serve as column headers
league_columns = [k for k in league_data.keys() if k not in ['slug', 'shortName']]
athletes_columns = desired_keys

# Print the column headers and the lists
print(f"League Foreign Key Columns (Keys): {league_columns}")
print(f"League Foreign Key Data (Values): {league_list}")

print(f"Athlete Foreign Key Table Columns (Keys): {athletes_columns}")
print(f"Athlete Foreign Key Data (Values): {athletes_list}")
