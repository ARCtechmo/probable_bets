
## This program pulls the data from the APIs ###
# Inspect --- Network ---- Fetch/XHR --- Preview / Headers

### ESPN APIs ###
# NOTE: The "siteapi" "byathlete" API covers the basic player stats (no API for splits and other status)
# Task: download json files for each week for 2023 (wk1, wk2,...) and see if the json has weekly identifiers (do this on Tuesday)
#  -line 19 "atheletes" is a list of dictionaries each named named "athlete" which has the player stats
#  -line 29780 "categories" is a list of dictionaries that contain the column headers
#  -each "athlete" has a "categories" list of the individual stats (column headers)
#  -match the "categories" list starting on line 29780 with each "categories" for each "athlete" 
#  -choose a sample of players, go through each category and ensure the data matches with the ESPN website
#  -each "athlete" has a unique identifieer called "id" and must be included along with the player name and league 

# Task: modify the code as necessary to download the .json files from the API

## FantasyPros projections API ## 
# https://api.fantasypros.com/public/v2/json/nfl/{season}/projections

## PFF API ##
# https://www.pff.com/api/betting/best_bets?league=nfl

# Task: update code to scrape the html (requests or beautifulsoup)

## thelines.com ## game totals and implied team totals
# https://www.thelines.com/betting/nfl/implied-team-totals/

## 4for4 Air Yards ##
# https://www.4for4.com/tools/air-yards

# import the libraries
import requests
import json
import csv
import random
import time
from urllib.parse import urlparse, parse_qs

# Make an HTTP GET request
def fetch_data(url):
    response = requests.get(url)

    # test the response
    if response.status_code == 200:
        print(f"Successfully got the data: HTTP Status Code: {response.status_code}")
    
        # load the JSON from the URL
        return response.json()
    
    # return HTTPS failed response
    else:
        print(f"Failed to get data. HTTP Status Code: {response.status_code}")
        return None
    
# dump JSON to a CSV file 
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

# parse the espn urls, name, and dump into json files
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

if __name__ == "__main__":

    # list of URLs
    urls = [
            "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=offense%3Apassing&sort=passing.passingYards%3Adesc&season=2022&seasontype=2",
            "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=offense%3Arushing&sort=rushing.rushingYards%3Adesc&season=2022&seasontype=2",
            "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=offense%3Areceiving&sort=receiving.receivingYards%3Adesc&season=2022&seasontype=2",
            "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=defense&sort=defensive.totalTackles%3Adesc&season=2022&seasontype=2",
            "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=2&limit=50&category=defense&sort=defensive.totalTackles%3Adesc&season=2022&seasontype=2",
            "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=3&limit=50&category=defense&sort=defensive.totalTackles%3Adesc&season=2022&seasontype=2",
            "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=scoring&sort=scoring.totalPoints%3Adesc&season=2022&seasontype=2",
            "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=specialTeams%3Areturning&sort=returning.kickReturnYards%3Adesc&season=2022&seasontype=2",
            "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=specialTeams%3Akicking&sort=kicking.fieldGoalsMade%3Adesc&season=2022&seasontype=2",
            "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=true&page=1&limit=50&category=specialTeams%3Apunting&sort=punting.grossAvgPuntYards%3Adesc&season=2022&seasontype=2",

            ]
    
    # loop through the urls
    for url in urls:

        # Randomized time delay between 1 and 6 seconds
        # fetch the urls and assign to a variable        
        time_delay = random.uniform(1,3)
        time.sleep(time_delay)
        data = fetch_data(url)

        # test urls string splicing without fetching
        # data = urls

        if data:
            if 'espn' in url:
                json_file_name = parse_espn_url(url)
                if json_file_name:
                    with open(json_file_name, "w") as txtfile:
                        json.dump(data, txtfile, indent=4)
        
        # elif "resultSet" in data and "rowSet" in data["resultSet"]:
        #     write_standard_csv(data, 'nfl_data.csv')