from timestamp.main import parse_args
from datetime import datetime
import pytest

datetime_start = datetime.strptime('04.08.21 12:18', '%d.%m.%y %H:%M')

def test_parse_args_no_args(capsys):
    '''Should Raise a System Exit because argument option is missing'''
    with pytest.raises(SystemExit):
        parse_args([])
    out, err = capsys.readouterr()
    msg = err.split('\n')
    assert msg[1] == 'pytest: error: the following arguments are required: option'

def test_parse_args_wrong_arg(capsys):
    '''Should Raise a System Exit because of wrong argument '''
    with pytest.raises(SystemExit):
        parse_args(['wrong'])
    out, err = capsys.readouterr()
    msg = err.split('\n')
    assert msg[1] == "pytest: error: argument option: invalid choice: 'wrong' (choose from 'start', 'stop', 'read', 'delete')"

def test_parse_args_start_no_args(capsys):
    '''Should Raise a System Exit because argument activity is missing'''
    with pytest.raises(SystemExit):
        parse_args(['start'])
    out, err = capsys.readouterr()
    msg = err.split('\n')
    assert msg[1] == 'pytest start: error: the following arguments are required: activity'



