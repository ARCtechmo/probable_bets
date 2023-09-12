
## This program pulls the data from the APIs ###
# Inspect --- Network ---- Fetch/XHR --- Preview / Headers

### ESPN APIs ###
# Task: download json files for each week for 2023 (wk1, wk2,...) and see if the json has weekly identifiers (do this on Tuesday)
# The APIs are headers, categories, positions, dropdown, *byathlete, teams

# NOTE: Use the "byathelete" API when pulling from the website and create .json files with the data 
#  -line 19 "atheletes" is a list of dictionaries each named named "athlete" which has the player stats
#  -line 29780 "categories" is a list of dictionaries that contain the column headers
#  -each "athlete" has a "categories" list of the individual stats (column headers)
#  -match the "categories" list starting on line 29780 with each "categories" for each "athlete" 

#  -Task: Choose a sample of players, go through each category and ensure the data matches with the ESPN website
#  -Each "athlete" has a unique identifieer called "id" and must be included along with the player name and league 

# NOTE: The "byathlete" API covers the basic player stats but not all of the splits
#  -Task: Pull data from the splits page if possible and compare
#  -I will need home vs away, indoors / outdoors, grass / turf, opponent, and outcome  

# import the libraries
import requests
import json
import csv
import random
import time



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
            "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=true&page=1&limit=50&category=specialTeams%3Apunting&sort=punting.grossAvgPuntYards%3Adesc&season=2022&seasontype=2"
    ]
    
    for index, url in enumerate(urls):

        # Randomized time delay between 1 and 6 seconds
        time_delay = random.uniform(1,6)
        time.sleep(time_delay)

        data = fetch_data(url)
    
        if data:
            if "resultSet" in data and "rowSet" in data["resultSet"]:
                write_standard_csv(data, 'nfl_data.csv')
            else:
                with open(f"nfl_stats_{index}.json", "w") as txtfile:
                    json.dump(data, txtfile, indent=4)