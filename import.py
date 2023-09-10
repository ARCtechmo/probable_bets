
## This program pulls the data from the APIs ###
# Inspect --- Network ---- Fetch/XHR --- Preview / Headers

## task: review APIs
# ESPN: headers, categories, positions, dropdown, *byathlete, teams

# import the libraries
import requests
import json
import csv

# Set the URLs
NFL_test_url = "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=offense%3Apassing&sort=passing.passingYards%3Adesc&season=2022&seasontype=2"

# Make an HTTP GET request
def fetch_data(url):
    response = requests.get(NFL_test_url)

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
    NFL_test_url = "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&page=1&limit=50&category=offense%3Apassing&sort=passing.passingYards%3Adesc&season=2022&seasontype=2"
    
    data = fetch_data(NFL_test_url)
    
    if data:
        if "resultSet" in data and "rowSet" in data["resultSet"]:
            write_standard_csv(data, 'nfl_data.csv')
        else:
            with open("nfl_data_alternate.json", "w") as txtfile:
                json.dump(data, txtfile, indent=4)