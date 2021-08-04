'''Tests the helpers Functions in main'''

from timestamp.helpers import last_has_timestamp


def test_last_has_timestamp():
    row = ['', '', '', '']
    table = [row]
    assert last_has_timestamp(table) is False
    row = ['', '', '12:08', '']
    table = [row]
    assert last_has_timestamp(table)
