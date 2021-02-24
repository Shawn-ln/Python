# Filename: head.py
import datetime

class Head:
    def __init__(self, FailRetry, FailRetrytimes, UPLIMIT, LOWLIMIT,  RUNITEM):
        self.FailRetry = FailRetry
        self.FailRetrytimes = FailRetrytimes
        self.UPLIMIT = UPLIMIT
        self.LOWLIMIT = LOWLIMIT
        self.RUNITEM = RUNITEM
        self.now = datetime.datetime.now()

    def titles(self):
        print('title: ' + str(self.RUNITEM) + ' is start running at ' + str(self.now))

    def judge(self):
        if self.FailRetry < self.FailRetrytimes:
            return True
        return False


