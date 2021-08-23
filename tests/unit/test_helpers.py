'''Tests the helpers Functions in main. '''
import os
from timestamp.helpers import last_has_timestamp, check_file, write, append_timestamp, read, insert_stop_timestamp




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

