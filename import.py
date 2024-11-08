import sqlite3
from csv import DictReader

def import_nutrition_table():

    con = sqlite3.connect("self.db")
    cur = con.cursor()
    cur.execute("DROP TABLE nutrition")
    cur.execute("CREATE TABLE nutrition(id, name, calories, protein)")

    with open('data.csv', 'r') as f:
        reader = DictReader(f)
        for line in reader:
            name = line['name'].replace("'", "")

            cur.execute(f"INSERT INTO nutrition VALUES ({line['ID']}, '{name}', {line['Calories']}, {line['Protein (g)']})")

    con.commit()


# def import_log_table():
#     con = sqlite3.connect('self.db')
#     cur = con.cursor()
#     # cur.execute("DROP TABLE logs")
#     cur.execute("CREATE TABLE logs(id, date, food_id, serving_size, serving_unit)") 
#     con.commit()



if __name__ == "__main__":
    import_nutrition_table()