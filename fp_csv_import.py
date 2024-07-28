# this code renames the fantasypros csv files for individual player statistics
## ***IMPORTANT: Process one week at a time to avoid getting weeks mixed up ***

import os

def modify_filenames(directory):
    # Prompt user for input
    year = input("Enter the year: ")
    if not year.isdigit():
        print("Invalid input for year. Exiting.")
        return
    
    week = input("Enter the week: ")
    if not week.isdigit():
        print("Invalid input for week. Exiting.")
        return

    # Define the valid positions
    valid_positions = {"QB", "RB", "WR", "TE", "K", "DL", "LB", "DB", "DST"}

    # List all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            # Split the filename to identify the parts we need
            parts = filename.split('_')
            
            # Ensure the last part does not contain the .csv extension
            if parts[-1].endswith('.csv'):
                parts[-1] = parts[-1][:-4]

            # Debug print to check the parts
            # print(f"Processing: {filename}")
            # print(f"Parts: {parts}")

            # Check if the filename matches the expected pattern
            if (len(parts) == 5 and
                parts[0] == "FantasyPros" and
                parts[1] == "Fantasy" and
                parts[2] == "Football" and
                parts[3] == "Statistics" and
                parts[4] in valid_positions):
                
                # Reconstruct the new filename
                new_filename = f"FantasyPros_Statistics_{parts[4]}_{year}_wk{week}.csv"
                # Display the proposed new filename
                print(f"Proposed rename: {filename} -> {new_filename}")
                
                # Prompt the user to accept the change
                while True:
                    user_input = input("Accept change? (Y to accept, E to exit, C to correct): ").strip().upper()
                    if user_input == 'Y' or user_input == "":
                        # Rename the file
                        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
                        print(f"Renamed: {filename} -> {new_filename}")
                        break
                    elif user_input == 'E':
                        print("Exiting without renaming any files.")
                        return
                    elif user_input == 'C':
                        # Prompt for correct year and week
                        year = input("Enter the correct year: ")
                        if not year.isdigit():
                            print("Invalid input for year. Exiting.")
                            return
                        week = input("Enter the correct week: ")
                        if not week.isdigit():
                            print("Invalid input for week. Exiting.")
                            return
                        new_filename = f"FantasyPros_Statistics_{parts[4]}_{year}_wk{week}.csv"
                        print(f"Corrected rename: {filename} -> {new_filename}")
                    else:
                        print("Invalid input. Please enter 'Y', 'E', or 'C'.")
            else:
                pass
                #debug
                # print(f"Skipped: {filename} (unexpected format)")

# Define the directory containing the files
directory = "."

# Call the function
modify_filenames(directory)
