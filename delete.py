import sqlite3
from sys import argv

con = sqlite3.connect('self.db')
cur = con.cursor()

if len(argv) == 3 and argv[1] == 'log' and argv[2].isdigit():
    cur.execute(f"DELETE FROM logs WHERE id={argv[2]}")
    con.commit()
elif len(argv) == 3 and argv[1] == 'food' and argv[2].isdigit():
    cur.execute(f"DELETE FROM nutrition WHERE id={argv[2]}")
    con.commit()
else:
    print("usage: py delete.py log <id> OR py delete.py food <id>")