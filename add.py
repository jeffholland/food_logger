import sqlite3
from sys import argv
from utils import oz_to_g

con = sqlite3.connect('self.db')
cur = con.cursor()

def get_unique_id():
    res = cur.execute("SELECT MAX(id) FROM nutrition")
    result = res.fetchall()[0][0]
    if result == None:
        return 1
    else:
        return result + 1

def insert_food(name, calories, protein):
    id = get_unique_id()
    cur.execute(f"INSERT INTO nutrition VALUES ({id}, '{name}', {calories}, {protein})")
    con.commit()
    

if __name__ == "__main__":

    if len(argv) == 4:
        insert_food(argv[1], argv[2], argv[3])
        print(f"added {argv[1]} with {argv[2]} calories and {argv[3]}g protein per 100g serving")

    elif len(argv) == 5 or (len(argv) == 6 and argv[5] == 'g'):
        cals = float(argv[2]) * (100 / argv[4])
        protein = float(argv[3]) * (100 / argv[4])
        insert_food(argv[1], cals, protein)
        print(f"added {argv[1]} with {cals} calories and {protein}g protein per 100g serving")

    elif len(argv) == 6 and argv[5] == 'oz':
        cals = float(argv[2]) * (100 / oz_to_g(float(argv[4])))
        protein = float(argv[3]) * (100 / oz_to_g(float(argv[4])))
        insert_food(argv[1], cals, protein)
        print(f"added {argv[1]} with {cals} calories and {protein}g protein per 100g serving")

    else:
        print("""usage: py add.py <name> <calories> <protein> <(optional) serving size> <(optional) serving unit> 
              (note: default serving size is 100g, currently supported serving units are 'g' and 'oz')
              """)