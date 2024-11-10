import sqlite3
from datetime import date, timedelta
from utils import oz_to_g

import tkinter as tk

PADDING = 5
FONT_SIZE = 12

con = sqlite3.connect('self.db')
cur = con.cursor()

def get_logs_date(date):
    res = cur.execute(f"SELECT * FROM logs WHERE date='{date.isoformat()}'")
    logs = res.fetchall()
    result = []

    for log in logs:
        res = cur.execute(f"SELECT * FROM nutrition WHERE id={log[2]}")
        item = res.fetchone()

        if item == None:
            return None

        if log[4] == 'oz': serving_size = oz_to_g(log[3])
        else: serving_size = log[3]

        cals = round(item[2] * (serving_size / 100))
        protein = round(item[3] * (serving_size / 100))

        result.append({
            'name': item[1],
            'serving': str(log[3]) + log[4],
            'calories': cals,
            'protein': protein
        })

    return result

def get_totals(data):
    g_total = 0
    cal_total = 0
    protein_total = 0

    for row in data:
        if row['serving'][-2:] == 'oz':
            g_total += float(row['serving'][:-2]) * 28.4
        else:
            g_total += float(row['serving'][:-1])

        cal_total += row['calories']
        protein_total += row['protein']

    return ('Total', str(round(g_total)) + 'g', cal_total, protein_total)



class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.date = date.today()
        self.data = get_logs_date(self.date)
        self.createWidgets()

    def refresh_data(self):
        self.date_label_var.set(self.date.strftime("%m/%d/%y"))

        for widget in self.widgets:
            widget.grid_forget()
        self.widgets.clear()

        self.data = get_logs_date(self.date)

        row_counter = 2
        col_counter = 0
        widths = [32, 8, 8, 8]

        # Empty data

        if len(self.data) == 0:
            self.widgets.append(tk.Label(
                self,
                text="No logs",
                width=sum(widths)
            ))
            self.widgets[-1].grid(row=row_counter, column=col_counter, columnspan=4, padx=PADDING, pady=PADDING)
            return

        # Header row (keys)
        
        for key in self.data[0].keys():
            self.widgets.append(tk.Label(self, text=key, width=widths[col_counter], font=f'TkTextFont {FONT_SIZE-1} italic'))
            self.widgets[-1].grid(row=row_counter, column=col_counter)
            col_counter += 1

        row_counter += 1

        # Middle rows (values)

        for row in self.data:
            col_counter = 0

            for cell in row.values():
                if len(str(cell)) > widths[col_counter]: cell = str(cell)[:(widths[col_counter]-3)] + '...'

                self.widgets.append(tk.Label(self, text=cell, bd=2, relief='groove', width=widths[col_counter], font=f'Helvetica {FONT_SIZE} normal'))

                self.widgets[-1].grid(row=row_counter, column=col_counter)
                col_counter += 1

            row_counter += 1

        # Footer row (totals)

        totals = get_totals(self.data)
        col_counter = 0

        for total in totals:
            self.widgets.append(tk.Label(self, text=total, bd=2, relief='groove', width=widths[col_counter], font=F"Helvetica {FONT_SIZE} bold"))
            self.widgets[-1].grid(row=row_counter, column=col_counter)
            col_counter += 1
        row_counter += 1
        

    def show_prev_day(self):
        self.date -= timedelta(days=1)
        self.refresh_data()

    def show_next_day(self):
        self.date += timedelta(days=1)
        self.refresh_data()

    def createWidgets(self):
        self.widgets = []
        row_counter = 0

        # Date
        self.date_label_var = tk.StringVar(self)
        self.date_label = tk.Label(
            self,
            textvariable=self.date_label_var,
            font=f"Helvetica {FONT_SIZE+2} bold"
        )
        self.date_label_var.set(self.date.strftime("%m/%d/%y"))
        self.date_label.grid(row=row_counter, column=0, columnspan=4, pady=PADDING)
        row_counter += 1

        # Next and previous buttons
        self.prev_button = tk.Button(
            self,
            text="<<",
            command=self.show_prev_day
        )
        self.prev_button.grid(row=row_counter, column=0, pady=PADDING)
        
        self.next_button = tk.Button(
            self,
            text=">>",
            command=self.show_next_day
        )
        self.next_button.grid(row=row_counter, column=2, columnspan=3, pady=PADDING)

        row_counter += 1

        self.refresh_data()



app = Application()
app.master.title('View food logs')
app.mainloop()