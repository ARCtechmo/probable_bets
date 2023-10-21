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
## TASK: create the remaining functions to export data to the db

if __name__ == '__main__':
    # Create a connection to the database
    conn = create_connection()

    # Create tables
    create_tables(conn)
