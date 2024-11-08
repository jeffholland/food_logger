import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import sqlite3
from search import search
from datetime import date
from utils import oz_to_g

PADDING = 5

con = sqlite3.connect('self.db')
cur = con.cursor()

def get_names(search_str):
    first_names = []
    other_names = []

    for item in search(search_str):
        if item[1].lower().find(search_str.lower()) == 0:
            first_names.append(item[1])
        else:
            other_names.append(item[1])

    result = [*sorted(first_names), *sorted(other_names)]
    return result

def get_id(name):
    res = cur.execute(f"SELECT id FROM nutrition WHERE name='{name}'")
    return res.fetchone()[0]

def get_unique_id():
    res = cur.execute("SELECT MAX(id) FROM logs")
    result = res.fetchall()[0][0]
    if result == None:
        return 1
    else:
        return result + 1
    
def get_nutrition(name, serving_size_in_g):
    res = cur.execute(f"SELECT calories, protein FROM nutrition WHERE name='{name}'")
    result = res.fetchone()

    if result == None: return ('', '')

    return (
        f"Calories: {round(result[0] * (serving_size_in_g / 100))}", 
        f"Protein: {round(result[1] * (serving_size_in_g / 100))}g")


def insert_log(item_id, serving_size, serving_unit='g', date=date.today().isoformat()):
    log_id = get_unique_id()
    try:
        cur.execute(f"INSERT INTO logs VALUES ({log_id}, '{date}', {item_id}, {serving_size}, '{serving_unit}')")
        con.commit()
        return True
    except Exception as e:
        return False




class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        names = get_names('')
        self.dropdown_variable = tk.StringVar(self)
        self.dropdown = ttk.Combobox(
            self, 
            values=names, 
            textvariable=self.dropdown_variable,
            postcommand=self.fill_dropdown,
            validate='focusout',
            validatecommand=self.validate_dropdown,
            width=60
        )
        self.dropdown.grid(columnspan=3, padx=PADDING, pady=PADDING)

        self.serving_size_var = tk.StringVar(self)
        self.serving_size_entry = ttk.Entry(
            self,
            textvariable=self.serving_size_var
        )
        self.serving_size_var.set(1)
        self.serving_size_entry.bind('<FocusOut>', self.reset_view_field)
        self.serving_size_entry.grid(row=0,column=3,columnspan=2,padx=PADDING,pady=PADDING)

        self.serving_unit_var = tk.StringVar(self)
        self.oz_button = ttk.Radiobutton(
            self,
            text='oz',
            value='oz',
            variable=self.serving_unit_var
        )
        self.oz_button.grid(row=1,column=3,columnspan=1,padx=PADDING,pady=PADDING)
        self.oz_button.invoke()

        self.g_button = ttk.Radiobutton(
            self,
            text='g',
            value='g',
            variable=self.serving_unit_var
        )
        self.g_button.grid(row=1,column=4,columnspan=1,padx=PADDING,pady=PADDING)

        self.log_button = ttk.Button(
            self,
            text='Log',
            state=tk.DISABLED,
            command=self.submit_log
        )
        self.log_button.grid(row=2,column=4,padx=PADDING,pady=PADDING)
        self.serving_size_entry.bind('<KeyPress-Return>', self.keypress_return_handler)
        self.log_button.bind('<KeyPress-Return>', self.keypress_return_handler)

        self.date_field_var = tk.StringVar(self)
        self.date_field = tk.Entry(
            self,
            textvariable=self.date_field_var
        )
        self.date_field_var.set(date.today().isoformat())
        self.date_field.grid(row=1, column=0, padx=PADDING, pady=PADDING)

        self.view_field_var = tk.StringVar(self)
        self.view_field = ttk.Label(
            self,
            textvariable=self.view_field_var
        )
        self.view_field.grid(row=2,column=0,columnspan=3,padx=PADDING,pady=PADDING)

    def keypress_return_handler(self, event):
        self.log_button.invoke()

    def fill_dropdown(self):
        names = get_names(self.dropdown_variable.get())
        self.dropdown.configure(values=names)

    def validate_dropdown(self):
        self.fill_dropdown()
        values = self.dropdown.cget('values')
        
        if len(values) != 0:
            self.dropdown_variable.set(values[0])
            self.log_button.config(state=tk.NORMAL)
            return True
        
        self.view_field_var.set('')
        self.log_button.config(state=tk.DISABLED)
        return False
    
    def reset_view_field(self, event):
        name = self.dropdown_variable.get()
        serving_size = self.serving_size_var.get()

        if (serving_size.isdigit() and len(name) > 0):

            name = self.dropdown_variable.get()
            serving_unit = self.serving_unit_var.get()
            serving_size = float(self.serving_size_var.get())

            if serving_unit == 'oz': serving_size = oz_to_g(serving_size)

            self.view_field_var.set(get_nutrition(name, serving_size))


    def submit_log(self):
        name = self.dropdown_variable.get()
        serving_size = self.serving_size_var.get()
        serving_unit = self.serving_unit_var.get()
        date_consumed = self.date_field_var.get()

        if insert_log(get_id(name), serving_size, serving_unit, date_consumed):
            messagebox.showinfo("Success", f"Successfully logged {serving_size}{serving_unit} of {name} consumed on {date_consumed}")
        else:
            messagebox.showerror("Error", f"Failed to log {serving_size}{serving_unit} of {name}. Try something else.")

        self.dropdown_variable.set('')
        self.serving_size_var.set('')
        self.date_field_var.set(date.today().isoformat())

app = Application()
app.master.title('Insert log')
app.mainloop()