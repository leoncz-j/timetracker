'''Tests the helpers Functions in main. '''
import os
from timestamp.helpers import last_has_timestamp, check_file  # , write, append_timestamp, read, \
# insert_stop_timestamp
from datetime import datetime

today = datetime.strptime('04.08.21 12:18', '%d.%m.%y %H:%M')
today_str = today.strftime('%m-%y')
"""

def test_config():
    config(today_str)
    assert check_file(os.getcwd() + '/config.ini')
    config_file = os.getcwd() + '/config.ini'
    file = get_path_from_config(config_file)
    assert file == get_home_path() + '/Zeiterfassung-08-21.csv'


def test_get_file_path():
    path = get_file_path()
    assert path == get_home_path() + '/Zeiterfassung-08-21.csv'

"""


def test_last_has_timestamp():
    row = ['', '', '', '']
    table = [row]
    assert last_has_timestamp(table) is False
    row = ['', '', '12:08', '']
    table = [row]
    assert last_has_timestamp(table)


def test_check_file():
    assert check_file('/tests/data/doesnotexist.csv') is False
    assert check_file(os.getcwd() + '/tests/data/testfile.csv')
