import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
import tkinter as tk


def save_img(figure, country):
    """Saves graph as image"""
    figure.savefig("Trend in number of confirmed cases for {}.png".format(country))
    tk.messagebox.showinfo(title="Alert",
                           message='Saved as: "Trend in number of confirmed cases for {}.png"'.format(country))


def trend_for_country(window, list_of_lists, country):
    """Displays line graph for selected country"""

    menubar = tk.Menu(window)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Save As Image", command=lambda: save_img(dataframe.plot().get_figure(), country))

    menubar.add_cascade(label="File", menu=filemenu)
    window.config(menu=menubar)

    dates = []
    number_of_confirmed = []

    for data in list_of_lists:
        if data[0] == country:
            dates.append(data[1])
            number_of_confirmed.append(data[2])

    if len(number_of_confirmed) > 1:

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
    else:
        window.destroy()
        tk.messagebox.showerror(title="Error", message="Error: Not enough data to plot graph")
