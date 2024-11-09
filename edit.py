import sqlite3
from sys import argv

con = sqlite3.connect('self.db')
cur = con.cursor()

cur.execute("UPDATE logs SET date='2024-11-08' WHERE id=27")
cur.execute("UPDATE logs SET date='2024-11-08' WHERE id=25")

con.commit()