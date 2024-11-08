from sys import argv, exit
import sqlite3
from utils import oz_to_g


def search(search_str, mode='normal'):
    con = sqlite3.connect('self.db')
    cur = con.cursor()

    match mode:
        case 'exact':
            res = cur.execute(f"SELECT * FROM nutrition WHERE name='{search_str}'")
        case 'start':
            res = cur.execute(f"SELECT * FROM nutrition WHERE name LIKE '{search_str}%'")
        case 'normal':
            res = cur.execute(f"SELECT * FROM nutrition WHERE name LIKE '%{search_str}%'")

    return res.fetchall()



params = ["search_string", "serving_size (g)"]

if __name__ == "__main__":

    search_str = ''
    serving_size = 100
    mode = 'normal'

    if len(argv) > 1:
        search_str = argv[1]

        if len(argv) > 2:
            if '--exact' in argv:
                mode = 'exact'

            if '--start' in argv:
                mode = 'start'

            if '--grams' in argv:
                idx = argv.index('--grams') + 1
                serving_size = float(argv[idx])

            if '--oz' in argv:
                idx = argv.index('--oz') + 1
                serving_size = oz_to_g(float(argv[idx]))
    else:
        usage_str = 'usage: py search.py '
        for param in params:
            usage_str += f'<{param}> '

        print(usage_str)
        exit()



    results = search(search_str, mode)

    if len(results) > 0:
        for result in results:
            cals = round(float(result[3]) * (serving_size / 100))

            print(f"{result[0]} - {result[1]} - {cals} calories in {serving_size}g")
    else:
        print("No results for " + search_str)