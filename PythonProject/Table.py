from tkinter import *
from tkinter import ttk
from operator import itemgetter


def load_table(root, item_list):
    """Loads data into table"""
    table = root.children["!treeview"]
    table.delete(*table.get_children())

    for (country, date, value1, value2, value3, value4) in item_list:
        int(value1)
        int(value2)
        int(value3)
        int(value4)
        table.insert("", "end", values=(country, date, value1, value2, value3, value4))


def sort(root, col_name):
    """Sorts contents of table"""
    if col_name == "Country":
        sort_col = 0
    elif col_name == "Date":
        sort_col = 1
    elif col_name == "Number of Confirmed Cases":
        sort_col = 2
    elif col_name == "Number of Deaths":
        sort_col = 3
    elif col_name == "Number of Recovered Cases":
        sort_col = 4
    else:
        sort_col = 5

    table = root.children["!treeview"]
    item_list = []
    for child in table.get_children():
        item_list.append(table.item(child)["values"])

    item_list.sort(key=itemgetter(sort_col))
    load_table(root, item_list)


def init_table(root):
    """Initialises table"""
    title = Label(root, text="Covid 19 analyser", font=("ComicSans", 40)).pack()
    headers = ("Country", "Date", "Number of Confirmed Cases", "Number of Deaths", "Number of Recovered Cases",
               "Number of Active Cases")
    table = ttk.Treeview(root, columns=headers, show='headings')

    for col_name in headers:
        table.heading(col_name, text=col_name, command=lambda c=col_name: sort(root, c))
        table.column(col_name, stretch=YES)
    table.pack(fill=BOTH, expand=1)
