import os
import pandas as pd
import re
import glob

def extract_data(file_path, columns):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Select relevant columns that are present in the DataFrame
    existing_columns = [col for col in columns if col in df.columns]
    df = df[existing_columns]
    
    # Convert DataFrame to list of dictionaries
    data_array = df.to_dict(orient='records')
    
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
        file_paths[position] = matched_files[0]  # Assuming there's only one file per position
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

# Extract data for available positions
all_data = {}
for position, path in file_paths.items():
    if path is not None:
        all_data[position] = extract_data(path, columns_dict[position])

# Rename fields for all positions
for position, mapping in field_mappings.items():
    if position in all_data:  # Check if position data exists
        all_data[position] = rename_fields(all_data[position], mapping)

# Display the modified data for all positions to verify
for position, data in all_data.items():
    print(f"Data for {position}:")
    print(data[:5])  # Display the first 5 records for each position
