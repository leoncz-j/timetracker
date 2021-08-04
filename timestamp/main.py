from timestamp.helpers import read, write, append_timestamp, insert_stop_timestamp, last_has_timestamp, check_file, \
    parse_args, yes_no
import argparse
from datetime import date
from timestamp.Timestamp import Timestamp
import sys

### config.ini anlegen, prüfen und verwenden
DEFAULT_PATH = '/home/leon/Dokumente/Zeiterfassung-' + date.today().strftime('%m-%y') + '.csv'


def stop(file, timestamp):
    table = read(file)
    if bool(len(table)) and last_has_timestamp(table):
        append_timestamp(file, timestamp)
        print('Stopp-Zeitstempel bereits vorhanden. Neuer Zeitstempel wurde angelegt!')

    elif bool(len(table)):
        insert_stop_timestamp(table, file, timestamp)

    else:
        append_timestamp(file, timestamp)
        print('In dieser Datei wurde noch kein Zeitstempel gefunden. Neuer Zeitstempel wurde angelegt!')


def stempel_checks_start(file):
    if not check_file(file):
        print('Die Datei existiert nicht! Soll sie angelegt werden? (y/n)')
        inp = yes_no()
        if inp == 'n':
            sys.exit()
        write([], file)

    table = read(file)
    if bool(len(table)) and last_has_timestamp(table) is False:
        print('Letzter Zeitstempel hat keinen Stopp Zeitstempel. Trotzdem neuen Eintrag anlegen? (y/n)')
        inp = yes_no()
        if inp == 'n':
            sys.exit()



def zeitstempel():
    file = DEFAULT_PATH
    args = parse_args()
    description = args.Activity
    timestamp = Timestamp(description)
    stempel_checks_start(file)
    append_timestamp(file, timestamp)


def zeitstempel_stopp():
    file = DEFAULT_PATH
    args = parse_args(optional=True)
    description = args.Activity
    timestamp = Timestamp(description)

    if not check_file(file):
        print('Die Datei existiert nicht! Soll sie angelegt werden? (y/n)')
        inp = yes_no()
        if inp == 'n':
            sys.exit()
        write([], file)

    stop(file, timestamp)


if __name__ == '__main__':
    zeitstempel()
