from timestamp.helpers import read, write, append, last_has_timestamp
import argparse
from datetime import date
from timestamp.Timestamp import Timestamp, Activity
import sys

DEFAULT_PATH = '/home/leon/Dokumente/Zeiterfassung-' + date.today().strftime('%m-%y') + '.csv'


def stop(description=None):
    table = read(DEFAULT_PATH)
    if last_has_timestamp(table):
        new_activity = Activity(Timestamp(description))
        append(new_activity, DEFAULT_PATH)
        print('Stopp-Zeitstempel bereits vorhanden. Neuer Zeitstempel wurde angelegt')

    else:
        activity = Activity.from_row(table[-1])
        activity.add_stop_timestamp(Timestamp(description if description is not None else ' '))
        table[-1] = activity.to_row()
        write(table, DEFAULT_PATH)


def start(description):
    table = read(DEFAULT_PATH)
    if last_has_timestamp(table) is False:
        print('Letzter Zeitstempel hat keinen Stopp Zeitstempel. Trotzdem anlegen? (y/n)')
        inp = input()
        if inp not in ['y', 'n']:
            sys.exit()
        if inp == 'y':
            new_activity = Activity(Timestamp(description))
            append(new_activity, DEFAULT_PATH)
    else:
        new_activity = Activity(Timestamp(description))
        append(new_activity, DEFAULT_PATH)


def zeitstempel():
    parser = argparse.ArgumentParser(description='Zeitstempel in eine CSV Datei schreiben')
    parser.add_argument('Activity',
                        metavar='activity',
                        type=str,
                        help='Description of the activity')
    args = parser.parse_args()
    description = args.Activity
    start(description)


def zeitstempel_stopp():
    parser = argparse.ArgumentParser(description='Zeitstempel in eine CSV Datei schreiben')
    parser.add_argument('Activity',
                        metavar='activity',
                        type=str,
                        nargs="?",
                        default=' ',
                        help='Description of the activity')
    args = parser.parse_args()
    description = args.Activity
    stop(description)


if __name__ == '__main__':
    zeitstempel()
