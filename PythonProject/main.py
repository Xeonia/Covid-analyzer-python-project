from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from operator import itemgetter
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
import FileIO

all_items_in_table = []


def filter_datasets(data, country, s_date, e_date):
    metric = [1000, 50, 1]
    if s_date == "":
        s_date = "0000-00-00"
    if e_date == "":
        e_date = "2300-12-31"
    s_date_obj = s_date.split("-")
    s_metric = sum([int(s_date_obj[i]) * metric[i] for i in range(3)])
    e_date_obj = e_date.split("-")
    e_metric = sum([int(e_date_obj[i]) * metric[i] for i in range(3)])
    info = []
    for i in range(0, 35156, 188):
        if data[i][0] == country or country == "":
            if e_date:
                for j in range(188):
                    date_obj = data[i + j][1].split("-")
                    date_metric = sum([int(date_obj[i]) * metric[i] for i in range(3)])
                    if s_metric <= date_metric <= e_metric:
                        info.append(data[i + j])
            else:
                for j in range(188):
                    if s_date == data[i + j][1]:
                        info.append(data[i + j])
    return info


def search(parent, country, start_date, end_date):
    if end_date < start_date:
        tk.messagebox.showerror(title="Error", message="Error: End date must be after start date")
    else:
        parent.destroy()
        data = filter_datasets(all_items_in_table, country, start_date, end_date)
        load_table(data)


def load_combobox_country_and_date():
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


def save_img(figure, country):
    figure.savefig("Trend in number of confirmed cases for {}.png".format(country))
    tk.messagebox.showinfo(title="Alert",
                           message='Saved as: "Trend in number of confirmed cases for {}.png"'.format(country))


def trend_for_country(window, list_of_lists, country):
    menubar = Menu(window)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Save As Image", command=lambda: save_img(dataframe.plot().get_figure(), country))

    menubar.add_cascade(label="File", menu=filemenu)
    window.config(menu=menubar)

    dates = []
    number_of_confirmed = []
    for data in list_of_lists:
        if data[0] == country:
            dates.append(data[1])
            number_of_confirmed.append(data[2])

    figure = plt.Figure(figsize=(100, 100), dpi=80)
    ax = figure.add_subplot()

    line = FigureCanvasTkAgg(figure, window)
    line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    data = {"Date": dates, "Number of confirmed cases": number_of_confirmed}

    dataframe = DataFrame(data, columns=["Date", "Number of confirmed cases"])
    dataframe = dataframe[['Date', 'Number of confirmed cases']].groupby('Date').sum()
    dataframe.plot(kind='line', legend=True, ax=ax, fontsize=10,
                   title="Number of confirmed cases in {} over time".format(country))

    ax.set_xlabel("Date")
    ax.set_ylabel("Number of confirmed cases")


def load_table(item_list, newFile=False):
    if newFile:
        global all_items_in_table
        all_items_in_table = item_list

    table = root.children["!treeview"]
    table.delete(*table.get_children())

    try:
        for (country, date, value1, value2, value3, value4) in item_list:
            int(value1)
            int(value2)
            int(value3)
            int(value4)
            table.insert("", "end", values=(country, date, value1, value2, value3, value4))
    except:
        tk.messagebox.showerror(title="Error", message="Error: You must choose a csv file you saved from this project")


def sort(col_name):
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
    load_table(item_list)


def line_graph(parent, country):
    if country == "":
        tk.messagebox.showerror(title="Error", message="Error: You must choose a country")
    else:
        parent.destroy()
        newWindow = Toplevel(root)
        newWindow.title(country)

        # sets the geometry of toplevel
        newWindow.geometry("750x500")
        trend_for_country(newWindow, all_items_in_table, country)


def show_graph():
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
    newWindow = Toplevel(root)
    newWindow.title("About")

    newWindow.geometry("300x70")

    Label(newWindow,
          text="Python Project on Covid 19 analyser").pack()
    Label(newWindow,
          text="Done By: Eugene, Bryan, Varun, Samuel and Darrell").pack()


def init_search():
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
    filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    if len(filename) > 0:
        data_list = FileIO.load_data_from_file(filename)
        load_table(data_list, newFile=True)
        init_menu(show_view=True)


def load_default_file():
    data_list = FileIO.load_default_data()
    load_table(data_list, newFile=True)
    init_menu(show_view=True)


def save_csv():
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
        viewmenu.add_command(label="Graph", command=show_graph)
        menubar.add_cascade(label="View", menu=viewmenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About...", command=about_window)
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menubar)


def init_table():
    title = Label(root, text="Covid 19 analyser", font=("ComicSans", 40)).grid(row=0, columnspan=6)
    headers = ("Country", "Date", "Number of Confirmed Cases", "Number of Deaths", "Number of Recovered Cases",
               "Number of Active Cases")
    table = ttk.Treeview(root, columns=headers, show='headings')

    for col_name in headers:
        table.heading(col_name, text=col_name, command=lambda c=col_name: sort(c))
    table.grid(row=1, columnspan=6)


def init():
    init_menu()
    init_table()


root = Tk()

init()
root.mainloop()
