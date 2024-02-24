# construct the database
import sqlite3
import hashlib

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

        CREATE TABLE IF NOT EXISTS playerStatistics(
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
        InterceptionsDefense INTEGER,
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
        FieldGoalsMade1_19 INTEGER,
        FieldGoalsMade20_29 INTEGER,
        FieldGoalsMade30_39 INTEGER,
        FieldGoalsMade40_49 INTEGER,
        FieldGoalsMade50Plus INTEGER,
        FieldGoalAttempts1_19 INTEGER,
        FieldGoalAttempts20_29 INTEGER,
        FieldGoalAttempts30_39 INTEGER,
        FieldGoalAttempts40_49 INTEGER,
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
        PuntsReturned INTEGER,
        PuntsReturnedYards INTEGER,
        AveragePuntReturnYards INTEGER,
        row_hash TEXT NOT NULL UNIQUE,
        FOREIGN KEY(leagueFK) REFERENCES league (id) ON UPDATE CASCADE,
        FOREIGN KEY(seasonFK) REFERENCES season (id) ON UPDATE CASCADE,
        FOREIGN KEY(playerFK) REFERENCES athletes (id) ON UPDATE CASCADE,
        FOREIGN KEY(PlayerPositionFK) REFERENCES positions (id) ON UPDATE CASCADE,
        FOREIGN KEY(playerTeamFK) REFERENCES teams (id) ON UPDATE CASCADE,
        FOREIGN KEY(playerStatusFK) REFERENCES athleteStatus (id) ON UPDATE CASCADE
        );

        CREATE TABLE IF NOT EXISTS playerRanks(
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
        InterceptionsDefense INTEGER,
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
        FieldGoalsMade1_19 INTEGER,
        FieldGoalsMade20_29 INTEGER,
        FieldGoalsMade30_39 INTEGER,
        FieldGoalsMade40_49 INTEGER,
        FieldGoalsMade50Plus INTEGER,
        FieldGoalAttempts1_19 INTEGER,
        FieldGoalAttempts20_29 INTEGER,
        FieldGoalAttempts30_39 INTEGER,
        FieldGoalAttempts40_49 INTEGER,
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
        PuntsReturned INTEGER,
        PuntsReturnedYards_duplicate INTEGER,
        AveragePuntReturnYards INTEGER,
        row_hash TEXT NOT NULL UNIQUE,
        FOREIGN KEY(leagueFK) REFERENCES league (id) ON UPDATE CASCADE,
        FOREIGN KEY(seasonFK) REFERENCES season (id) ON UPDATE CASCADE,
        FOREIGN KEY(playerFK) REFERENCES athletes (id) ON UPDATE CASCADE,
        FOREIGN KEY(PlayerPositionFK) REFERENCES positions (id) ON UPDATE CASCADE,
        FOREIGN KEY(playerTeamFK) REFERENCES teams (id) ON UPDATE CASCADE,
        FOREIGN KEY(playerStatusFK) REFERENCES athleteStatus (id) ON UPDATE CASCADE
    );
        CREATE TABLE IF NOT EXISTS fantasy_pros_WR (
        season INT,
        week INT,
        player_id INT,
        position_id INT,
        team_id INT,
        points REAL,
        points_ppr REAL,
        points_half REAL,
        rec_rec REAL,
        rec_yds REAL,
        rec_tds REAL,
        rec_yds_100 REAL,
        rec_yds_200 REAL,
        scrimage_yards_100 REAL,
        scrimage_yards_200 REAL,
        rush_att REAL,
        rush_yds REAL,
        rush_tds REAL,
        rush_yds_100 REAL,
        rush_yds_200 REAL,
        fumbles REAL,
        ret_tds REAL,
        two_pt_tds REAL
    );
        CREATE TABLE IF NOT EXISTS fantasy_pros_TE (
        season INT,
        week INT,
        player_id INT,
        position_id INT,
        team_id INT,
        points REAL,
        points_ppr REAL,
        points_half REAL,
        rec_rec REAL,
        rec_yds REAL,
        rec_tds REAL,
        rec_yds_100 REAL,
        rec_yds_200 REAL,
        scrimage_yards_100 REAL,
        scrimage_yards_200 REAL,
        fumbles REAL,
        ret_tds REAL,
        two_pt_tds REAL
    );
        CREATE TABLE IF NOT EXISTS fantasy_pros_RB (
        season INT,
        week INT,
        player_id INT,
        position_id INT,
        team_id INT,
        points REAL,
        points_ppr REAL,
        points_half REAL,
        rush_att REAL,
        rush_yds REAL,
        rush_tds REAL,
        rush_yds_100 REAL,
        rush_yds_200 REAL,
        scrimage_yards_100 REAL,
        scrimage_yards_200 REAL,
        rec_rec REAL,
        rec_yds REAL,
        rec_tds REAL,
        rec_yds_100 REAL,
        rec_yds_200 REAL,
        fumbles REAL,
        ret_tds REAL,
        two_pt_tds REAL
    );

        CREATE TABLE IF NOT EXISTS fantasy_pros_QB (
        season INT,
        week INT,
        player_id INT,
        position_id INT,
        team_id INT,
        points REAL,
        points_ppr REAL,
        points_half REAL,
        pass_att REAL,
        pass_cmp REAL,
        pass_yds REAL,
        pass_tds REAL,
        pass_ints REAL,
        pass_yds_300 REAL,
        pass_yds_400 REAL,
        rush_att REAL,
        rush_yds REAL,
        rush_tds REAL,
        rush_yds_100 REAL,
        rush_yds_200 REAL,
        scrimage_yards_100 REAL,
        scrimage_yards_200 REAL,
        fumbles REAL,
        ret_tds REAL,
        two_pt_tds REAL
    );
        CREATE TABLE IF NOT EXISTS fantasy_pros_K (
        season INT,
        week INT,
        player_id INT,
        position_id INT,
        team_id INT,
        points REAL,
        points_ppr REAL,
        points_half REAL,
        fga REAL,
        fg REAL,
        xpt REAL
    );

        CREATE TABLE IF NOT EXISTS fantasy_pros_Def (
        season INT,
        week INT,
        team_id INT,
        points REAL,
        points_ppr REAL,
        points_half REAL,
        def_sack REAL,
        def_int REAL,
        def_td REAL,
        def_pa REAL,
        def_tyda REAL,
        def_safety REAL,
        def_ff REAL,
        def_fr REAL,
        def_retd REAL
    );

        CREATE TABLE IF NOT EXISTS pro_football_focus(
        props_last_updated_at DATE,
        player_id INTEGER,
        position_id INTEGER,
        team_id INTEGER,
        opponent_team_id INTEGER,
        prop_type TEXT,
        projection TEXT,
        line REAL,
        over INTEGER,
        under INTEGER,
        FOREIGN KEY (player_id) REFERENCES athletes(id),
        FOREIGN KEY (position_id) REFERENCES positions(id),
        FOREIGN KEY (team_id) REFERENCES teams(id),
        FOREIGN KEY (opponent_team_id) REFERENCES teams(id)
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

### new function to create a hash of each row ##
def generate_row_hash(row_data):
    # Create a string representation of the row data
    row_str = ''.join(map(str, row_data))

    # Generate a hash (MD5 used here for simplicity)
    return hashlib.md5(row_str.encode()).hexdigest()

# NOTE: initial testing matched results on ESPN website
## function without filters ##
def insert_into_playerStatistics(conn, stats_data):
    cur = conn.cursor()

    # fetch column names
    cur.execute("PRAGMA table_info(playerStatistics)")
    columns = cur.fetchall()

    # Assuming the last column is 'row_hash'
    column_names = ", ".join([column[1] for column in columns if column[1] != 'row_hash'])

    for stat_row in stats_data:
        # Generate a hash for the row
        row_hash = generate_row_hash(stat_row)

        # Append the row_hash to the stat_row list
        stat_row_with_hash = list(stat_row) + [row_hash]
        print("TEST insert_into_playerStatistics FUNCTION:", stat_row, row_hash)

        # Prepare your SQL INSERT statement here with the modified data
        sql_query = f"INSERT INTO playerStatistics ({column_names}, row_hash) VALUES ({', '.join(['?' for _ in range(len(stat_row_with_hash))])})"
        # cur.execute(sql_query, stat_row_with_hash)

        try:
            cur.execute(sql_query, stat_row_with_hash)
        except sqlite3.IntegrityError:
            # This catches the exception thrown by the UNIQUE constraint violation
            print(f"TEST insert_into_playerStatistics FUNCTION: Skipping duplicate row with hash: {row_hash}")

    conn.commit()

## function without filters ##
def insert_into_playerRanks(conn, ranks_data):
    cur = conn.cursor()

    # Fetch column names from the 'playerRanks' table
    cur.execute("PRAGMA table_info(playerRanks)")
    columns = cur.fetchall()

    # Assuming the last column is 'row_hash'
    column_names = ", ".join([column[1] for column in columns if column[1] != 'row_hash'])

    for rank_row in ranks_data:
        # Generate a hash for the row
        row_hash = generate_row_hash(rank_row)

        # Append the row_hash to the rank_row list
        rank_row_with_hash = list(rank_row) + [row_hash]
        print("TEST insert_into_playerRanks FUNCTION:", rank_row, row_hash)

        # Prepare your SQL INSERT statement here with the modified data
        sql_query = f"INSERT INTO playerRanks ({column_names}, row_hash) VALUES ({', '.join(['?' for _ in range(len(rank_row_with_hash))])})"
        
        try:
            cur.execute(sql_query, rank_row_with_hash)
        except sqlite3.IntegrityError:
            # This catches the exception thrown by the UNIQUE constraint violation
            print(f"TEST insert_into_playerRanks FUNCTION: Skipping duplicate row with hash: {row_hash}")

    conn.commit()

## NOTE:  ** DO NOT DELETE UNITL TESTING IS COMPLETE **
# def insert_into_playerStatistics(conn, statistics_data):
#     cur = conn.cursor()

#     # fetch column names
#     cur.execute("PRAGMA table_info(playerStatistics)")
#     columns = cur.fetchall()
#     column_names = ", ".join([column[1] for column in columns])
#     for stat_row in statistics_data:
#         if isinstance(stat_row, (list, tuple)) and len(stat_row) == 109: 

#             # extract the specific columns from the stat_row for duplicate checking
#             weekStart, weekEnd, week, playerFK = stat_row[2], stat_row[3], stat_row[4], stat_row[5]

#             # check for duplicate row based on 'weekStart', 'weekEnd', 'week', 'playerFK'
#             cur.execute("SELECT * FROM playerStatistics WHERE weekStart = ? AND weekEnd = ? AND week = ? AND playerFK = ?", 
#                         (weekStart, weekEnd, week, playerFK))
            
#             ## FIXME this section is causing some atheltes to not popualte data for certain weeks
#             # dynamically generate the placeholders for the values
#             if cur.fetchone() is None:
#                 placeholders = ", ".join("?" * len(stat_row))
#                 sql_query = f"INSERT INTO playerStatistics ({column_names}) VALUES ({placeholders})"
#                 cur.execute(sql_query, stat_row)
#             else: 
#                 print(f"TEST insert_into_playerStatistics FUNCTION: Skipping duplicate data for playerFK={playerFK}, weekStart={weekStart}, weekEnd={weekEnd}, week={week}")
#         else:    
#             print(f"TEST insert_into_playerStatistics FUNCTION: Invalid data (length mismatch), skipping: {stat_row}")
#     conn.commit()

## NOTE:  ** DO NOT DELETE UNITL TESTING IS COMPLETE **
## task: Check to ensure the same issue of certain weeks returning null data for certain players (see the above function)
# def insert_into_playerRanks(conn, ranks_data):
#     cur = conn.cursor()

#     # Fetch column names from the 'playerRanks' table
#     cur.execute("PRAGMA table_info(playerRanks)")
#     columns = cur.fetchall()
#     column_names = ", ".join([column[1] for column in columns])

#     for rank_row in ranks_data:
#         if isinstance(rank_row, (list, tuple)) and len(rank_row) == 109:  

#             # Extract the specific columns from the rank_row for duplicate checking
#             weekStart, weekEnd, week, playerFK = rank_row[2], rank_row[3], rank_row[4], rank_row[5]

#             # Check for duplicate row based on 'weekStart', 'weekEnd', 'week', 'playerFK'
#             cur.execute("SELECT * FROM playerRanks WHERE weekStart = ? AND weekEnd = ? AND week = ? AND playerFK = ?", 
#                         (weekStart, weekEnd, week, playerFK))

#             # Dynamically generate the placeholders for the values
#             if cur.fetchone() is None:
#                 placeholders = ", ".join("?" * len(rank_row))
#                 sql_query = f"INSERT INTO playerRanks ({column_names}) VALUES ({placeholders})"
#                 cur.execute(sql_query, rank_row)
#             else:
#                 print(f"TEST insert_into_playerRanks FUNCTION: Skipping duplicate data for playerFK={playerFK}, weekStart={weekStart}, weekEnd={weekEnd}, week={week}")
#         else:    
#             print(f"TEST insert_into_playerRanks FUNCTION: Skipping invalid data: {rank_row}")
#     conn.commit()
      
def insert_or_update_fantasy_pros_QB(conn, qb_data):
    cur = conn.cursor()
    for row in qb_data:
        season, week, player_id = row[0], row[1], row[2]
        
        # Check if a row exists for the same player_id and week
        cur.execute("SELECT 1 FROM fantasy_pros_QB WHERE player_id = ? AND week = ?", (player_id, week))
        exists = cur.fetchone()

        if exists:
            # Update the existing row if player_id with the same week exists
            update_columns = [column[1] for column in cur.execute("PRAGMA table_info(fantasy_pros_QB)").fetchall() if column[1] not in ['player_id', 'week', 'rowid', 'season']]
            update_statement = ", ".join([f"{col} = ?" for col in update_columns])
            update_values = row[3:]  # Excluding player_id, season, and week from the update values
            cur.execute(f"UPDATE fantasy_pros_QB SET {update_statement} WHERE player_id = ? AND week = ?", (*update_values, player_id, week))
        else:
            # Insert a new row if no matching player_id and week are found
            column_names = ", ".join([column[1] for column in cur.execute("PRAGMA table_info(fantasy_pros_QB)").fetchall() if column[1] != 'rowid'])
            placeholders = ', '.join(['?' for _ in row])
            cur.execute(f"INSERT INTO fantasy_pros_QB ({column_names}) VALUES ({placeholders})", row)

        conn.commit()

def insert_or_update_fantasy_pros_WR(conn, qb_data):
    cur = conn.cursor()
    for row in qb_data:
        season, week, player_id = row[0], row[1], row[2]
        
        # Check if a row exists for the same player_id and week
        cur.execute("SELECT 1 FROM fantasy_pros_WR WHERE player_id = ? AND week = ?", (player_id, week))
        exists = cur.fetchone()

        if exists:
            # Update the existing row if player_id with the same week exists
            update_columns = [column[1] for column in cur.execute("PRAGMA table_info(fantasy_pros_WR)").fetchall() if column[1] not in ['player_id', 'week', 'rowid', 'season']]
            update_statement = ", ".join([f"{col} = ?" for col in update_columns])
            update_values = row[3:]  # Excluding player_id, season, and week from the update values
            cur.execute(f"UPDATE fantasy_pros_WR SET {update_statement} WHERE player_id = ? AND week = ?", (*update_values, player_id, week))
        else:
            # Insert a new row if no matching player_id and week are found
            column_names = ", ".join([column[1] for column in cur.execute("PRAGMA table_info(fantasy_pros_WR)").fetchall() if column[1] != 'rowid'])
            placeholders = ', '.join(['?' for _ in row])
            cur.execute(f"INSERT INTO fantasy_pros_WR ({column_names}) VALUES ({placeholders})", row)

        conn.commit()

def insert_or_update_fantasy_pros_RB(conn, qb_data):
    cur = conn.cursor()
    for row in qb_data:
        season, week, player_id = row[0], row[1], row[2]
        
        # Check if a row exists for the same player_id and week
        cur.execute("SELECT 1 FROM fantasy_pros_RB WHERE player_id = ? AND week = ?", (player_id, week))
        exists = cur.fetchone()

        if exists:
            # Update the existing row if player_id with the same week exists
            update_columns = [column[1] for column in cur.execute("PRAGMA table_info(fantasy_pros_RB)").fetchall() if column[1] not in ['player_id', 'week', 'rowid', 'season']]
            update_statement = ", ".join([f"{col} = ?" for col in update_columns])
            update_values = row[3:]  # Excluding player_id, season, and week from the update values
            cur.execute(f"UPDATE fantasy_pros_RB SET {update_statement} WHERE player_id = ? AND week = ?", (*update_values, player_id, week))
        else:
            # Insert a new row if no matching player_id and week are found
            column_names = ", ".join([column[1] for column in cur.execute("PRAGMA table_info(fantasy_pros_RB)").fetchall() if column[1] != 'rowid'])
            placeholders = ', '.join(['?' for _ in row])
            cur.execute(f"INSERT INTO fantasy_pros_RB ({column_names}) VALUES ({placeholders})", row)

        conn.commit()

def insert_or_update_fantasy_pros_TE(conn, qb_data):
    cur = conn.cursor()
    for row in qb_data:
        season, week, player_id = row[0], row[1], row[2]
        
        # Check if a row exists for the same player_id and week
        cur.execute("SELECT 1 FROM fantasy_pros_TE WHERE player_id = ? AND week = ?", (player_id, week))
        exists = cur.fetchone()

        if exists:
            # Update the existing row if player_id with the same week exists
            update_columns = [column[1] for column in cur.execute("PRAGMA table_info(fantasy_pros_TE)").fetchall() if column[1] not in ['player_id', 'week', 'rowid', 'season']]
            update_statement = ", ".join([f"{col} = ?" for col in update_columns])
            update_values = row[3:]  # Excluding player_id, season, and week from the update values
            cur.execute(f"UPDATE fantasy_pros_TE SET {update_statement} WHERE player_id = ? AND week = ?", (*update_values, player_id, week))
        else:
            # Insert a new row if no matching player_id and week are found
            column_names = ", ".join([column[1] for column in cur.execute("PRAGMA table_info(fantasy_pros_TE)").fetchall() if column[1] != 'rowid'])
            placeholders = ', '.join(['?' for _ in row])
            cur.execute(f"INSERT INTO fantasy_pros_TE ({column_names}) VALUES ({placeholders})", row)

        conn.commit()

def insert_or_update_fantasy_pros_K(conn, qb_data):
    cur = conn.cursor()
    for row in qb_data:
        season, week, player_id = row[0], row[1], row[2]
        
        # Check if a row exists for the same player_id and week
        cur.execute("SELECT 1 FROM fantasy_pros_K WHERE player_id = ? AND week = ?", (player_id, week))
        exists = cur.fetchone()

        if exists:
            # Update the existing row if player_id with the same week exists
            update_columns = [column[1] for column in cur.execute("PRAGMA table_info(fantasy_pros_K)").fetchall() if column[1] not in ['player_id', 'week', 'rowid', 'season']]
            update_statement = ", ".join([f"{col} = ?" for col in update_columns])
            update_values = row[3:]  # Excluding player_id, season, and week from the update values
            cur.execute(f"UPDATE fantasy_pros_K SET {update_statement} WHERE player_id = ? AND week = ?", (*update_values, player_id, week))
        else:
            # Insert a new row if no matching player_id and week are found
            column_names = ", ".join([column[1] for column in cur.execute("PRAGMA table_info(fantasy_pros_K)").fetchall() if column[1] != 'rowid'])
            placeholders = ', '.join(['?' for _ in row])
            cur.execute(f"INSERT INTO fantasy_pros_K ({column_names}) VALUES ({placeholders})", row)

        conn.commit()

def insert_or_update_fantasy_pros_Def(conn, qb_data):
    cur = conn.cursor()
    for row in qb_data:
        season, week, team_id = row[0], row[1], row[2]
        
        # Check if a row exists for the same team_id and week
        cur.execute("SELECT 1 FROM fantasy_pros_Def WHERE team_id = ? AND week = ?", (team_id, week))
        exists = cur.fetchone()

        if exists:
            # Update the existing row if team_id with the same week exists
            update_columns = [column[1] for column in cur.execute("PRAGMA table_info(fantasy_pros_Def)").fetchall() if column[1] not in ['team_id', 'week', 'rowid', 'season']]
            update_statement = ", ".join([f"{col} = ?" for col in update_columns])
            update_values = row[3:]  # Excluding team_id, season, and week from the update values
            cur.execute(f"UPDATE fantasy_pros_Def SET {update_statement} WHERE team_id = ? AND week = ?", (*update_values, team_id, week))
        else:
            # Insert a new row if no matching team_id and week are found
            column_names = ", ".join([column[1] for column in cur.execute("PRAGMA table_info(fantasy_pros_Def)").fetchall() if column[1] != 'rowid'])
            placeholders = ', '.join(['?' for _ in row])
            cur.execute(f"INSERT INTO fantasy_pros_Def ({column_names}) VALUES ({placeholders})", row)

        conn.commit()

def insert_or_update_pro_football_focus(conn, pff_data):
    # Extract data from pff_data
    (props_last_updated_at, 
     player_id, position_id, team_id, opponent_team_id, 
     prop_type, projection, 
     line, over, under) = pff_data

    # Create a cursor object
    cur = conn.cursor()

    # Determine if we should check for a row with a NULL player_id
    player_id_check = "player_id IS NULL" if player_id is None else "player_id = ?"

    # Prepare the SQL query to check for an existing entry
    query = f"""
        SELECT * FROM pro_football_focus 
        WHERE {player_id_check} AND position_id = ? AND team_id = ? 
        AND opponent_team_id = ? AND prop_type = ? AND projection = ? AND line = ? 
        AND over = ? AND under = ?
    """

    # Prepare the parameters for the SQL query, excluding the player_id if it is NULL
    params = [position_id, team_id, opponent_team_id, prop_type, 
              projection, line, over, under]
    if player_id is not None:
        params.insert(0, player_id)

    # Execute the query to check for an existing entry
    cur.execute(query, params)
    existing_entry = cur.fetchone()

    # Update or insert the entry based on the existence check
    if existing_entry:
        # Only update if player_id is not NULL
        if player_id is not None:
            update_query = """
                UPDATE pro_football_focus 
                SET props_last_updated_at = ?, projection = ?, line = ?, over = ?, under = ? 
                WHERE player_id = ? AND position_id = ? AND team_id = ? 
                AND opponent_team_id = ? AND prop_type = ?
            """
            cur.execute(update_query, (props_last_updated_at, projection, line, over, under, 
                                       player_id, position_id, team_id, opponent_team_id, prop_type))
    else:
        # Insert a new entry
        insert_query = """
            INSERT INTO pro_football_focus (props_last_updated_at, player_id, position_id, team_id, opponent_team_id, prop_type, projection, line, over, under) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cur.execute(insert_query, (props_last_updated_at, player_id, position_id, team_id, opponent_team_id, 
                                   prop_type, projection, line, over, under))

    # Commit the transaction
    conn.commit()


if __name__ == '__main__':
    # Create a connection to the database
    conn = create_connection()

    # Create tables
    create_tables(conn)

