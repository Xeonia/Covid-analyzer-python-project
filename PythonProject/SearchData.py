import tkinter as tk


def valid_date(date_obj):
    """validates a date item"""
    if len(date_obj) != 3:
        return False
    for i in range(len(date_obj)):
        date_obj[i] = int(date_obj[i])
    is_leap = (date_obj[0] % 4 == 0)
    is_leap = (date_obj[0] % 100 != 0)
    is_leap = (date_obj[0] % 400 == 0)
    days = {31: [1, 3, 5, 7, 8, 10, 12], 30: [4, 6, 9, 11], 'leap': [2]}
    if date_obj[1] in days[31]:
        return date_obj[2] <= 31
    elif date_obj[1] in days[30]:
        return date_obj[2] <= 30
    elif date_obj[1] in days["leap"]:
        return date_obj[2] <= 28 + is_leap
    else:
        return False


def filter_datasets(data, country, s_date, e_date):
    """
    This function filters datasets by country and date range.
    's_date' and 'e_date' are in the format yyyy-mm-dd.
    'country' is the country of interest. By default, it is an empty string, which identifies every country.
    """
    if s_date == "":
        s_date = "1970-01-01"
    if e_date == "":
        e_date = "2030-12-31"
    metric = [1000, 50, 1]
    s_date_obj = s_date.split("-")
    e_date_obj = e_date.split("-")
    if not valid_date(s_date_obj) or not valid_date(e_date_obj):
        tk.messagebox.showerror(title="Error", message="Error: Invalid dates entered")
        return data

    s_metric = sum([int(s_date_obj[i]) * metric[i] for i in range(3)])
    e_metric = sum([int(e_date_obj[i]) * metric[i] for i in range(3)])

    if e_metric < s_metric:
        tk.messagebox.showerror(title="Error", message="Error: Start date cannot be after end date")
        return data

    # This section creates a metric to identify dates that fall within the date range.
    # Months have at least 31x the weight of days and years have at least 365x the weight

    info = []
    for i in range(len(data)):
        if data[i][0] == country or country == "":
            date_obj = data[i][1].split("-")
            date_metric = sum([int(date_obj[i]) * metric[i] for i in range(
                3)])  # create a metric to identify if the item falls within the date range specified
            if s_metric <= date_metric <= e_metric:
                info.append(data[i])
    if info != []:
        return info
    else:
        tk.messagebox.showerror(title="Error", message="Error: Invalid country")
        return data
