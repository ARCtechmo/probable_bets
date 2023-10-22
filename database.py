# build a simple database for demo
import sqlite3

def create_connection():
    """Create a database connection and return the connection object."""
    conn = sqlite3.connect('database.db')
    return conn

def create_tables(conn):
    cur = conn.cursor()
    cur.executescript(
        '''
        CREATE TABLE IF NOT EXISTS league(
        id INTEGER NOT NULL PRIMARY KEY,
        league TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS season(
        id INTEGER NOT NULL PRIMARY KEY,
        seasonType TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS athletes(
        id INTEGER NOT NULL PRIMARY KEY,
        uid INTEGER NOT NULL UNIQUE,
        guid INTEGER NOT NULL UNIQUE,
        sport TEXT NOT NULL,
        firstName TEXT NOT NULL,
        lastName TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS positions(
        id INTEGER NOT NULL PRIMARY KEY,
        position TEXT NOT NULL,
        abbr TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS teams(
        id INTEGER NOT NULL PRIMARY KEY,
        teamUid INTEGER NOT NULL UNIQUE,
        teamName TEXT NOT NULL UNIQUE,
        teamShortName TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS athleteStatus(
        id INTEGER NOT NULL PRIMARY KEY,
        status TEXT NOT NULL
        )
       
        '''
    )
    conn.commit()
    conn.close()

def insert_into_league(conn, league_data):
    cur = conn.cursor()
    for data in league_data:
        if isinstance(data, (list, tuple)) and len(data) == 2:
            id, league_name = data
            cur.execute("SELECT * FROM league WHERE id=?", (id,))
            if cur.fetchone() is None:
                cur.execute("INSERT INTO league (id, league) VALUES (?, ?)", (id, league_name))
        else:
            print(f"Skipping invalid data: {data}")
    conn.commit()

def insert_into_season(conn, season_data):
    cur = conn.cursor()
    for data in season_data:
        if isinstance(data, (list, tuple)) and len(data) == 2:
            id, season_type = data
            cur.execute("SELECT * FROM season WHERE id=?", (id,))
            if cur.fetchone() is None:
                cur.execute("INSERT INTO season (id, seasonType) VALUES (?,?)", (id, season_type))
        else:
            print(f"Skipping invalid data: {data}")
    conn.commit()

def insert_into_teams(conn, teams_data):
    cur = conn.cursor()
    for team_row in teams_data:
        if isinstance(team_row, (list, tuple)) and len(team_row) == 4:
            id, teamUID, teamName, teamShortName = team_row
            
            # check for duplicate entries based on id and teamUID
            cur.execute("SELECT * FROM teams WHERE id = ? OR teamUID = ?", (id, teamUID))
            existing_entry = cur.fetchone()
            if existing_entry is None:
                # insert new entry
                cur.execute("INSERT INTO teams (id, teamUID, teamName, teamShortName) VALUES (?, ?, ?, ?)",
                            (id, teamUID, teamName, teamShortName))
        else:
            print(f"Skipping invalid data: {team_row}")
    conn.commit()

def insert_into_positions(conn, positions_data):
    cur = conn.cursor()
    for position_row in positions_data:
        if isinstance(position_row, (list, tuple)) and len(position_row) == 3:  
            id, position, abbr = position_row
            cur.execute("SELECT * FROM positions WHERE id=?", (id,))
            if cur.fetchone() is None:
                cur.execute("INSERT INTO positions (id, position, abbr) VALUES (?, ?, ?)", (id, position, abbr))
        else:
            print(f"Skipping invalid data: {position_row}")
    conn.commit()

def insert_into_athlete_status(conn, status_data):
    cur = conn.cursor()
    for status_row in status_data:
        if isinstance(status_row, (list, tuple)) and len(status_row) == 2: 
            id, status = status_row
            cur.execute("SELECT * FROM athleteStatus WHERE id=?", (id,))
            if cur.fetchone() is None:
                cur.execute("INSERT INTO athleteStatus (id, status) VALUES (?, ?)", (id, status))
        else:
            print(f"Skipping invalid data: {status_row}")
    conn.commit()

#FIXME Fix the count discrepancy
## export_nested_athlete_list count is correct
## count in "athletes" differs from export_nested_athlete_list count
## UNIQUE CONSTRAINTS may be causing the issue 
def insert_into_athletes(conn, athletes_data):
    cur = conn.cursor()
    for athlete_row in athletes_data:
        if isinstance(athlete_row, (list, tuple)) and len(athlete_row) == 6: 
            id, uid, guid, sport, firstName, lastName = athlete_row
            cur.execute("SELECT * FROM athletes WHERE id=?", (id,))
            if cur.fetchone() is None:
                cur.execute("INSERT INTO athletes (id, uid, guid, sport, firstName, lastName) VALUES (?,?,?,?,?,?)",
                            (id, uid, guid, sport, firstName, lastName))
        else:
            print(f"Skipping invalid data: {athlete_row}")
    conn.commit()

if __name__ == '__main__':
    # Create a connection to the database
    conn = create_connection()

    # Create tables
    create_tables(conn)
