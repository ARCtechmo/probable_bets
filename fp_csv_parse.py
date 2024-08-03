import os
import pandas as pd
import re
import glob
from database import create_connection
from fp_parse4 import get_team_id

def get_all_athletes(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, firstName, lastName FROM Athletes")
    athletes = cur.fetchall()
    return athletes

def normalize_name(name):
    if not isinstance(name, str):
        return '', ''
    
    suffixes = ['Jr', 'Sr', 'II', 'III', 'IV', 'V']
    name_parts = name.lower().replace('.', '').replace(',', '').split()
    name_parts = [part for part in name_parts if part not in suffixes]
    
    if len(name_parts) == 1:
        first_name = name_parts[0]
        last_name = ''
    elif len(name_parts) >= 2:
        first_name = name_parts[0]
        last_name = name_parts[-1]
    else:
        first_name, last_name = '', ''
    
    return first_name, last_name

def extract_data(file_path):
    df = pd.read_csv(file_path)
    return df

def extract_player_names(df):
    player_names = df['Player'].tolist()
    return player_names

def match_athlete_ids(athletes, player_names):
    matched_data = []
    for player in player_names:
        first_name, last_name = normalize_name(player)
        athlete_id = None
        for athlete in athletes:
            if athlete[1].lower() == first_name and athlete[2].lower() == last_name:
                athlete_id = athlete[0]
                break
        matched_data.append((player, athlete_id))
    return matched_data

def prepare_data(df, athletes, position_abbr, conn):
    player_names = extract_player_names(df)
    matched_data = match_athlete_ids(athletes, player_names)
    data_array = df.to_dict(orient='records')
    
    for i, record in enumerate(data_array):
        player, athlete_id = matched_data[i]
        if player and isinstance(player, str):
            team_short_name = player.split(' ')[-1].strip('()')
            team_id = get_team_id(conn, team_short_name)
        else:
            team_id = None
        
        record['Player'] = athlete_id
        record['Team'] = team_id
    
    return data_array

# Define columns for each position
columns_dict = {
    'WR': ['Rank', 'Player', 'REC', 'TGT', 'YDS', 'Y/R', 'LG', '20+', 'TD', 'ATT', 'YDS.1', 'TD.1', 'FL', 'G', 'FPTS', 'FPTS/G', 'ROST'],
    'TE': ['Rank', 'Player', 'REC', 'TGT', 'YDS', 'Y/R', 'LG', '20+', 'TD', 'ATT', 'YDS.1', 'TD.1', 'FL', 'G', 'FPTS', 'FPTS/G', 'ROST'],
    'RB': ['Rank', 'Player', 'ATT', 'YDS', 'Y/A', 'LG', '20+', 'TD', 'REC', 'TGT', 'YDS.1', 'Y/R', 'TD.1', 'FL', 'G', 'FPTS', 'FPTS/G', 'ROST'],
    'QB': ['Rank', 'Player', 'CMP', 'ATT', 'PCT', 'YDS', 'Y/A', 'TD', 'INT', 'SACK', 'YDS.1', 'TD.1', 'FL', 'G', 'FPTS', 'FPTS/G', 'ROST'],
    'LB': ['Rank', 'Player', 'TACKLE', 'ASSIST', 'SACK', 'PD', 'INT', 'FF', 'FR', 'DEF TD', 'G', 'FPTS', 'FPTS/G', 'ROST'],
    'K': ['Rank', 'Player', 'FGM', 'FGA', 'PCT', 'EPM', 'EPA', 'PCT.1', 'G', 'FPTS', 'FPTS/G', 'ROST'],
    'DST': ['Rank', 'Player', 'SACK', 'INT', 'FR', 'TD', 'SFTY', 'SPC TD', 'G', 'FPTS', 'FPTS/G', 'ROST'],
    'DL': ['Rank', 'Player', 'TACKLE', 'ASSIST', 'SACK', 'PD', 'INT', 'FF', 'FR', 'DEF TD', 'G', 'FPTS', 'FPTS/G', 'ROST'],
    'DB': ['Rank', 'Player', 'TACKLE', 'ASSIST', 'SACK', 'PD', 'INT', 'FF', 'FR', 'DEF TD', 'G', 'FPTS', 'FPTS/G', 'ROST']
}

# Define a pattern for each file type
file_patterns = {
    'WR': re.compile(r'FantasyPros_Statistics_WR_\d+_wk\d+\.csv'),
    'TE': re.compile(r'FantasyPros_Statistics_TE_\d+_wk\d+\.csv'),
    'RB': re.compile(r'FantasyPros_Statistics_RB_\d+_wk\d+\.csv'),
    'QB': re.compile(r'FantasyPros_Statistics_QB_\d+_wk\d+\.csv'),
    'LB': re.compile(r'FantasyPros_Statistics_LB_\d+_wk\d+\.csv'),
    'K': re.compile(r'FantasyPros_Statistics_K_\d+_wk\d+\.csv'),
    'DST': re.compile(r'FantasyPros_Statistics_DST_\d+_wk\d+\.csv'),
    'DL': re.compile(r'FantasyPros_Statistics_DL_\d+_wk\d+\.csv'),
    'DB': re.compile(r'FantasyPros_Statistics_DB_\d+_wk\d+\.csv')
}

# Function to find files that match the pattern
def find_files(pattern):
    return [file for file in glob.glob("*.csv") if pattern.match(file)]

# Create the file_paths dictionary by finding the files that match the patterns
file_paths = {}
for position, pattern in file_patterns.items():
    matched_files = find_files(pattern)
    if matched_files:
        file_paths[position] = matched_files[0]
    else:
        file_paths[position] = None

# Define new field names mapping for each position
field_mappings = {
    'WR': {
        'Rank': 'rank',
        'Player': 'player',
        'REC': 'receptions',
        'TGT': 'targets',
        'YDS': 'yards',
        'Y/R': 'yards_per_reception',
        'LG': 'longest_reception',
        '20+': 'receptions_20_plus',
        'TD': 'touchdowns',
        'ATT': 'attempts',
        'YDS.1': 'rushing_yards',
        'TD.1': 'rushing_touchdowns',
        'FL': 'fumbles_lost',
        'G': 'games',
        'FPTS': 'fantasy_points',
        'FPTS/G': 'fantasy_points_per_game',
        'ROST': 'roster_percentage'
    },
    'TE': {
        'Rank': 'rank',
        'Player': 'player',
        'REC': 'receptions',
        'TGT': 'targets',
        'YDS': 'yards',
        'Y/R': 'yards_per_reception',
        'LG': 'longest_reception',
        '20+': 'receptions_20_plus',
        'TD': 'touchdowns',
        'ATT': 'attempts',
        'YDS.1': 'rushing_yards',
        'TD.1': 'rushing_touchdowns',
        'FL': 'fumbles_lost',
        'G': 'games',
        'FPTS': 'fantasy_points',
        'FPTS/G': 'fantasy_points_per_game',
        'ROST': 'roster_percentage'
    },
    'RB': {
        'Rank': 'rank',
        'Player': 'player',
        'ATT': 'attempts',
        'YDS': 'yards',
        'Y/A': 'yards_per_attempt',
        'LG': 'longest_run',
        '20+': 'runs_20_plus',
        'TD': 'touchdowns',
        'REC': 'receptions',
        'TGT': 'targets',
        'YDS.1': 'receiving_yards',
        'Y/R': 'yards_per_reception',
        'TD.1': 'receiving_touchdowns',
        'FL': 'fumbles_lost',
        'G': 'games',
        'FPTS': 'fantasy_points',
        'FPTS/G': 'fantasy_points_per_game',
        'ROST': 'roster_percentage'
    },
    'QB': {
        'Rank': 'rank',
        'Player': 'player',
        'CMP': 'completions',
        'ATT': 'attempts',
        'PCT': 'completion_percentage',
        'YDS': 'yards',
        'Y/A': 'yards_per_attempt',
        'TD': 'touchdowns',
        'INT': 'interceptions',
        'SACK': 'sacks',
        'YDS.1': 'rushing_yards',
        'TD.1': 'rushing_touchdowns',
        'FL': 'fumbles_lost',
        'G': 'games',
        'FPTS': 'fantasy_points',
        'FPTS/G': 'fantasy_points_per_game',
        'ROST': 'roster_percentage'
    },
    'LB': {
        'Rank': 'rank',
        'Player': 'player',
        'TACKLE': 'tackles',
        'ASSIST': 'assists',
        'SACK': 'sacks',
        'PD': 'passes_defended',
        'INT': 'interceptions',
        'FF': 'forced_fumbles',
        'FR': 'fumble_recoveries',
        'DEF TD': 'defensive_touchdowns',
        'G': 'games',
        'FPTS': 'fantasy_points',
        'FPTS/G': 'fantasy_points_per_game',
        'ROST': 'roster_percentage'
    },
    'K': {
        'Rank': 'rank',
        'Player': 'player',
        'FGM': 'field_goals_made',
        'FGA': 'field_goals_attempted',
        'PCT': 'field_goal_percentage',
        'EPM': 'extra_points_made',
        'EPA': 'extra_points_attempted',
        'PCT.1': 'extra_point_percentage',
        'G': 'games',
        'FPTS': 'fantasy_points',
        'FPTS/G': 'fantasy_points_per_game',
        'ROST': 'roster_percentage'
    },
    'DST': {
        'Rank': 'rank',
        'Player': 'team',
        'SACK': 'sacks',
        'INT': 'interceptions',
        'FR': 'fumble_recoveries',
        'TD': 'touchdowns',
        'SFTY': 'safeties',
        'SPC TD': 'special_teams_touchdowns',
        'G': 'games',
        'FPTS': 'fantasy_points',
        'FPTS/G': 'fantasy_points_per_game',
        'ROST': 'roster_percentage'
    },
    'DL': {
        'Rank': 'rank',
        'Player': 'player',
        'TACKLE': 'tackles',
        'ASSIST': 'assists',
        'SACK': 'sacks',
        'PD': 'passes_defended',
        'INT': 'interceptions',
        'FF': 'forced_fumbles',
        'FR': 'fumble_recoveries',
        'DEF TD': 'defensive_touchdowns',
        'G': 'games',
        'FPTS': 'fantasy_points',
        'FPTS/G': 'fantasy_points_per_game',
        'ROST': 'roster_percentage'
    },
    'DB': {
        'Rank': 'rank',
        'Player': 'player',
        'TACKLE': 'tackles',
        'ASSIST': 'assists',
        'SACK': 'sacks',
        'PD': 'passes_defended',
        'INT': 'interceptions',
        'FF': 'forced_fumbles',
        'FR': 'fumble_recoveries',
        'DEF TD': 'defensive_touchdowns',
        'G': 'games',
        'FPTS': 'fantasy_points',
        'FPTS/G': 'fantasy_points_per_game',
        'ROST': 'roster_percentage'
    }
}

def rename_fields(data, field_mapping):
    for record in data:
        for old_field, new_field in field_mapping.items():
            if old_field in record:
                record[new_field] = record.pop(old_field)
    return data

# Check if files exist
missing_files = [pos for pos, path in file_paths.items() if path is None]
if missing_files:
    print("Missing files for positions:", missing_files)
else:
    print("All files found")

# Extract and prepare data for all positions
all_data = {}
conn = create_connection()
athletes = get_all_athletes(conn)
for position, path in file_paths.items():
    if path is not None:
        df = extract_data(path)
        all_data[position] = prepare_data(df, athletes, position, conn)

# Rename fields for all positions
for position, mapping in field_mappings.items():
    if position in all_data:  # Check if position data exists
        all_data[position] = rename_fields(all_data[position], mapping)

# Display the modified data for all positions to verify
for position, data in all_data.items():
    print(f"Data for {position}:")
    print(data[:5])  # Display the first 5 records for each position

# Prepare and insert data into the database
for position, data in all_data.items():
    print(f"\nData to be inserted for position {position}:")
    for record in data:
        print(record)
        # Uncomment the following lines if you want to insert data into the database
        # if position == 'QB':
        #     insert_or_update_fantasy_pros_QB(conn, record)
        # elif position == 'RB':
        #     insert_or_update_fantasy_pros_RB(conn, record)
        # elif position == 'WR':
        #     insert_or_update_fantasy_pros_WR(conn, record)
        # elif position == 'TE':
        #     insert_or_update_fantasy_pros_TE(conn, record)
        # elif position == 'K':
        #     insert_or_update_fantasy_pros_K(conn, record)
        # elif position == 'DST':
        #     insert_or_update_fantasy_pros_Def(conn, record)

conn.close()

