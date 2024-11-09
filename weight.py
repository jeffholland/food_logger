import sqlite3
from sys import argv
from datetime import date

con = sqlite3.connect('self.db')
cur = con.cursor()

if len(argv) == 2 and argv[1].isdigit():
    cur.execute(f"INSERT INTO weight VALUES('{date.today().isoformat()}', {argv[1]})")
    con.commit()
    print(f"Logged {argv[1]} pounds for today")
else:
    print("Usage: py weight.py <weight-in-pounds>")
print()