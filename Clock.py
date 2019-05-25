from random import randint
from datetime import datetime
from datetime import timedelta
from time import time


class Clock:

    def __init__(self):
        self._error = randint(0, 29) * 1000

    def getClock(self):
        return (self._current_milli_time() + self._error)

    def adjustClock(self, a):
        self._error += a

    def getDate(self):
        current_milli_time_error = self._current_milli_time() + self._error
        return datetime.utcfromtimestamp(current_milli_time_error // 1000).replace(microsecond=current_milli_time_error % 1000 * 1000).strftime("%c")

    def _current_milli_time(self):
        return (round(time() * 1000))
