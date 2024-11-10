import sqlite3
from sys import argv
from datetime import date

con = sqlite3.connect('self.db')
cur = con.cursor()

def validate_number(input):
    if input.isdigit(): return True

    split_decimal = input.split('.')
    if len(split_decimal) == 2 and split_decimal[0].isdigit() and split_decimal[1].isdigit():
        return True
    
    return False


if len(argv) == 2 and validate_number(argv[1]):
    cur.execute(f"INSERT INTO weight VALUES('{date.today().isoformat()}', {argv[1]})")
    con.commit()
    print(f"Logged {argv[1]} pounds for today")
else:
    print("Usage: py weight.py <weight-in-pounds>")
print()