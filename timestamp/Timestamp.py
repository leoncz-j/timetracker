from datetime import datetime


class Timestamp:

    def __init__(self, description, timestamp=None):
        self.description = description
        if timestamp is None:
            self.datetime = datetime.now()
        else:
            self.datetime = timestamp
        self.time = self.datetime.time()
        self.date = self.datetime.date()

    def __str__(self):
        return 'Timestamp (%s, %s, %s)' % (
            self.date.strftime('%d.%m.%y'), self.time.strftime('%H:%M'), "Tätigkeit: " + self.description)


class Activity:

    def __init__(self, timestamp_start, timestamp_stop=None):
        self.timestamp_start = timestamp_start
        self.timestamp_stop = timestamp_stop
        self.description = timestamp_start.description

    def __str__(self):
        return 'Activity: (From %s, Until %s)' % (self.timestamp_start, self.timestamp_stop)

    @classmethod
    def from_row(cls, row):
        if len(row) != 4:
            raise ValueError
        description = row[3][11:] if row[3][:11] == 'Tätigkeit: ' else row[3]
        datetime_start = datetime.strptime(row[0] + ' ' + row[1], '%d.%m.%y %H:%M')
        if len(row[2].strip(' ')) != 0:
            datetime_stop = datetime.strptime(row[0] + ' ' + row[2], '%d.%m.%y %H:%M')
        else:
            datetime_stop = None

        return cls(Timestamp(description, datetime_start),
                   Timestamp(description, datetime_stop) if datetime_stop is not None else None)

    def to_row(self):
        start = self.timestamp_start
        stop = self.timestamp_stop
        description = start.description  # if stop is None else start.description + ' ' + stop.description

        if self.timestamp_stop is None:
            return [start.date.strftime('%d.%m.%y'), start.time.strftime('%H:%M'), '',
                    "Tätigkeit: " + description]
        else:
            return [start.date.strftime('%d.%m.%y'), start.time.strftime('%H:%M'), stop.time.strftime('%H:%M'),
                    "Tätigkeit: " + description]

    def add_stop_timestamp(self, timestamp):
        self.timestamp_stop = timestamp
