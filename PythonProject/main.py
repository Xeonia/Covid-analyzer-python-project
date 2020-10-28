from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
import FileIO
import SearchData
import LineGraph
import Table
import heatmap

all_items_in_table = []


def show_heatmap():
    """Calls function to display heatmap on browser"""
    try:
        list_exists = None
        list_exists = FileIO.load_default_data()
        if list_exists is not None:
            heatmap.main()
    except:
        tk.messagebox.showerror(title="Error", message="Error: Default File has been corrupted or moved")


def search(parent, country, start_date, end_date):
    """Helper function to call functions that assist in searching and loading of data"""
    parent.destroy()
    data = SearchData.filter_datasets(all_items_in_table, country, start_date, end_date)
    Table.load_table(root, data)


def load_combobox_country_and_date():
    """Returns a tuple containing set of countries and set of dates"""
    set_countries = set()
    set_dates = set()
    for item in all_items_in_table:
        set_countries.add(item[0])
        set_dates.add(item[1])

    list_countries = sorted(list(set_countries))
    list_dates = sorted(list(set_dates))
    list_countries.insert(0, "")
    list_dates.insert(0, "")
    return list_countries, list_dates


def line_graph(parent, country):
    """Helper function to validate country and call function to display graph"""
    valid_country = False
    for i in range(len(all_items_in_table)):
        if all_items_in_table[i][0] == country:
            valid_country = True
            break
    if country == "":
        tk.messagebox.showerror(title="Error", message="Error: You must choose a country")
    elif not valid_country:
        tk.messagebox.showerror(title="Error", message="Error: Invalid country")
    else:
        parent.destroy()
        newWindow = Toplevel(root)
        newWindow.title(country)

        # sets the geometry of toplevel
        newWindow.geometry("750x500")
        LineGraph.trend_for_country(newWindow, all_items_in_table, country)


def show_graph():
    """Select country to view graph"""
    newWindow = Toplevel(root)
    newWindow.title("Select country")

    newWindow.geometry("250x50")
    list_countries = load_combobox_country_and_date()[0]
    Label(newWindow, text="Select Country").grid()
    select_country = ttk.Combobox(newWindow, values=list_countries[1:])
    select_country.grid(row=0, column=1)

    Button(newWindow, text="View Graph", command=lambda: line_graph(newWindow, select_country.get())).grid(row=1,
                                                                                                           column=1)


def about_window():
    """Displays about window"""
    newWindow = Toplevel(root)
    newWindow.title("About")

    newWindow.geometry("300x70")

    Label(newWindow,
          text="Python Project on Covid 19 analyser").pack()
    Label(newWindow,
          text="Done By: Eugene, Bryan, Varun, Samuel and Darrell").pack()


def init_search():
    """Initialises search window"""
    list_countries, list_dates = load_combobox_country_and_date()

    newWindow = Toplevel(root)
    newWindow.title("Search")

    newWindow.geometry("250x100")

    Label(newWindow, text="Country: ").grid(row=0)
    Label(newWindow, text="Start Date: ").grid(row=1)
    Label(newWindow, text="End Date: ").grid(row=2)

    countries = ttk.Combobox(newWindow, values=list_countries)
    countries.current(0)
    countries.grid(row=0, column=1)
    sdates = ttk.Combobox(newWindow, values=list_dates)
    sdates.current(0)
    sdates.grid(row=1, column=1)
    edates = ttk.Combobox(newWindow, values=list_dates)
    edates.current(0)
    edates.grid(row=2, column=1)
    Button(newWindow, text="Search",
           command=lambda: search(newWindow, countries.get(), sdates.get(), edates.get())).grid(row=3,
                                                                                                column=1)


def open_file():
    """Allows user to open and load data from file"""
    global all_items_in_table
    previous_contents = all_items_in_table
    filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    try:
        if len(filename) > 0:
            data_list = FileIO.load_data_from_file(filename)
            all_items_in_table = data_list
            for element in all_items_in_table:
                element[2] = int(element[2])
                element[3] = int(element[3])
                element[4] = int(element[4])
                element[5] = int(element[5])
            Table.load_table(root, data_list)
            init_menu(show_view=True)
    except:
        all_items_in_table = previous_contents
        tk.messagebox.showerror(title="Error", message="Error: You must choose a csv file you saved from this project")


def load_default_file():
    """Load default data"""
    global all_items_in_table
    previous_contents = all_items_in_table
    try:
        data_list = FileIO.load_default_data()
        all_items_in_table = data_list
        for element in all_items_in_table:
            element[2] = int(element[2])
            element[3] = int(element[3])
            element[4] = int(element[4])
            element[5] = int(element[5])
        Table.load_table(root, data_list)
        init_menu(show_view=True)
    except:
        all_items_in_table = previous_contents
        tk.messagebox.showerror(title="Error", message="Error: Default File has been corrupted or moved")


def save_csv():
    """Allows user to save contents of table into file"""
    filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                            filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    if len(filename) > 0:
        filename += ".csv"
        table = root.children["!treeview"]
        item_list = []
        for child in table.get_children():
            item_list.append(table.item(child)["values"])
        FileIO.save_data(filename, item_list)


def init_menu(show_view=False):
    """Shows the menu bar for main window"""
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=open_file)
    filemenu.add_command(label="Load default", command=load_default_file)
    filemenu.add_command(label="Save", command=save_csv)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=exit)
    menubar.add_cascade(label="File", menu=filemenu)

    if show_view:
        viewmenu = Menu(menubar, tearoff=0)
        viewmenu.add_command(label="Search", command=init_search)
        viewmenu.add_command(label="Show graph", command=show_graph)
        viewmenu.add_command(label="Show global heatmap", command=show_heatmap)
        menubar.add_cascade(label="View", menu=viewmenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About...", command=about_window)
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menubar)


def init():
    """Calls initialising functions"""
    init_menu()
    Table.init_table(root)


root = Tk()
root.title("Covid-19 Analyser")

init()
root.mainloop()
