from timestamp.helpers import read, write, append_timestamp, insert_stop_timestamp, last_has_timestamp, check_file, \
    yes_no
import argparse

from datetime import date
from timestamp.Activity import Timestamp
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

    parser_read = subparsers.add_parser('read',
                                        help='Auslesen der letzten Zeilen.')
    parser_read.add_argument('Lines',
                             metavar='lines',
                             type=int,
                             nargs="?",
                             help='Anzahl der Zeilen.',
                             default=1)
    parser_read.set_defaults(func=read_wrapper)

    parser_delete = subparsers.add_parser('delete',
                                          help='Löschen der letzten Zeilen.')
    parser_delete.add_argument('Lines',
                               metavar='lines',
                               type=int,
                               nargs="?",
                               help='Anzahl der Zeilen.',
                               default=1)
    parser_delete.set_defaults(func=delete_wrapper)

    return parser.parse_args(args)


def stop(file, timestamp):
    if not check_file(file):
        print('Die Datei existiert nicht! Soll sie angelegt werden? (y/n)')
        inp = yes_no()
        if inp == 'n':
            sys.exit()
        write([], file)

    rows = read(file)
    if bool(len(rows)) and last_has_timestamp(rows):
        append_timestamp(file, timestamp)
        print('Stopp-Zeitstempel bereits vorhanden. Neuer Zeitstempel wurde angelegt!')

    elif bool(len(rows)):
        insert_stop_timestamp(rows, file, timestamp)

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

    rows = read(file)
    if bool(len(rows)) and last_has_timestamp(rows) is False:
        print('Letzter Zeitstempel hat keinen Stopp Zeitstempel. Trotzdem neuen Eintrag anlegen? (y/n)')
        inp = yes_no()
        if inp == 'n':
            sys.exit()
    append_timestamp(file, timestamp)


def read_lines(file, lines=5):
    if not check_file(file):
        print('Die Datei existiert nicht!')
        sys.exit()

    rows = read(file)
    if not bool(len(rows)):
        print('Die Datei ist leer!')
        sys.exit()

    rows.reverse()
    lines_to_read = [rows[i] for i in list(range(lines if lines <= len(rows) else len(rows)))]
    lines_to_read.reverse()
    for line in lines_to_read:
        print(str(line).replace("'", "")[1:-1])


def delete_lines(file, lines=1):
    if not check_file(file):
        print('Die Datei existiert nicht!')
        sys.exit()

    rows = read(file)
    if not bool(len(rows)):
        print('Die Datei ist leer!')
        sys.exit()

    print('Sicher, dass die letzte', ('n ' + lines + ' ') if lines > 1 else '', 'Aktivität', 'en' if lines > 1 else '',
          'gelöscht werden soll', 'en? (y/n)' if lines > 1 else '? (y/n)')

    inp = yes_no()
    if inp == 'n':
        sys.exit()

    rows = rows[:-lines]
    write(rows, file)


def start_wrapper(args):
    file = DEFAULT_PATH
    timestamp = Timestamp(args.Activity)
    start(file, timestamp)


def read_wrapper(args):
    file = DEFAULT_PATH
    read_lines(file, args.Lines)


def delete_wrapper(args):
    file = DEFAULT_PATH
    delete_lines(file, args.Lines)


def stop_wrapper(args):
    file = DEFAULT_PATH
    timestamp = Timestamp(args.Activity)
    stop(file, timestamp)


def main():
    args = parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
