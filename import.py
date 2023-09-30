
## This program pulls the data from the APIs ###
# Inspect --- Network ---- Fetch/XHR --- Preview / Headers

### ESPN APIs ###
#  Task: choose a sample of players, go through each category and ensure the data matches with the ESPN website
# NOTE: The "siteapi" "byathlete" API covers the basic player stats (no API for splits and other status)
#  -"currentSeason" key (at the bottom of the jsont file) has the dates and regular season weeks
#  -line 19 "atheletes" is a list of dictionaries each named named "athlete" which has the player stats
#  -each "athlete" has a unique identifieer called "id" and must be included along with the player name and league 
#  -line 29780 "categories" is a list of dictionaries that contain the column headers
#  -match the "categories" list starting on line 29780 with each "categories" for each "athlete" 
#  -each "athlete" has a "categories" list of the individual stats (column headers)

## FantasyPros projections API ## 
# NOTE: waiting for the API key
# https://api.fantasypros.com/public/v2/json/nfl/{season}/projections

## PFF API ##
# https://www.pff.com/api/betting/best_bets?league=nfl
# has unique id for each game: "game_id"

## rotowire API ##
# https://www.rotowire.com/betting/nfl/tables/nfl-games.php?week={week}
# has unique id for each game: "game_id

## airyards CSV file only##
# NOTE: website uses unique session ids and nounces as security measures to prevent webscraping; returns empty json files
# https://apps.airyards.com/airyards.com_wopr_app/session

# Tasks:
# review json files
# decide which categores to pull and build lists
# outline your database design / tables

# import the libraries
import requests
import os
import json
import csv
import random
import time
from urllib.parse import urlparse, urlencode, parse_qs
from datetime import datetime 

# Initialize data variable to avoid NameError
data = None

# function for randomized time delay 
def handle_random_delay(min_delay=1, max_delay=3):
    time_delay = random.uniform(min_delay,max_delay)
    time.sleep(time_delay)

# function tests  HTTP GET request
def fetch_data(url):
    response = requests.get(url)

    # test the response
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Successfully retrieved {url}")
    
        # load the JSON from the URL
        return response.json()
    
    # return HTTPS failed response
    except requests.RequestException as e:
        print(f"Failed to retrieve {url}. Error: {e}")
        return None
  
# function parses and formats the ESPN urls
def parse_espn_url(url):

        # Formulate JSON filename based on URL components
        query_string = urlparse(url).query
        params = parse_qs(query_string)
        sort_param = params.get('sort', [''])[0]
        page_param = params.get('page',[''])[0]
        season_param = params.get('season', [''])[0]

        if sort_param and page_param and season_param:

            # Access the first element from list and then split at %
            # split and replace special characters
            sort_value = sort_param.split('%')[0]
            sort_value = sort_value.replace(':desc','').replace('.','_')
            return f"espn_{sort_value}_page{page_param}_{season_param}.json"
        return None

# function parses the ESPN urls and dumps into json files
def handle_espn_data(url):
     data = fetch_data(url)
     if data:
        json_file_name = parse_espn_url(url)
        if json_file_name:
            with open(json_file_name, "w") as txtfile:
                json.dump(data, txtfile, indent=4)
        return data

# function fetches .json data for pff prop bets 
def handle_pff_data(url):
    data = fetch_data(url)
    if data:
        with open('pff_prop_bets', "w") as txtfile:
            json.dump(data, txtfile, indent=4)
        return data

# function parses the rotowire url
def parse_rotowire_url(url):
    query_string = urlparse(url).query
    params = parse_qs(query_string)
    week_param = params.get('week', [''])[0]
    if week_param:
        return f"rotowire_odds_lines_week_{week_param}.json"
    return None

# function fetches .json for nfl lines
def handle_rotowire_data(url):
    data = fetch_data(url)
    if data:
        json_file_name = parse_rotowire_url(url)
        if json_file_name:
            with open(json_file_name, "w") as txtfile:
                json.dump(data, txtfile, indent=4)
        return data

# function fetches .json data for nfl air yards
def handle_airyards_data(url):
    data = fetch_data(url)
    if data:
        with open('airyards1', "w") as txtfile:
            json.dump(data, txtfile, indent=4)

    return data


# function to generate FantasyPros URLs based on the positions
def generate_fantasy_pros_urls(season, positions=None, week=None, scoring=None):
    
    # fetch API 
    base_url = f"https://api.fantasypros.com/public/v2/json/nfl/{season}/projections"
    
    # positions
    positions_list = ['QB','RB','WR','TE','K','DST','IDP','DL','LB','DB'] if positions is None else positions.split(',')
    
    # make sure that positions_str is a raw string, not a string containing quotes
    scoring_str = scoring.replace("'", "") if scoring else None
    generated_urls = []

    for position in positions_list:
        params = {'position': position}
        if week:
            params['week'] = week
        if scoring:
            params['scoring'] = scoring_str
        query_string = urlencode(params)
        full_url = f"{base_url}?{query_string}"
        generated_urls.append(full_url)

    return generated_urls

