from timestamp.helpers import read, write, append_timestamp, insert_stop_timestamp, last_has_timestamp, check_file, \
    yes_no
import argparse
from datetime import date
from timestamp.Timestamp import Timestamp
import sys

### config.ini anlegen, prüfen und verwenden
DEFAULT_PATH = '/home/leon/Dokumente/Zeiterfassung-' + date.today().strftime('%m-%y') + '.csv'


def parse_args(args=None):
    parser = argparse.ArgumentParser(description='Zeitstempel in eine CSV Datei schreiben')

    subparsers = parser.add_subparsers(help='Zur Auswahl stehen start, stop, config, read oder delete.', dest='option',
                                       required=True)
    parser_start = subparsers.add_parser('start', help='Ein neuer Start-Zeitstempel wird in die CSV Datei geschrieben.')
    parser_start.add_argument('Activity',
                              metavar='activity',
                              type=str,
                              help='Beschreibung der Aktivität.')
    parser_start.set_defaults(func=start_wrapper)

    parser_stop = subparsers.add_parser('stop',
                                        help='Ein Stopp-Zeitstempel wird zur letzten Aktivität hinzugefügt. Zusätzliche Beschreibung optional.')
    parser_stop.add_argument('Activity',
                             metavar='activity',
                             type=str,
                             nargs="?",
                             help='Beschreibung der Aktivität.')
    parser_stop.set_defaults(func=stop_wrapper)

    return parser.parse_args(args)


def stop(file, timestamp):
    if not check_file(file):
        print('Die Datei existiert nicht! Soll sie angelegt werden? (y/n)')
        inp = yes_no()
        if inp == 'n':
            sys.exit()
        write([], file)

    table = read(file)
    if bool(len(table)) and last_has_timestamp(table):
        append_timestamp(file, timestamp)
        print('Stopp-Zeitstempel bereits vorhanden. Neuer Zeitstempel wurde angelegt!')

    elif bool(len(table)):
        insert_stop_timestamp(table, file, timestamp)

    else:
        append_timestamp(file, timestamp)
        print('In dieser Datei wurde noch kein Zeitstempel gefunden. Neuer Zeitstempel wurde angelegt!')


def start(file, timestamp):
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
    append_timestamp(file, timestamp)


def start_wrapper(args):
    file = DEFAULT_PATH
    timestamp = Timestamp(args.Activity)
    start(file, timestamp)


def stop_wrapper(args):
    file = DEFAULT_PATH
    timestamp = Timestamp(args.Activity)
    stop(file, timestamp)


def main():
    args = parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
