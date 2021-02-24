# Filename: support.py
import datetime

def print_func(par):
    print("Hello : ", par)
    return

def titles(RUNITEM):
    now = datetime.datetime.now()
    print('title: ' + str(RUNITEM) + ' is start running at ' + str(now))

def judge(FailRetry, FailRetrytimes):
    if int(FailRetry) < int(FailRetrytimes):
        return True
    return False


