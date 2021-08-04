import csv
import sys
import argparse
from timestamp.Timestamp import Activity


def check_file(file):
    try:
        read(file)
        return True
    except FileNotFoundError:
        return False


def yes_no():
    inp = input()
    if inp not in ['y', 'n']:
        sys.exit()
    return inp


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


def append_timestamp(file, timestamp):
    new_activity = Activity(timestamp)
    append(new_activity, file)


def insert_stop_timestamp(table, file, timestamp):
    activity = Activity.from_row(table[-1])
    activity.add_stop_timestamp(timestamp)  # if description is not None else ' '))
    table[-1] = activity.to_row()
    write(table, file)


def parse_args(args=None, optional=False):
    parser = argparse.ArgumentParser(description='Zeitstempel in eine CSV Datei schreiben')
    if optional is False:
        parser.add_argument('Activity',
                            metavar='activity',
                            type=str,
                            help='Description of the activity')
    else:
        parser.add_argument('Activity',
                            metavar='activity',
                            type=str,
                            nargs="?",
                            default=' ',
                            help='Description of the activity')
    return parser.parse_args(args)
