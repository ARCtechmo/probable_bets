
###  This program pulls the data from  APIs ###
# Inspect --- Network ---- Fetch/XHR --- Preview / Headers
# NOTE: Store API keys in your OS as an environment variable
### NOTE: DO NOT PUT YOUR API KEY INTO THE CODE!!!! ###

## rotowire API ##
# https://www.rotowire.com/betting/nfl/tables/nfl-games.php?week={week}
# has unique id for each game: "game_id

# Task:
# updated fetch_data() function to accept headers
# make sure the espn api still pulls correctly

# task: go through the fp api and organize the information into lists

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
from math import ceil

# Initialize data variable to avoid NameError
data = None

## Task: NEW: evaluate ###
# handle_espn_data() function modified
# Dictionary to store count, limit, and total athletes fetched 
# ...for each unique "sort"
sort_data = {}

# function for randomized time delay 
def handle_random_delay(min_delay=1, max_delay=3):
    time_delay = random.uniform(min_delay,max_delay)
    time.sleep(time_delay)

# function tests  HTTP GET request
def fetch_data(url, headers=None):
    response = requests.get(url, headers=headers)

    # test the response
    try:
        # response = requests.get(url)
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

# original unmodified function 
# function parses the ESPN urls and dumps into json files
# NOTE: DOES NOT CAPUTRE EVERY URL PAGE - 
# def handle_espn_data(url):
#      data = fetch_data(url)
#      if data:
#         json_file_name = parse_espn_url(url)
#         if json_file_name:
#             with open(json_file_name, "w") as txtfile:
#                 json.dump(data, txtfile, indent=4)
#         return data

## Task: new modified function -- evaluate and test
# function parses the ESPN urls and dumps into json files
# code modifications to handle separate counts for each "sort" criteria
def handle_espn_data(url):
    data = fetch_data(url)
    count = 0
    limit = 0
    athletes_fetched = 0
    sort_param = ''

    if data:

        # Extract count, limit, and sort from the data for pagination
        count = data.get('count', 0)
        limit = data.get('limit', 0)

        # Assuming you can get the sort parameter from the data; otherwise, parse from URL
        sort_param = data.get('sort', '')  

        # Get the number of athletes fetched in this page
        athletes_fetched = len(data.get('athletes', []))

        json_file_name = parse_espn_url(url)
        if json_file_name:
            with open(json_file_name, "w") as txtfile:
                json.dump(data, txtfile, indent=4)

    return count, limit, athletes_fetched, sort_param

# function fetches .json data for pff prop bets 
def handle_pff_data(url):
    data = fetch_data(url)
    if data:
        with open('pff_prop_bets.json', "w") as txtfile:
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

# function to generate FantasyPros URLs based on the positions
def generate_fantasy_pros_urls(season, positions=None, week=None, scoring=None):
    
    # fetch API 
    base_url = f"https://api.fantasypros.com/public/v2/json/nfl/{season}/projections"
    
    # positions
    positions_list = ['QB','RB','WR','TE','K','DST'] if positions is None else positions.split(',')
    
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

# function to generate the JSON filename based on the FantasyPros URL
def generate_fantasy_pros_filename(url, season):
    query_string = urlparse(url).query
    params = parse_qs(query_string)
    position_param = params.get('position', [''])[0]
    scoring_param = params.get('scoring', [''])[0]
    
    filename_suffix = f"{position_param}_projections_{season}"
    if scoring_param:
        filename_suffix += f"_{scoring_param}"
    
    return f"fantasy_pros_{filename_suffix}.json"

# function to handle data from FantasyPros
def handle_fantasy_pros_data(season, positions=None, week=None, scoring=None):
    api_key = os.environ.get('api_key')
    if not api_key:
        print("API key is not set in environment variables.")
        return None
    
    headers = {'x-api-key': api_key}
    generated_urls = generate_fantasy_pros_urls(season, positions, week, scoring)
    if generated_urls is None:
        print("No URLs were generated.")
        return None
    
    for full_url in generated_urls:
        print(f"Fetching data for URL: {full_url}")
        response = fetch_data(full_url, headers)
        if response:
            json_file_name = generate_fantasy_pros_filename(full_url, season)
            if json_file_name:
                with open(json_file_name, "w") as txtfile:
                    json.dump(response, txtfile, indent=4)

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
            # f"https://www.pff.com/api/betting/best_bets?league=nfl",
            # f"https://www.rotowire.com/betting/nfl/tables/nfl-games.php?week={week}",
            ]
    

    # fixme: espn url api not capturing all pages
    # task: evaluate and test
    espn_urls = [
            # f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=offense%3Apassing&sort=passing.passingYards%3Adesc&season={year}&seasontype=2",
            # f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=offense%3Arushing&sort=rushing.rushingYards%3Adesc&season={year}&seasontype=2",
            # f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=offense%3Areceiving&sort=receiving.receivingYards%3Adesc&season={year}&seasontype=2",
            # f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=defense&sort=defensive.totalTackles%3Adesc&season={year}&seasontype=2",
            # f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=scoring&sort=scoring.totalPoints%3Adesc&season={year}&seasontype=2",
            # f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=specialTeams%3Areturning&sort=returning.kickReturnYards%3Adesc&season={year}&seasontype=2",
            # f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=specialTeams%3Akicking&sort=kicking.fieldGoalsMade%3Adesc&season={year}&seasontype=2",
            # f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=true&page=1&limit=50&category=specialTeams%3Apunting&sort=punting.grossAvgPuntYards%3Adesc&season={year}&seasontype=2",
        ]
    
    # TASK: evaluate and test
    # Loop through all the ESPN URLs 
    for initial_espn_url in espn_urls:
        
        # Fetch the first page to get count, limit, and sort for pagination
        count, limit, athletes_fetched, sort_param = handle_espn_data(initial_espn_url)

        # Initialize data for this sort
        sort_data[sort_param] = {'count': count, 'limit': limit, 'total_athletes_fetched': 0}

        # Update total_athletes_fetched for this sort
        sort_data[sort_param]['total_athletes_fetched'] += athletes_fetched

        # Calculate the total number of pages
        total_pages = ceil(count / limit)

        # Loop through all the pages
        # Start from page 2 as we have already fetched page 1
        for page in range(2, total_pages + 1):  

            # Modify the URL for each page
            espn_url = initial_espn_url.replace("page=1", f"page={page}")

            # Fetch the data for each page
            _, _, athletes_fetched, _ = handle_espn_data(espn_url)


            # Update total_athletes_fetched for this sort
            sort_data[sort_param]['total_athletes_fetched'] += athletes_fetched

        # Verify if the total number of athletes fetched matches 
        # ...the count for this sort
        if sort_data[sort_param]['total_athletes_fetched'] == sort_data[sort_param]['count']:
            print(f"Successfully fetched all athletes for sort: {sort_param}.")

        else:
            print(f"Data might be incomplete for sort: {sort_param}. \
                  Total athletes fetched: {sort_data[sort_param]['total_athletes_fetched']}, \
                  expected: {sort_data[sort_param]['count']}.")


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
