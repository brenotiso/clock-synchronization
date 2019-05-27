from random import randint
from datetime import datetime
from datetime import timedelta
from time import time


class Clock:

    def __init__(self):
        self.__error = randint(0, 29) * 1000

    def getClock(self):
        return (self.__current_milli_time() + self.__error)

    def adjustClock(self, a):
        self.__error += a

    def getError(self):
        return self.__error

    def getDate(self):
        current_milli_time__error = self.__current_milli_time() + self.__error
        return datetime.utcfromtimestamp(current_milli_time__error // 1000).replace(microsecond=current_milli_time__error % 1000 * 1000).strftime("%c")

    def __current_milli_time(self):
        return (round(time() * 1000))
