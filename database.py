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
        );

        CREATE TABLE playerStatistics(
        leagueFK INTEGER NOT NULL,
        seasonFK INTEGER NOT NULL,
        weekStart TEXT,
        weekEnd TEXT,
        week TEXT,
        playerFK INTEGER NOT NULL,
        PlayerPositionFK INTEGER NOT NULL,
        playerTeamFK INTEGER,
        playerStatusFK INTEGER,
        GamesPlayed INTEGER,
        ForcedFumbles INTEGER,
        FumblesRecovered INTEGER,
        FumblesTouchdowns INTEGER,
        Completions INTEGER,
        PassingAttempts INTEGER,
        CompletionPercentage INTEGER,
        PassingYards INTEGER,
        YardsPerPassAttempt INTEGER,
        PassingYardsPerGame INTEGER,
        LongestPass INTEGER,
        PassingTouchdowns INTEGER,
        Interceptions INTEGER,
        TotalSacks INTEGER,
        SackYardsLost INTEGER,
        TotalQBR INTEGER,
        PasserRating INTEGER,
        AdjustedQBR INTEGER,
        RushingAttempts INTEGER,
        RushingYards INTEGER,
        YardsPerRushAttempt INTEGER,
        LongRushing INTEGER,
        Yards20PlusRushingPlays INTEGER,
        RushingTouchdowns INTEGER,
        RushingYardsPerGame INTEGER,
        RushingFumbles INTEGER,
        RushingFumblesLost INTEGER,
        Rushing1stDowns INTEGER,
        Receptions INTEGER,
        ReceivingTargets INTEGER,
        ReceivingYards INTEGER,
        YardsPerReception INTEGER,
        ReceivingTouchdowns INTEGER,
        LongReception INTEGER,
        Yards20PlusReceivingPlays INTEGER,
        ReceivingYardsPerGame INTEGER,
        ReceivingFumbles INTEGER,
        ReceivingFumblesLost INTEGER,
        ReceivingYardsAfterCatch INTEGER,
        ReceivingFirstDowns INTEGER,
        SoloTackles INTEGER,
        AssistTackles INTEGER,
        TotalTackles INTEGER,
        Sacks INTEGER,
        SackYards INTEGER,
        TacklesForLoss INTEGER,
        PassesDefended INTEGER,
        LongInterception INTEGER,
        Interceptions_duplicate INTEGER,
        InterceptionYards INTEGER,
        InterceptionTouchdowns INTEGER,
        RushingTouchdowns_duplicate INTEGER,
        ReceivingTouchdowns_duplicate INTEGER,
        ReturnTouchdowns INTEGER,
        TotalTouchdowns INTEGER,
        FieldGoals INTEGER,
        KickExtraPoints INTEGER,
        TotalTwoPointConversions INTEGER,
        TotalPoints INTEGER,
        TotalPointsPerGame INTEGER,
        KickReturns INTEGER,
        KickReturnYards INTEGER,
        YardsPerKickReturn INTEGER,
        LongKickReturn INTEGER,
        KickReturnTouchdowns INTEGER,
        PuntReturns INTEGER,
        PuntReturnYards INTEGER,
        YardsPerPuntReturn INTEGER,
        LongPuntReturn INTEGER,
        PuntReturnTouchdowns INTEGER,
        PuntReturnFairCatches INTEGER,
        FieldGoalMade INTEGER,
        FieldGoalAttempts INTEGER,
        FieldGoalPercentage INTEGER,
        LongFieldGoalMade INTEGER,
        FieldGoalsMade119 INTEGER,
        FieldGoalsMade2029 INTEGER,
        FieldGoalsMade3039 INTEGER,
        FieldGoalsMade4049 INTEGER,
        FieldGoalsMade50Plus INTEGER,
        FieldGoalAttempts119 INTEGER,
        FieldGoalAttempts2029 INTEGER,
        FieldGoalAttempts3039 INTEGER,
        FieldGoalAttempts4049 INTEGER,
        FieldGoalAttempts50Plus INTEGER,
        ExtraPointsMade INTEGER,
        ExtraPointAttempts INTEGER,
        ExtraPointPercentage INTEGER,
        Punts INTEGER,
        PuntYards INTEGER,
        LongPunt INTEGER,
        GrossAveragePuntYards INTEGER,
        NetAveragePuntYards INTEGER,
        PuntsBlocked INTEGER,
        PuntsInside20 INTEGER,
        Touchbacks INTEGER,
        FairCatches INTEGER,
        PuntReturns_duplicate INTEGER,
        PuntReturnYards_duplicate INTEGER,
        AveragePuntReturnYards INTEGER,
        FOREIGN KEY(leagueFK) REFERENCES league (id) ON UPDATE CASCADE,
        FOREIGN KEY(seasonFK) REFERENCES season (id) ON UPDATE CASCADE,
        FOREIGN KEY(playerFK) REFERENCES athletes (id) ON UPDATE CASCADE,
        FOREIGN KEY(PlayerPositionFK) REFERENCES positions (id) ON UPDATE CASCADE,
        FOREIGN KEY(playerTeamFK) REFERENCES teams (id) ON UPDATE CASCADE,
        FOREIGN KEY(playerStatusFK) REFERENCES athleteStatus (id) ON UPDATE CASCADE
        );

        CREATE TABLE playerRanks(
        leagueFK INTEGER NOT NULL,
        seasonFK INTEGER NOT NULL,
        weekStart TEXT,
        weekEnd TEXT,
        week TEXT,
        playerFK INTEGER NOT NULL,
        PlayerPositionFK INTEGER NOT NULL,
        playerTeamFK INTEGER,
        playerStatusFK INTEGER,
        GamesPlayed INTEGER,
        ForcedFumbles INTEGER,
        FumblesRecovered INTEGER,
        FumblesTouchdowns INTEGER,
        Completions INTEGER,
        PassingAttempts INTEGER,
        CompletionPercentage INTEGER,
        PassingYards INTEGER,
        YardsPerPassAttempt INTEGER,
        PassingYardsPerGame INTEGER,
        LongestPass INTEGER,
        PassingTouchdowns INTEGER,
        Interceptions INTEGER,
        TotalSacks INTEGER,
        SackYardsLost INTEGER,
        TotalQBR INTEGER,
        PasserRating INTEGER,
        AdjustedQBR INTEGER,
        RushingAttempts INTEGER,
        RushingYards INTEGER,
        YardsPerRushAttempt INTEGER,
        LongRushing INTEGER,
        Yards20PlusRushingPlays INTEGER,
        RushingTouchdowns INTEGER,
        RushingYardsPerGame INTEGER,
        RushingFumbles INTEGER,
        RushingFumblesLost INTEGER,
        Rushing1stDowns INTEGER,
        Receptions INTEGER,
        ReceivingTargets INTEGER,
        ReceivingYards INTEGER,
        YardsPerReception INTEGER,
        ReceivingTouchdowns INTEGER,
        LongReception INTEGER,
        Yards20PlusReceivingPlays INTEGER,
        ReceivingYardsPerGame INTEGER,
        ReceivingFumbles INTEGER,
        ReceivingFumblesLost INTEGER,
        ReceivingYardsAfterCatch INTEGER,
        ReceivingFirstDowns INTEGER,
        SoloTackles INTEGER,
        AssistTackles INTEGER,
        TotalTackles INTEGER,
        Sacks INTEGER,
        SackYards INTEGER,
        TacklesForLoss INTEGER,
        PassesDefended INTEGER,
        LongInterception INTEGER,
        Interceptions_duplicate INTEGER,
        InterceptionYards INTEGER,
        InterceptionTouchdowns INTEGER,
        RushingTouchdowns_duplicate INTEGER,
        ReceivingTouchdowns_duplicate INTEGER,
        ReturnTouchdowns INTEGER,
        TotalTouchdowns INTEGER,
        FieldGoals INTEGER,
        KickExtraPoints INTEGER,
        TotalTwoPointConversions INTEGER,
        TotalPoints INTEGER,
        TotalPointsPerGame INTEGER,
        KickReturns INTEGER,
        KickReturnYards INTEGER,
        YardsPerKickReturn INTEGER,
        LongKickReturn INTEGER,
        KickReturnTouchdowns INTEGER,
        PuntReturns INTEGER,
        PuntReturnYards INTEGER,
        YardsPerPuntReturn INTEGER,
        LongPuntReturn INTEGER,
        PuntReturnTouchdowns INTEGER,
        PuntReturnFairCatches INTEGER,
        FieldGoalMade INTEGER,
        FieldGoalAttempts INTEGER,
        FieldGoalPercentage INTEGER,
        LongFieldGoalMade INTEGER,
        FieldGoalsMade119 INTEGER,
        FieldGoalsMade2029 INTEGER,
        FieldGoalsMade3039 INTEGER,
        FieldGoalsMade4049 INTEGER,
        FieldGoalsMade50Plus INTEGER,
        FieldGoalAttempts119 INTEGER,
        FieldGoalAttempts2029 INTEGER,
        FieldGoalAttempts3039 INTEGER,
        FieldGoalAttempts4049 INTEGER,
        FieldGoalAttempts50Plus INTEGER,
        ExtraPointsMade INTEGER,
        ExtraPointAttempts INTEGER,
        ExtraPointPercentage INTEGER,
        Punts INTEGER,
        PuntYards INTEGER,
        LongPunt INTEGER,
        GrossAveragePuntYards INTEGER,
        NetAveragePuntYards INTEGER,
        PuntsBlocked INTEGER,
        PuntsInside20 INTEGER,
        Touchbacks INTEGER,
        FairCatches INTEGER,
        PuntReturns_duplicate INTEGER,
        PuntReturnYards_duplicate INTEGER,
        AveragePuntReturnYards INTEGER,
        FOREIGN KEY(leagueFK) REFERENCES league (id) ON UPDATE CASCADE,
        FOREIGN KEY(seasonFK) REFERENCES season (id) ON UPDATE CASCADE,
        FOREIGN KEY(playerFK) REFERENCES athletes (id) ON UPDATE CASCADE,
        FOREIGN KEY(PlayerPositionFK) REFERENCES positions (id) ON UPDATE CASCADE,
        FOREIGN KEY(playerTeamFK) REFERENCES teams (id) ON UPDATE CASCADE,
        FOREIGN KEY(playerStatusFK) REFERENCES athleteStatus (id) ON UPDATE CASCADE
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

def insert_into_playerStatistics(conn, statistics_data):
    cur = conn.cursor()

    # fetch column names
    cur.execute("PRAGMA table_info(playerStatistics)")
    columns = cur.fetchall()
    column_names = ", ".join([column[1] for column in columns])
    for stat_row in statistics_data:
        if isinstance(stat_row, (list, tuple)) and len(stat_row) == 109: 

            # extract the specific columns from the stat_row for duplicate checking
            weekStart, weekEnd, week, playerFK = stat_row[2], stat_row[3], stat_row[4], stat_row[5]

            # check for duplicate row based on 'weekStart', 'weekEnd', 'week', 'playerFK'
            cur.execute("SELECT * FROM playerStatistics WHERE weekStart = ? AND weekEnd = ? AND week = ? AND playerFK = ?", 
                        (weekStart, weekEnd, week, playerFK))
            
            # dynamically generate the placeholders for the values
            if cur.fetchone() is None:
                placeholders = ", ".join("?" * len(stat_row))
                sql_query = f"INSERT INTO playerStatistics ({column_names}) VALUES ({placeholders})"
                cur.execute(sql_query, stat_row)
            else:
                print(f"Skipping duplicate data for playerFK={playerFK}, weekStart={weekStart}, weekEnd={weekEnd}, week={week}")
        else:    
            print(f"Skipping invalid data: {stat_row}")
    conn.commit()

def insert_into_playerRanks(conn, ranks_data):
    cur = conn.cursor()

    # Fetch column names from the 'playerRanks' table
    cur.execute("PRAGMA table_info(playerRanks)")
    columns = cur.fetchall()
    column_names = ", ".join([column[1] for column in columns])

    for rank_row in ranks_data:
        if isinstance(rank_row, (list, tuple)) and len(rank_row) == 109:  

            # Extract the specific columns from the rank_row for duplicate checking
            weekStart, weekEnd, week, playerFK = rank_row[2], rank_row[3], rank_row[4], rank_row[5]

            # Check for duplicate row based on 'weekStart', 'weekEnd', 'week', 'playerFK'
            cur.execute("SELECT * FROM playerRanks WHERE weekStart = ? AND weekEnd = ? AND week = ? AND playerFK = ?", 
                        (weekStart, weekEnd, week, playerFK))

            # Dynamically generate the placeholders for the values
            if cur.fetchone() is None:
                placeholders = ", ".join("?" * len(rank_row))
                sql_query = f"INSERT INTO playerRanks ({column_names}) VALUES ({placeholders})"
                cur.execute(sql_query, rank_row)
            else:
                print(f"Skipping duplicate data for playerFK={playerFK}, weekStart={weekStart}, weekEnd={weekEnd}, week={week}")
        else:    
            print(f"Skipping invalid data: {rank_row}")
    conn.commit()


if __name__ == '__main__':
    # Create a connection to the database
    conn = create_connection()

    # Create tables
    create_tables(conn)

