import sqlite3


def create_tables(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS player (
            player_id INTEGER PRIMARY KEY,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            player_winrate REAL DEFAULT 0
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hero (
            hero_id INTEGER PRIMARY KEY,
            hero_name TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hero_stats (
        player_id INTEGER NOT NULL,
        hero_id INTEGER NOT NULL,
        hero_winrate REAL NOT NULL,
        avg_kda REAL NOT NULL,
        avg_souls_per_minute REAL NOT NULL,
        games_played INTEGER DEFAULT 0,
        PRIMARY KEY (player_id, hero_id),
        FOREIGN KEY (player_id) REFERENCES player(player_id),
        FOREIGN KEY (hero_id) REFERENCES hero(hero_id)
    );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS match (
            match_id INTEGER PRIMARY KEY,
            match_mmr REAL NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS match_stats (
            player_id INTEGER NOT NULL,
            hero_id INTEGER NOT NULL,
            match_id INTEGER NOT NULL,
            match_kills INTEGER NOT NULL, 
            match_deaths INTEGER NOT NULL, 
            match_assists INTEGER NOT NULL,
            match_kda REAL NOT NULL, 
            souls_per_minute REAL NOT NULL,
            damage REAL NOT NULL,
            win_loss INTEGER NOT NULL, -- 1 for win, 0 for loss
            player_mmr REAL NOT NULL,
            PRIMARY KEY (player_id, hero_id, match_id),
            FOREIGN KEY (player_id) REFERENCES player(player_id),
            FOREIGN KEY (hero_id) REFERENCES hero(hero_id),
            FOREIGN KEY (match_id) REFERENCES match(match_id)
        );
    """)

    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='trigger' AND name='update_avg_kda';
    """)

    if cursor.fetchone() is None:
        cursor.execute("""
            CREATE TRIGGER update_avg_kda
            AFTER INSERT ON match_stats
            FOR EACH ROW
            BEGIN
                -- Calculate the average KDA for the player and hero based on all their matches
                UPDATE hero_stats
                SET avg_kda = (
                    SELECT AVG((CAST(match_kills AS REAL) + CAST(match_assists AS REAL)) / 
                               NULLIF(CAST(match_deaths AS REAL), 0))
                    FROM match_stats
                    WHERE match_stats.player_id = NEW.player_id
                      AND match_stats.hero_id = NEW.hero_id
                )
                WHERE hero_stats.player_id = NEW.player_id
                  AND hero_stats.hero_id = NEW.hero_id;
            END;
        """)

    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='trigger' AND name='update_match_kda';
    """)
    if cursor.fetchone() is None:
        cursor.execute("""
            CREATE TRIGGER update_match_kda
            AFTER INSERT ON match_stats
            FOR EACH ROW
            BEGIN
                UPDATE match_stats
                SET match_kda = (CAST(NEW.match_kills AS REAL) + CAST(NEW.match_assists AS REAL)) / 
                                NULLIF(CAST(NEW.match_deaths AS REAL), 0)
                WHERE match_stats.player_id = NEW.player_id
                  AND match_stats.hero_id = NEW.hero_id
                  AND match_stats.match_id = NEW.match_id;
            END;
        """)

    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='trigger' AND name='increment_games_played';
    """)
    if cursor.fetchone() is None:
        cursor.execute("""
            CREATE TRIGGER increment_games_played
            AFTER INSERT ON match_stats
            FOR EACH ROW
            BEGIN
                UPDATE hero_stats
                SET games_played = games_played + 1
                WHERE player_id = NEW.player_id
                  AND hero_id = NEW.hero_id;
            END;
        """)

    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='trigger' AND name='increment_win_loss';
    """)
    if cursor.fetchone() is None:
        cursor.execute("""
            CREATE TRIGGER increment_win_loss
            AFTER INSERT ON match_stats
            FOR EACH ROW    
            BEGIN 
                UPDATE player
                SET wins = wins + 1
                WHERE player_id = NEW.player_id
                  AND NEW.win_loss = 1;

                UPDATE player
                SET losses = losses + 1
                WHERE player_id = NEW.player_id
                  AND NEW.win_loss = 0;
            END;
        """)

    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='trigger' AND name='update_player_winrate';
    """)
    if cursor.fetchone() is None:
        cursor.execute("""
            CREATE TRIGGER update_player_winrate
            AFTER UPDATE ON player
            FOR EACH ROW 
            BEGIN 
                UPDATE player
                SET player_winrate = 
                    CAST(NEW.wins AS REAL) / 
                    NULLIF(CAST(NEW.wins AS REAL) + CAST(NEW.losses AS REAL), 0)
                WHERE player_id = NEW.player_id;
            END;
        """)


def main():
    database = 'deadlock.db'
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    create_tables(cursor)

    connection.commit()  # Commit changes to the database
    cursor.close()
    connection.close()


if __name__ == '__main__':
    main()
