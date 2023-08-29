# build a simple database for demo
import sqlite3

def create_connection():
    """Create a database connection and return the connection object."""
    conn = sqlite3.connect('database.db')
    return conn

def create_table(conn, create_table_sql):
    """Create a table using the provided SQL statement."""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def main():
    # SQL statement to drop old "offense" table (optional)
    drop_old_offense_table = """ DROP TABLE IF EXISTS offense; """

    # SQL statement to create updated "offense" table
    # offense_table = """ CREATE TABLE IF NOT EXISTS offense (
    #                         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                         name TEXT NOT NULL,
    #                         team TEXT,
    #                         games_played INTEGER,
    #                         total_yards INTEGER,
    #                         total_yards_per_game REAL,
    #                         total_passing_yards INTEGER,
    #                         total_passing_yards_per_game REAL,
    #                         total_rushing_yards INTEGER,
    #                         total_rushing_yards_per_game REAL,
    #                         total_points INTEGER,
    #                         total_points_per_game REAL
    #                     ); """

    # SQL statement to create "defense" table
    # defense_table = """ CREATE TABLE IF NOT EXISTS defense (
    #                         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                         name TEXT NOT NULL,
    #                         rating INTEGER
    #                     ); """
    
    # Create a database connection
    conn = create_connection()

    # Create tables
    if conn is not None:
        # Drop the old "offense" table to create the new one
        c = conn.cursor()
        c.execute(drop_old_offense_table)

        # create_table(conn, offense_table)
        # create_table(conn, defense_table)

        # Commit changes
        conn.commit()

        # Close resources
        conn.close()
    else:
        print("Error! Cannot establish a database connection.")

if __name__ == '__main__':
    main()
