
###  This program pulls the data from  APIs ###
# Inspect --- Network ---- Fetch/XHR --- Preview / Headers
# NOTE: Store API keys in your OS as an environment variable
### NOTE: DO NOT PUT YOUR API KEY INTO THE CODE!!!! ###

## rotowire API ##
# https://www.rotowire.com/betting/nfl/tables/nfl-games.php?week={week}
# has unique id for each game: "game_id



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

# initialize data variable to avoid NameError
# initialize sort_data dictionary
# dict stores count, limit, and total athletes fetched for each unique "sort"
data = None

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

# function parses the ESPN urls and dumps into json files
# code modifications to handle separate counts for each "sort" criteria
def handle_espn_data(url, remaining_athletes=None):
    data = fetch_data(url)
    count = 0
    limit = 0
    athletes_fetched = 0
    sort_param = ''

    if data:

        # Debug: print out what the data looks like
        print(f"Debug: Data keys available: {data.keys()}")

        # Extract count, limit, and sort from the data for pagination
        # count = data.get('count', 0)
        # limit = data.get('limit', 0)
        count = data.get('pagination', {}).get('count', 0)
        limit = data.get('pagination', {}).get('limit', 0)

        # Debug: Print extracted values
        print(f"Debug: Extracted count: {count}, limit: {limit}")

        # assuming you can get the sort parameter from the data; otherwise, parse from URL
        sort_param = data.get('sort', '')  

        athletes = data.get('athletes', [])


        # If remaining_athletes is specified, trim the list to that size
        if remaining_athletes is not None:
            athletes = athletes[:remaining_athletes]

        # get the number of athletes fetched in this page
        # athletes_fetched = len(data.get('athletes', []))
        athletes_fetched = len(athletes)

        json_file_name = parse_espn_url(url)
        if json_file_name:
            with open(json_file_name, "w") as txtfile:
                json.dump(data, txtfile, indent=4)

    return count, limit, athletes_fetched, sort_param

# implement pagination in the if __name__ == "__main__" block
def handle_espn_pagination(initial_espn_url):
    count,limit, athletes_fetched, sort_param = handle_espn_data(initial_espn_url)
    
    # Debug: Print fetched values
    print(f"Debug: In handle_espn_pagination, count: {count}, limit: {limit}")
    
    if limit == 0:
        print(f"Limit is zero for URL: {initial_espn_url}. Skipping pagination.")
        return
    
    sort_data[sort_param] = {'count': count, 'limit': limit, 'total_athletes_fetched': 0}
    sort_data[sort_param]['total_athletes_fetched'] += athletes_fetched
    total_pages = ceil(count / limit)

    # Initialize remaining athletes count
    remaining_athletes = count - athletes_fetched
    print(f"Fetching {athletes_fetched} athletes for {sort_param} on page 1")  
  
    for page in range(2, total_pages + 1):
        espn_url = initial_espn_url.replace("page=1", f"page={page}")

        if remaining_athletes >= limit:
            _, _, athletes_fetched, _ = handle_espn_data(espn_url)
            print(f"Fetching {athletes_fetched} athletes for {sort_param} on page {page}")  
        
        # Fetch only the remaining athletes for the last page
        else:
            _, _, athletes_fetched, _ = handle_espn_data(espn_url, remaining_athletes)
            print(f"Fetching remaining {athletes_fetched} athletes for {sort_param} on page {page}")  

        sort_data[sort_param]['total_athletes_fetched'] += athletes_fetched
        
        # Update remaining athletes count
        remaining_athletes -= athletes_fetched  

# add a verification step for fetching all athletes 
def verify_data_fetched(sort_data):
    for sort_param, data in sort_data.items():
        if data['total_athletes_fetched'] == data['count']:
            print(f"Successfully fetched all athletes for sort: {sort_param}.")
        else:
            print(f"Data might be incomplete for sort: {sort_param}. \
                  Total athletes fetched: {data['total_athletes_fetched']}, \
                  expected: {data['count']}.")

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
# import path library module then use pathlib.Path() is an alternate but less secure approach
# NOTE: include this in the documentation
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

