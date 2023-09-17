# unused code

######### Test Web Scraping ###########
def test_webscraping(url):
    print(requests.get(url))
    page = requests.get(url)
    text = BeautifulSoup(page.text, 'html.parser')
    print(text)
# test_webscraping('https://www.scrapethissite.com/pages/forms/')
######### Test Web Scraping ###########


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

# function saves HTML to a .txt file
def save_html_to_txt(html_content, filename):
    if html_content:
        with open(f"{filename}.txt", "w", encoding='utf-8') as txtfile:
            txtfile.write(html_content.prettify())


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


# fixme
# function feteches and parses html data from thelines website
def handle_rotocurve_data(url):
    html_content = fetch_data(url)

  # Check if HTML content was successfully fetched
    if html_content:
        # Save HTML content to 'roto.txt'
        with open("roto.txt", "w", encoding='utf-8') as txtfile:
            # Here, I'm using BeautifulSoup to prettify the HTML content
            txtfile.write(BeautifulSoup(html_content, 'html.parser').prettify())
        print("HTML content saved to 'roto.txt'")
    else:
        print("Failed to fetch HTML content from the URL.")

# function feteches and parses html data from thelines website
def handle_thelines_data(url):
    html_content = fetch_html(url)
    # html_content = requests.get(url)

    # Check if HTML content was successfully fetched
    if html_content:

        # Save the entire HTML content to a text file
        # save_html_to_txt(BeautifulSoup(html_content, 'html.parser'), "thelines_html")
        # print("Entire HTML saved to 'thelines_html.txt'")
        
        page = requests.get(url)
        text = BeautifulSoup(page.text, 'html.parser')
        print(text)

        # initiialize BeautifulSoup object
        soup = BeautifulSoup(html_content,'html.parser')

        # identify the table by its id
        table = soup.find("table", {"id": "tablepress-2617"})
        if table:

            # extract headers
            headers = [header.text for header in table.find_all("th")]
            
            # Check 1
            print("Table Headers:", headers)  

            # Initialize a list to store each row data as a dictionary
            table_data = []

            # extract rows and populate table_data list
            for row in table.find_all("tr")[1:]:
                row_data = {}
                for i, cell in enumerate(row.find_all("td")):
                    row_data[headers[i]] = cell.text
                table_data.append(row_data)
            
            # Save the table HTML content to a text file 
            save_html_to_txt(table, "table_data")
                
            # check 2 
            print("Table Data:", table_data)
            
        else:
            print("No table found.")
    else:
        print("Failed to fetch HTML content from the URL.")   