# FIXME: Need to create separate json files for each url based on position
# fantasy_pros_projections_2023_QB.json
# fantasy_pros_projections_2023_RB.json

# function to handle data from FantasyPros
def handle_fantasy_pros_data(season, positions=None, week=None, scoring=None):

    # get api key from environment variable
    api_key = os.environ.get('api_key')
    if not api_key:
        print("API key is not set in environment variables.")
        return None  
        
    # Set headers
    headers = {'x-api-key': api_key}  
    generated_urls = generate_fantasy_pros_urls(season, positions, week, scoring)

    # Check if URLs are generated
    if generated_urls is None:
        print("No URLs were generated.")
        return None
    
    for full_url in generated_urls:
        print(f"Fetching data for URL: {full_url}")
        
    # Fetch data
    response = requests.get(full_url, headers=headers)

    try:
        # Check if the request was successful
        response.raise_for_status()  
        print(f"Successfully retrieved data for season {season} from FantasyPros.")

        # Parse JSON data
        data = response.json()

        # Create unique JSON filename based on parameters
        filename_suffix = f"{season}"
        if week: filename_suffix += f"_week{week}"
        if scoring: filename_suffix += f"_{scoring}"

        # Extract the position from the URL query params
        query_string = urlparse(full_url).query
        params = parse_qs(query_string)
        position_param = params.get('position', [''])[0]
        if position_param:
            filename_suffix += f"_position_{position_param}"
        
        # Save JSON to a file
        with open(f"fantasy_pros_projections_{season}.json", "w") as txtfile:
            json.dump(data, txtfile, indent=4)

        return data
    
    except requests.RequestException as e:
        print(f"Failed to retrieve data from FantasyPros. Error: {e}")
        return None


## FIXME: add option if user wants to retrieve data from a specific api
# main loop
## Explanation of the 'if __name__ == "__main__"': ##
# -main loop only gets executed when the script is run directly

   
# -main loop for data fetching and user input prompt only executes when the script is run directly.
# -main loop will not get executed if import.py file is imported as a module
if __name__ == "__main__":

    # Prompt the user to enter a year and use the current year if the input is blank
    # Ensure valid year input
    try:
        user_input = input("Enter the year to fetch ESPN data (hit Enter for current year): ")
        year = user_input if user_input else str(datetime.now().year)
    except ValueError:
        print("Invalid year entered. Using current year instead.")
        year = datetime.now().year

    # FIXME: I want automatic weekly input
    # make a list of the weeks from espn
    # match the current week to the espn week list
    # format the string to a number
    try:
        week_input = input("Enter the week to fetch rotowire odds/lines data: ")
        week = week_input if week_input else None
        if week is None:
            print("Invalid week entered.")
            exit()
    except ValueError:
        print("Invalid week entered.")
        exit()
    
    # Fetch FantasyPros data for the current year
    season = datetime.now().year
    fantasy_pros_urls = handle_fantasy_pros_data(season,week=None, scoring='STD')
    

    # list of URLs
    urls = [
            # f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=offense%3Apassing&sort=passing.passingYards%3Adesc&season={year}&seasontype=2",
            # f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=offense%3Arushing&sort=rushing.rushingYards%3Adesc&season={year}&seasontype=2",
            # f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=offense%3Areceiving&sort=receiving.receivingYards%3Adesc&season={year}&seasontype=2",
            # f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=defense&sort=defensive.totalTackles%3Adesc&season={year}&seasontype=2",
            # f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=2&limit=50&category=defense&sort=defensive.totalTackles%3Adesc&season={year}&seasontype=2",
            # f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=3&limit=50&category=defense&sort=defensive.totalTackles%3Adesc&season={year}&seasontype=2",
            # f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=scoring&sort=scoring.totalPoints%3Adesc&season={year}&seasontype=2",
            # f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=specialTeams%3Areturning&sort=returning.kickReturnYards%3Adesc&season={year}&seasontype=2",
            # f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=specialTeams%3Akicking&sort=kicking.fieldGoalsMade%3Adesc&season={year}&seasontype=2",
            # f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=true&page=1&limit=50&category=specialTeams%3Apunting&sort=punting.grossAvgPuntYards%3Adesc&season={year}&seasontype=2",
            # f"https://www.pff.com/api/betting/best_bets?league=nfl",
            # f"https://www.rotowire.com/betting/nfl/tables/nfl-games.php?week={week}",
            ]
    
    # Append FantasyPros URLs to the urls list
    if fantasy_pros_urls is not None:
        urls.extend(fantasy_pros_urls)
    else:
        print("No FantasyPros URLs.")


    # loop through the urls and fetch the data
    for url in urls:

        # execute time delay
        handle_random_delay()

        if 'espn' in url:
            handle_espn_data(url)

        elif 'pff' in url:
            handle_pff_data(url)
        
        elif 'rotowire' in url:
            handle_rotowire_data(url)

        elif 'airyards' in url:
            handle_airyards_data(url)

