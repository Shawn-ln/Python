# Coding by LiXiao
# Datatime:2/26/2021 11:37 AM
# Filename:support.py
# Toolby: PyCharm

import os
import re
import datetime
from shutil import copyfile


def get_ini_info(param):
    os.chdir(r'C:\WinTest')
    logname = 'Model_ini.BAT'
    with open(logname, 'r', encoding='utf-8', newline='') as f:
        for line in f.readlines():
            if param in line:
                # 截取'param='后面的内容
                str = re.sub(r'^.*=', '', line)
                return str
            else:
                ex = Exception("param信息在Model_ini.BAT未找到！！！")
                # 抛出异常对象
                raise ex


def gettesttime(start):
    EndTime = datetime.datetime.now()
    EndTimes = re.sub(r'\..*$', "", str(EndTime))
    d1 = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(EndTimes, '%Y-%m-%d %H:%M:%S')
    TestTimes = d2 - d1
    return TestTimes


def disableIPV6():
    instruct1 = 'reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters" /v DisabledComponents /t REG_DWORD /d 0xffffffff /f'
    os.system(instruct1)
    instruct2 = 'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient" /v EnableMulticast /t REG_DWORD /d 0 /f'
    os.system(instruct2)
    instruct3 = 'reg add "HKLM\SOFTWARE\Wow6432Node\Policies\Microsoft\Windows NT\DNSClient" /v EnableMulticast /t REG_DWORD /d 0 /f'
    os.system(instruct3)
    instruct4 = 'netsh advfirewall firewall add rule name="Block All ICMPV6 Inbound" protocol=icmpv6:any,any dir=in action=block'
    os.system(instruct4)
    instruct5 = 'netsh advfirewall firewall add rule name="Block All ICMPV6 Outbound" protocol=icmpv6:any,any dir=out action=block'
    os.system(instruct5)
    instruct6 = 'netsh advfirewall firewall add rule name="Block All LLMNR UDP Outbound" protocol=UDP remoteport=5355 dir=out action=block'
    os.system(instruct6)
    return

def padsetting():
    os.chdir(r'C:\WinTest\Tools')
    instruct1 = 'RotationLock.exe -D'
    os.system(instruct1)
    instruct2 = 'ChangeScreenOrien.exe -A'
    os.system(instruct2)
    print('\n')
    return


def SyncTime():
    os.chdir(r'C:\WinTest\Tools')
    instruct1 = 'tzutil.exe /s "china standard time"'
    os.system(instruct1)
    instruct2 = 'start /w reg.exe import TimeFormat.reg'
    os.system(instruct2)
    instruct3 = r'net use \\172.24.248.17 "QWEqwe123.com" /user:"ncpd\sf"'
    os.system(instruct3)
    instruct4 = r'net time \\172.24.248.17 /set /yes'
    os.system(instruct4)
    return


def ptd(ptdkey):
    os.chdir(r'C:\WinTest\Tools')
    instruct = 'PTDRegRun.exe ' + ptdkey
    os.system(instruct)
    print('\n')
    return


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
    passfail = ''
    if Result == 'P':
        passfail = 'PASS'
    if Result == 'F':
        passfail = 'FAIL'
    os.chdir(r'C:\WinTest\LogFile')
    logname = str('TestLog_' + passfail + '.txt')
    with open(logname, 'a', encoding='utf-8') as f:
        f.write('PAT_TEST,' + RUNITEM + ',' + SN + ',' + UPLIMIT + ',' + LOWLIMIT + ',' +
                passfail + ',' + NUM + ',' + LOGINFO + ',' + str(Starttime) + ',' + str(TestTime) + '\n')
        return

def getMBSN():
    os.chdir(r'C:\WinTest\Tools')
    instruct = 'EEPROM64.exe -g -mbsn -f mbsn.txt'
    os.system(instruct)
    log_name = 'mbsn.txt'
    with open(log_name, 'r', encoding='utf-8', newline='') as f:
        for line in f:
            mbsn = line
            pattern = re.compile(r'^[0-9A-Z]{23}$')
            m = pattern.match(mbsn)
            print('测试主板MB_SN:' + m.group())  # 匹配成功m.group()才会有值，匹配失败会报错
    return mbsn


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
            print('测试SN:' + m.group())  # 匹配成功m.group()才会有值，匹配失败会报错
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
                # print(str)
    os.remove(logname)
    ItemID1 = re.sub(r'\|.*$', '', str)
    ItemID = re.sub(r'\D', '', ItemID1)
    # print(ItemID)

    if rea == 0:
        para = "%s %s %s %d %s %s" % ("sdtCreateResult.exe", Fixed, ItemName, Result, ItemID, ItemTag)
        # print(para)
        os.system(para)
        res = ''
        if Result == 1:
            res = 'Pass'
        elif Result == -1:
            res = 'Fail'
        else:
            ex = Exception("Result 参数信息格式错误！！！！")
            # 抛出异常对象
            raise ex
        # 目标路径和文件名
        target = r'C:\WinTest\Log' + '\\' + ItemName + res + '.log'
        # 复制 sdtCreateResult.log
        copyfile(r'sdtCreateResult.log', target)
        return 0
    if rea == 1:
        ex = Exception("TestStand.exe窗口不存在！！！")
        # 抛出异常对象
        raise ex
    else:
        print(instruct + ' 语句执行异常')


def passlog(RUNITEM):
    logpath = r'C:\WinTest\Log' + '\\' + RUNITEM + 'Pass.log'
    res = os.path.exists(logpath)
    return res