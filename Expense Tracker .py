import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Connect to SQLite database
conn = sqlite3.connect('expenses.db')
c = conn.cursor()

# Create table if not exists
c.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        amount REAL,
        category TEXT,
        date TEXT
    )
''')
conn.commit()

def add_expense(amount, category, date):
    c.execute('INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)', (amount, category, date))
    conn.commit()

def get_expenses():
    c.execute('SELECT * FROM expenses')
    return c.fetchall()

def get_summary():
    c.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    return c.fetchall()

# GUI
root = Tk()
root.title("Simple Expense Tracker")

def handle_add_expense():
    amount = amount_entry.get()
    category = category_entry.get()
    date = date_entry.get()

    if not amount or not category or not date:
        messagebox.showerror("Input Error", "All fields are required")
        return

    add_expense(amount, category, date)
    amount_entry.delete(0, END)
    category_entry.delete(0, END)
    date_entry.delete(0, END)
    messagebox.showinfo("Success", "Expense added successfully")

# Function to show expenses
def show_expenses():
    expenses_window = Toplevel(root)
    expenses_window.title("Expenses")

    expenses = get_expenses()
    tree = ttk.Treeview(expenses_window, columns=('ID', 'Amount', 'Category', 'Date'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Amount', text='Amount')
    tree.heading('Category', text='Category')
    tree.heading('Date', text='Date')

    for expense in expenses:
        tree.insert('', END, values=expense)

    tree.pack()

# Function to show summary
def show_summary():
    summary_window = Toplevel(root)
    summary_window.title("Summary")

    summary = get_summary()
    tree = ttk.Treeview(summary_window, columns=('Category', 'Total Amount'), show='headings')
    tree.heading('Category', text='Category')
    tree.heading('Total Amount', text='Total Amount')

    for item in summary:
        tree.insert('', END, values=item)

    tree.pack()

# GUI layout
frame = Frame(root)
frame.pack(pady=20)

amount_label = Label(frame, text="Amount")
amount_label.grid(row=0, column=0)
amount_entry = Entry(frame)
amount_entry.grid(row=0, column=1)

category_label = Label(frame, text="Category")
category_label.grid(row=1, column=0)
category_entry = Entry(frame)
category_entry.grid(row=1, column=1)

date_label = Label(frame, text="Date (YYYY-MM-DD)")
date_label.grid(row=2, column=0)
date_entry = Entry(frame)
date_entry.grid(row=2, column=1)

add_button = Button(frame, text="Add Expense", command=handle_add_expense)
add_button.grid(row=3, columnspan=2, pady=10)

show_expenses_button = Button(root, text="Show Expenses", command=show_expenses)
show_expenses_button.pack(pady=5)

show_summary_button = Button(root, text="Show Summary", command=show_summary)
show_summary_button.pack(pady=5)

root.mainloop()

conn.close()
