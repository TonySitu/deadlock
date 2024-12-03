

DATA_FILE = 'data.csv'


def main():
    try:
        with open(DATA_FILE) as file:
            lines = file.readlines()
            # header_skipped = lines[1:]
            for line in lines:
                separated_values = [value.strip() for value in line.split(',')]
                print(separated_values)
    except FileNotFoundError:
        print('File was not found')


if __name__ == '__main__':
    main()