def get_year():
    try:
        user_input = input("Enter the year (hit Enter for current year): ")
        return user_input if user_input else str(datetime.now().year)
    except ValueError:
        print("Invalid year entered. Using current year instead.")
        return str(datetime.now().year)

def get_week():
    try:
        week_input = input("Enter the week: ")
        return week_input if week_input else None
    except ValueError:
        print("Invalid week entered.")
        return None
##FIXME: This an optimization issue so fix in a later version. 
    # I want to automate weekly input
    # make a list of the weeks from espn
    # match the current week to the espn week list
    # format the string to a number

# TASK: Test each conditional and ensure it pulls all of the urls (especially the espn urls)
# -main loop for data fetching and user input prompt only executes when the script is run directly.
# -main loop will not get executed if import.py file is imported as a module
if __name__ == "__main__":
    year = None
    week = None
    
    # list of URLs
    pro_football_focus_url = f"https://www.pff.com/api/betting/best_bets?league=nfl"
    fantasy_pros_template_url = []
    rotowire_template_url = f"https://www.rotowire.com/betting/nfl/tables/nfl-games.php?week={week}",
    espn_template_urls = [
                f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=offense%3Apassing&sort=passing.passingYards%3Adesc&season={year}&seasontype=2",
                f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=offense%3Arushing&sort=rushing.rushingYards%3Adesc&season={year}&seasontype=2",
                f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=offense%3Areceiving&sort=receiving.receivingYards%3Adesc&season={year}&seasontype=2",
                f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=defense&sort=defensive.totalTackles%3Adesc&season={year}&seasontype=2",
                f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=scoring&sort=scoring.totalPoints%3Adesc&season={year}&seasontype=2",
                f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=specialTeams%3Areturning&sort=returning.kickReturnYards%3Adesc&season={year}&seasontype=2",
                f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=specialTeams%3Akicking&sort=kicking.fieldGoalsMade%3Adesc&season={year}&seasontype=2",
                f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=true&page=1&limit=50&category=specialTeams%3Apunting&sort=punting.grossAvgPuntYards%3Adesc&season={year}&seasontype=2"
                ]

    while True:
        user_choice = input("Would you like to download data or quit: press 1 to download data  or 'q' or 'quit' to exit the program. ")
        if user_choice.lower() in ['q' or 'Q']:
            print("Exiting the program")
            break
        
        elif user_choice == '1':
            print("Make a selection:")
            print("(1) ESPN")
            print("(2) Pro Football Focus")
            print("(3) Fantasy Pros")
            print("(4) Rotowire")
            print("Press 'q' or 'Q' to quit.")

            api_choice = input("Enter your choice: ")
            if api_choice.lower() in ['q' or 'Q']:
                print("Exiting the program")
                break
            
            elif api_choice == '1':
                year = get_year()
                espn_urls = [url_template.format(year=year) for url_template in espn_template_urls]                
                print("Fetching data from ESPN...")

                # Loop through all the ESPN URLs 
                for initial_espn_url in espn_urls:
                    handle_espn_pagination(initial_espn_url)

                    # Verify the data
                    verify_data_fetched(sort_data)
            
            elif api_choice =='2':
                handle_pff_data(pro_football_focus_url)
                print("Fetching data from Pro Football Focus...")
            
            elif api_choice =='3':

                # Fetch FantasyPros data for the current year
                season = datetime.now().year
                fantasy_pros_urls = handle_fantasy_pros_data(season,week=None, scoring='STD')
                print("Fetching data from Fantasy Pros...")

                # Append FantasyPros URLs to the urls list
                if fantasy_pros_urls is not None:
                    fantasy_pros_template_url.extend(fantasy_pros_urls)
                else:
                    print("No FantasyPros URLs.")
            
            elif api_choice == '4':
                week = get_week()
                rotowire_url = rotowire_template_url.format(week=week)
                handle_rotowire_data(rotowire_url)
                print("Fetching data from Rotowire...")
            else:
                print("Invalid choice. Please try again.")
                break
        else:
            print("Invalid choice. Please try again.")
            break     

  