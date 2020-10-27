import csv


def save_data(filename, data_list):
    """Writes to csv file"""
    with open(filename, "w", newline="") as infile:
        for stats in data_list:
            writer = csv.writer(infile)
            writer.writerow(stats)


def load_default_data():
    """Reads content from default file and returns as a list"""
    filename = "covid_19_clean_complete.csv"
    list_of_lists = []
    with open(filename) as infile:
        reader = csv.reader(infile)
        for row in reader:
            list_of_lists.append(",".join([row[1]] + [row[4]] + row[5:9]))
    list_of_lists.pop(0)
    list_of_lists.sort()
    list_of_lists2 = []
    a = list_of_lists.pop(0).split(",")
    list_of_lists2.append(a[:2] + [int(i) for i in a[2:]])
    while list_of_lists != []:
        a = list_of_lists.pop(0).split(",")
        if a[:2] == list_of_lists2[-1][:2]:
            for i in range(2, 6):
                list_of_lists2[-1][i] += int(a[i])
        else:
            list_of_lists2.append(a[:2] + [int(i) for i in a[2:]])

    # load list of lists into table
    return list_of_lists2


def load_data_from_file(filename):
    """Reads content from given file and returns it as a list"""
    list_of_lists = []
    with open(filename) as infile:
        reader = csv.reader(infile)
        for row in reader:
            list_of_lists.append(row)

    return list_of_lists
