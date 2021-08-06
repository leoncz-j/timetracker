

'''
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
                             type=str,
                             nargs="?",
                             help='Anzahl der Zeilen.')
    parser_read.set_defaults(func=read_wrapper)

    parser_delete = subparsers.add_parser('delete',
                                          help='Löschen der letzten Zeilen.')
    parser_delete.add_argument('Lines',
                               metavar='lines',
                               type=str,
                               nargs="?",
                               help='Anzahl der Zeilen.')
    parser_delete.set_defaults(func=delete_wrapper)

    return parser.parse_args(args)
'''