# Filename: support.py
import os
import re
import datetime


def gettesttime(start):
    EndTime = datetime.datetime.now()
    EndTimes = re.sub(r'\..*$', "", str(EndTime))
    d1 = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(EndTimes, '%Y-%m-%d %H:%M:%S')
    TestTimes = d2 - d1
    return TestTimes


def titles(RUNITEM, stage):
    now = datetime.datetime.now()
    StartTimes = re.sub(r'\..*$', "", str(now))
    print('title: ' + str(RUNITEM) + ' is ' + str(stage) + ' running at ' + str(StartTimes))
    return StartTimes


def judge(FailRetry, FailRetrytimes):
    if int(FailRetry) < int(FailRetrytimes):
        return True
    return False


def setinfo(RUNITEM, SN, UPLIMIT, LOWLIMIT, Result, NUM, LOGINFO, Starttime, TestTime):
    global PASSFAIL
    if Result == 'P':
        PASSFAIL = 'PASS'
    if Result == 'F':
        PASSFAIL = 'FAIL'
    os.chdir(r'C:\WinTest\LogFile')
    logname = str('TestLog_' + PASSFAIL + '.txt')
    with open(logname, 'a', encoding='utf-8') as f:
        f.write('PAT_TEST,' + RUNITEM + ',' + SN + ',' +
                UPLIMIT + ',' + LOWLIMIT +
                ',' + PASSFAIL + ',' + NUM + ',' + LOGINFO + ',' + str(Starttime) + ',' + str(TestTime) + '\n')
        return
        # print(f.write('PAT_TEST,' + SN + RUNITEM + UPLIMIT + LOWLIMIT + PASSFAIL + NUM + LOGINFO + TestTime + '\n'))


def getSN():
    os.chdir(r'C:\WinTest\Tools')
    instruct = 'EEPROM64.exe -g -ln -f SN.txt'
    os.system(instruct)
    log_name = 'SN.txt'
    with open(log_name, 'r', encoding='utf-8', newline='') as f:
        for line in f:
            SN = line
            pattern = re.compile(r'^[0-9A-Z]{8}$')
            m = pattern.match(SN)
            print(m.group())  # 匹配成功m.group()才会有值，匹配失败会报错
    return SN


def creatResult(Fixed, ItemName, Result, ItemTag):
    os.chdir(r'C:\WinTest\TestStand')
    instruct = 'tasklist | find "TestStand.exe"'
    rea = os.system(instruct)
    getID = 'sdtCheckResult.exe /a>' + ItemName + '.txt'
    os.system(getID)
    logname = ItemName + '.txt'
    with open(logname, 'r', encoding='utf-8', newline='') as f:
        for line in f.readlines():
            if ItemName in line:
                str = line
                print(str)
    ItemID1 = re.sub(r'\|.*$', '', str)
    ItemID = re.sub(r'\D', '', ItemID1)
    # ItemID = str(ItemID2)
    print(ItemID)

    if rea == 0:
        para = "%s %s %s %d %s %s" % ("sdtCreateResult.exe", Fixed, ItemName, Result, ItemID, ItemTag)
        print(para)
        os.system(para)
        return 0
    if rea == 1:
        ex = Exception("TestStand.exe窗口不存在！！！")
        # 抛出异常对象
        raise ex
    else:
        print(instruct + ' 语句执行异常')
