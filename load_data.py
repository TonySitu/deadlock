import sqlite3

DATA_FILE = 'data.csv'
DATABASE = 'deadlock.db'


def insert_player_info(cursor, data) -> None:
    cursor.execute("""
        INSERT OR IGNORE INTO player (player_id) VALUES (?);
    """, (data[0],))


def insert_hero_info(cursor, data) -> None:
    cursor.execute("""
        INSERT OR IGNORE INTO hero (hero_id, hero_name) VALUES (?, ?);
    """, (data[1], data[2],))


def insert_match_stats_info(cursor, data) -> None:
    cursor.execute("""
        INSERT OR IGNORE INTO match_stats (
            player_id,
            hero_id,
            match_id,
            match_mmr,
            match_kills,
            match_deaths,
            match_assists,
            match_souls_per_minute,
            damage,
            win_loss
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        data[0], data[1], data[3], data[4], data[8], data[9], data[10], data[5], data[6], data[7],))


def insert_hero_stats(cursor, data) -> None:
    cursor.execute("""
            INSERT OR IGNORE INTO hero_stats (player_id, hero_id) VALUES (?, ?);
        """, (data[0], data[1],))


def main():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    try:
        with open(DATA_FILE) as file:
            lines = file.readlines()
            header_skipped = lines[1:]
            for line in header_skipped:
                separated_values = [value.strip() for value in line.split(',')]
                insert_player_info(cursor, separated_values)
                insert_hero_info(cursor, separated_values)
                insert_hero_stats(cursor, separated_values)
                insert_match_stats_info(cursor, separated_values)

    except FileNotFoundError:
        print('File was not found')

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == '__main__':
    main()
