import sqlite3
from sys import argv

con = sqlite3.connect('self.db')
cur = con.cursor()

if len(argv) == 2:
    statement = argv[1]
    if statement[-1] != ';': statement += ';'

    if sqlite3.complete_statement(statement):
        if "select" in statement.lower():
            for row in cur.execute(statement):
                print(row)
        else:
            cur.execute(statement)
            con.commit()
            print("Executed statement")
    else:
        print("Invalid SQL statement, try again")
else:
    print("usage: py sql.py <sql-statement>")

print()