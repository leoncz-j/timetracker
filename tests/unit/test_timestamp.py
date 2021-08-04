'''Tests the Timestamp class and the Activity class'''

from datetime import datetime
from timestamp.Timestamp import Timestamp, Activity

datetime_start = datetime.strptime('04.08.21 12:18', '%d.%m.%y %H:%M')
datetime_stop = datetime.strptime('04.08.21 12:19', '%d.%m.%y %H:%M')


def test_to_row():
    ts_start = Timestamp('test description', datetime_start)
    ts_stop = Timestamp('test description', datetime_stop)

    activity = Activity(ts_start)
    row = activity.to_row()
    expected_row = ['04.08.21', '12:18', '', 'Tätigkeit: test description']
    assert row == expected_row

    activity.add_stop_timestamp(ts_stop)
    row = activity.to_row()
    expected_row[2] = '12:19'
    assert row == expected_row


def test_from_row():
    ts_start = Timestamp('test description', datetime_start)
    ts_stop = Timestamp('test description', datetime_stop)

    expected_activity = Activity(ts_start)
    row = ['04.08.21', '12:18', '', 'Tätigkeit: test description']
    activity = Activity.from_row(row)
    assert activity == expected_activity

    row[2] = '12:19'
    expected_activity.add_stop_timestamp(ts_stop)
    activity = Activity.from_row(row)
    assert activity == expected_activity
