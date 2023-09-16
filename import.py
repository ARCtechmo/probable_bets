
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

# Task: update code to scrape the html (requests or beautifulsoup)
## thelines.com ## game totals and implied team totals
# https://www.thelines.com/betting/nfl/implied-team-totals/

# Task: update code to scrape the html (requests or beautifulsoup)
## 4for4 Air Yards ##
# https://www.4for4.com/tools/air-yards

# import the libraries
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import json
import csv
import random
import time
from urllib.parse import urlparse, parse_qs
from datetime import datetime 

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
        f"https://www.thelines.com/betting/nfl/implied-team-totals/"
        ]


# Initialize data variable to avoid NameError
data = None

# Prompt the user to enter a year and use the current year if the input is blank
# Ensure valid year input
try:
    user_input = input("Please enter the year you want to fetch data for (hit Enter for current year): ")
    year = user_input if user_input else str(datetime.now().year)
except ValueError:
    print("Invalid year entered. Using current year instead.")
    year = datetime.now().year

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

# function tests HTTP requests for the html
def fetch_html(url):

    # test the response
    try:
        session = HTMLSession()
        response = session.get(url)
        print(f"Successfully retrieved {url}:")
        return response.text
    
    # capture exception 
    except Exception as e:
        print(f"Failed to retrieve {url}. Error {e}")
        return None
    
# function to dump JSON to a CSV file 
def write_standard_csv(data,file_name):

    # Open or create a .csv file to write to
    with open(file_name,'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write header to CSV file
        headers = data["resultSet"]["headers"]
        csv_writer.writerow(headers)
        
        # Write data to CSV file
        for player_data in data["resultSet"]["rowSet"]:
                csv_writer.writerow(player_data)

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

# function fetches .json data for pff prop bets 
def handle_pff_data(url):
    data = fetch_data(url)
    if data:
        with open('pff_prop_bets', "w") as txtfile:
            json.dump(data, txtfile, indent=4)

# function feteches html data from thelines website
def handle_thelines_data(url):
    html_content = fetch_html(url)
    if html_content:
        parse_thelines_html(html_content)
        save_html_to_txt(html_content, "thelines_page")

# function saves HTML to a .txt file
def save_html_to_txt(html_content, filename):
    with open(f"{filename}.txt", "w", encoding='utf-8') as txtfile:
        txtfile.write(html_content)

# function parses html from 'thelines' website
def parse_thelines_html(html_content):

    # Initialize BeautifulSoup object
    soup = BeautifulSoup(html_content, 'lxml')
    title = soup.title.string if soup.title else "No title found"
    print(f"Page Title: {title}")

# main loop
if __name__ == "__main__":
    
    # loop through the urls and fetch the data
    for url in urls:

        # execute time delay
        handle_random_delay()

        if 'espn' in url:
            handle_espn_data(url)

        elif 'pff' in url:
            handle_pff_data(url)

        elif 'thelines' in url:
            handle_thelines_data(url)