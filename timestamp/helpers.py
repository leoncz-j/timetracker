import csv



def append(activity, file):
    """Expects an object of type activity."""
    row = activity.to_row()
    with open(file, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(row)


def write(table, file):
    """Expects a list containing the rows of a csv file."""
    with open(file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerows(table)


def read(file):
    with open(file, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        return list(csvreader)


def last_has_timestamp(table):
    """Expects a list containing the rows of a csv file. Checks whether the last row has a stop timestamp."""
    row = table[-1]
    return len(row[2].strip(' ')) != 0