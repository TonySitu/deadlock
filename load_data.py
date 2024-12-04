import sqlite3


DATA_FILE = 'data.csv'
DATABASE = 'deadlock.db'


def insert_player_info(cursor, data) -> None:
    cursor.execute("""
        INSERT INTO player (player_id) VALUES (?);
    """, (data[0]))


def insert_hero_info(cursor, data) -> None:
    cursor.execute("""
        INSERT INTO hero (hero_id, hero_name) VALUES (?, ?);
    """, (data[1], data[2]))


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

    except FileNotFoundError:
        print('File was not found')

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == '__main__':
    main()
