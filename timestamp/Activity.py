from datetime import datetime, date
from os.path import expanduser
import configparser
import timestamp.helpers as helpers

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

    def __iter__(self):
        return (i for i in (self.description, self.time, self.date))

    def __eq__(self, other):
        return tuple(self) == tuple(other)


class Activity:

    def __init__(self, timestamp_start, timestamp_stop=None):
        self.timestamp_start = timestamp_start
        self.timestamp_stop = timestamp_stop
        self.description = timestamp_start.description

    def __str__(self):
        return 'Activity: (From %s, Until %s)' % (self.timestamp_start, self.timestamp_stop)

    def __iter__(self):
        return (i for i in (self.timestamp_start, self.timestamp_stop, self.description))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

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
        if self.timestamp_start.date < timestamp.date:
            self.timestamp_stop = Timestamp(timestamp.description,
                                            self.timestamp_start.datetime.replace(hour=23, minute=59))
        else:
            self.timestamp_stop = timestamp


class Config:
    DEFAULT_PATH = 'config.ini'

    def __init__(self, file=DEFAULT_PATH):
        """If there is a file, config will be loaded from the file, else the initiated config object will use Default values"""
        self.config_data = configparser.ConfigParser()

        if self.check_file(file):
            self.config_file = file
        else:
            self.reset()
            self.config_file = self.DEFAULT_PATH

    def reset(self, datestamp=None):
        """Resets the config.ini file to default values """
        if datestamp is not None:
            self.config_data['Default File'] = {
                'file': self.get_file_path(datestamp)}
        else:
            self.config_data['Default File'] = {
                'file': self.get_file_path()}

    def path_to_config(self, file):
        self.config_data['Default File'] = {
            'file': file}

    def write(self):
        with open(self.config_file, 'w') as configfile:
            self.config_data.write(configfile)

    def get_path_from_config(self):
        if not self.config_data['Default File']['file']:
            self.config_data.read(self.config_file)
        return self.config_data['Default File']['file']

    @staticmethod
    def get_home_path():
        return expanduser("~")

    def get_file_path(self, datestamp=date.today().strftime('%m-%y')):
        return self.get_home_path() + '/Zeiterfassung-' + datestamp + '.csv'

    @staticmethod
    def check_file(file):
        try:
            helpers.read(file)
            return True
        except FileNotFoundError:
            return False
