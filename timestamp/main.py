from timestamp.helpers import read, write, append, last_has_timestamp, check_file
import argparse
from datetime import date
from timestamp.Timestamp import Timestamp, Activity
import sys

### config.ini anlegen, prüfen und verwenden
DEFAULT_PATH = '/home/leon/Dokumente/Zeiterfassung-' + date.today().strftime('%m-%y') + '.csv'


def yes_no():
    inp = input()
    if inp not in ['y', 'n']:
        sys.exit()
    return inp


def stop(file, description=None):
    table = read(file)
    if bool(len(table)) and last_has_timestamp(table):
        new_activity = Activity(Timestamp(description))
        append(new_activity, file)
        print('Stopp-Zeitstempel bereits vorhanden. Neuer Zeitstempel wurde angelegt!')

    elif bool(len(table)):
        activity = Activity.from_row(table[-1])
        activity.add_stop_timestamp(Timestamp(description if description is not None else ' '))
        table[-1] = activity.to_row()
        write(table, file)

    else:
        new_activity = Activity(Timestamp(description))
        append(new_activity, file)
        print('In dieser Datei wurde noch kein Zeitstempel gefunden. Neuer Zeitstempel wurde angelegt!')


def start(file, description):
    table = read(file)
    if bool(len(table)) and last_has_timestamp(table) is False:
        print('Letzter Zeitstempel hat keinen Stopp Zeitstempel. Trotzdem neuen Eintrag anlegen? (y/n)')
        inp = yes_no()
        if inp == 'y':
            new_activity = Activity(Timestamp(description))
            append(new_activity, file)
    else:
        new_activity = Activity(Timestamp(description))
        append(new_activity, file)


def zeitstempel():
    parser = argparse.ArgumentParser(description='Zeitstempel in eine CSV Datei schreiben')
    parser.add_argument('Activity',
                        metavar='activity',
                        type=str,
                        help='Description of the activity')
    args = parser.parse_args()
    description = args.Activity
    file = DEFAULT_PATH

    if not check_file(file):
        print('Die Datei existiert nicht! Soll sie angelegt werden? (y/n)')
        inp = yes_no()
        if inp == 'n':
            sys.exit()
        write([], file)

    start(file, description)


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
    file = DEFAULT_PATH

    if not check_file(file):
        print('Die Datei existiert nicht! Soll sie angelegt werden? (y/n)')
        inp = yes_no()
        if inp == 'n':
            sys.exit()
        write([], file)

    stop(file, description)


if __name__ == '__main__':
    zeitstempel()
