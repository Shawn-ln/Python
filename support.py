# Coding by LiXiao
# Datatime:2/26/2021 11:37 AM
# Filename:support.py
# Toolby: PyCharm

import os
import re
import datetime
from shutil import copyfile
import json


def write_json(data, path, filename):
    os.chdir(path)
    del_log(path + '\\' + filename)
    with open(filename, 'w+', encoding='utf-8', newline='') as f:
        # f.write(write_data)
        json.dump(
            obj=data,
            fp=f,
            indent=3,
            ensure_ascii=False
        )
    return True


def read_json(path, filename):
    os.chdir(path)
    with open(filename, 'r+', encoding='utf-8') as f:
        # print(f.readlines())
        # res = json.loads(str(f.readlines()))
        res = json.load(f)
        # print(type(res), res)
        return res

def judge_battery(lowlimit, highlimit):
    if lowlimit > highlimit:
        ex = Exception('judge_battery() 参数值错误')
        # 抛出异常对象
        raise ex
    os.chdir(r'C:\win\FRTITEM\Battery')
    instruct = 'ACStatus.exe -c %d %d>battery.log' % (lowlimit, highlimit)
    res = os.system(instruct)
    print('res', res)
    rsoc = '.'
    with open('battery.log', 'r', encoding='utf-8', newline='') as f:
        for line in f.readlines():
            if 'RSOC:' in line:
                rsoc = re.sub('^.*:', '', line).strip()
                print('rsoc', rsoc)
            if 'Battery RSOC Test PASS' in line:
                print('电池电量:%s ,在 %d - %d 范围内，检查PASS' % (rsoc, lowlimit, highlimit))
                return False
            else:
                return True


def test(tool_path, result_log_name, checklist, act, check_item, instruct, check_data):
    print('check_item:', check_item)
    if checklist == 'YES':
        print('check_item:', check_item)
        result = dict()
        os.chdir(tool_path)
        res = os.system(instruct)
        print(instruct, res)
        for i in range(0, len(check_item)):
            print(check_item[i])
            if act == 'write':
                with open(result_log_name, 'w', encoding='utf-8', newline='') as f:
                    if f.write(check_data) == 0:
                        return True
                return False
            with open(result_log_name, 'r', encoding='utf-8', newline='') as f:
                for line in f.readlines():
                    print(line)
                    if check_item[i] in line:
                        if act == 'judge':
                            # 截取'param='后面的内容
                            strs = re.sub(r'^.*=', '', line).strip()
                            if check_data == strs:
                                # print(strs)
                                result[check_item[i]] = strs
                        if act == 'find':
                            return True
                        if act == 'read':
                            strs = re.sub(r'^.*=', '', line).strip()
                            result[check_item[i]] = strs

        return result

    elif checklist == 'NO':
        os.chdir(tool_path)
        if act == 'write':
            with open(result_log_name, 'w', encoding='utf-8', newline='') as f:
                if f.write(check_data) == 0:
                    return True
            return False
        res = os.system(instruct)
        print(instruct, res)
        with open(result_log_name, 'r', encoding='utf-8', newline='') as f:
            for line in f.readlines():
                print(line)
                if check_item in line:
                    if act == 'judge':
                        # 截取'param='后面的内容
                        strs = re.sub(r'^.*=', '', line).strip()
                        if check_data == strs:
                            # print(strs)
                            return True
                    if act == 'find':
                        return True
                    if act == 'read':
                        strs = re.sub(r'^.*=', '', line).strip()
                        return strs
        return False
    else:
        ex = Exception('checklist参数错误，只能为Y/N，实际为:' + checklist)
        # 抛出异常对象
        raise ex



def message(Code):
    if Code == '.':
        ex = Exception('message() 参数Errorcode传递值为错误值(.)！！！')
        # 抛出异常对象
        raise ex
    else:
        path = r'C:\WinTest\Messge'
        os.chdir(path)
        instruct1 = 'Messge.cmd ' + Code
        os.system(instruct1)
        return


def getMAC(MACID):
    os.chdir(r'C:\WinTest\Tools')
    del_log(log_path=r'C:\WinTest\Tools\WIFIBTMAC.BAT')
    instruct = 'WirelessBT-Mac_x86.exe 0 >WIFIBTMAC.BAT'
    os.system(instruct)
    strs = '.'
    with open('WIFIBTMAC.BAT', 'r', encoding='utf-8', newline='') as f:
        for line in f.readlines():
            if MACID in line:
                strs = re.sub(r'^.*=', '', line).strip()
                # print(strs)
                return strs
    return strs


def file_info(file_path, act, file_name, param):
    os.chdir(file_path)
    if act == 'write':
        with open(file_name, 'w', encoding='utf-8', newline='') as f:
            if f.write(param):
                return True
    if act == 'read':
        with open(file_name, 'r', encoding='utf-8', newline='') as f:
            for line in f.readlines():
                if param in line:
                    strs = re.sub(r'^.*=', '', line).strip()
                    return strs
    if act == 'find':
        with open(file_name, 'r', encoding='utf-8', newline='') as f:
            for line in f.readlines():
                if param in line:
                    print(line)
                    return True
    print(file_name, act, file_path, param)
    return


def get_csv_info(log_name_list, param_list, data_list):
    os.chdir(r'C:\WinTest\HW\HWDATA')
    result = dict()
    for i in range(0, len(log_name_list)):
        with open(log_name_list[i], 'r', encoding='utf-8', newline='') as f:
            for line in f.readlines():
                if param_list[i] in line:
                    strs = line.strip()
                    result[data_list[i]] = strs
                    break
    return result
    # ex = Exception(param_list + "信息在" + log_name_list +"未找到！！！")
    # # 抛出异常对象
    # raise ex


def get_response_info(lists, date):
    os.chdir(r'C:\WinTest\Tools')
    log_name = 'Response.bat'
    result = dict()
    for i in range(0, len(lists)):
        with open(log_name, 'r', encoding='utf-8', newline='') as f:
            for line in f.readlines():
                sts = '.'
                print(date[i], line)
                if date[i] in line:
                    # 截取'param='后面的内容
                    sts = re.sub(r'^.*=', '', line).rstrip()    # rstrip()—>right strip(),清除了右边末尾的空格
                    # print('sts:', sts)
                    result[lists[i]] = sts
                    break
    return result
    # ex = Exception(param + "信息在Response.bat未找到！！！")
    # # 抛出异常对象
    # raise ex


def del_log(log_path):
    res = os.path.exists(log_path)
    if res:
        os.remove(log_path)
        print('文件已成功删除！！！', log_path)
    else:
        print('文件不存在，无需删除！！！', log_path)
    return



def MonitorAgent64(DatabaseServer, DatabaseName, system, station, step, RequestFilePath, SN):
    path = r'C:\WinTest\Tools'
    os.chdir(path)
    with open(RequestFilePath, 'w', encoding='utf-8', newline='') as f:
        f.write('MBSN=' + SN)
    instruct1 = 'MonitorAgent64.exe %s %s %s %s %s %s' % (DatabaseServer, DatabaseName, system, station, step, RequestFilePath)
    os.system(instruct1)


def get_ini_info(param):
    os.chdir(r'C:\WinTest')
    logname = 'Model_ini.BAT'
    with open(logname, 'r', encoding='utf-8', newline='') as f:
        for line in f.readlines():
            if param in line:
                # 截取'param='后面的内容
                str = re.sub(r'^.*=', '', line).strip()
                return str
    ex = Exception(param + "信息在Model_ini.BAT未找到！！！")
    # 抛出异常对象
    raise ex


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


def setinfo(RUNITEM, SN, Result, NUM, LOGINFO, Starttime):
    passfail = ''
    EndTime = datetime.datetime.now()
    EndTimes = re.sub(r'\..*$', "", str(EndTime))
    d1 = datetime.datetime.strptime(Starttime, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(EndTimes, '%Y-%m-%d %H:%M:%S')
    TestTimes = d2 - d1
    print('测试用时:', TestTimes)
    if Result == 'P':
        passfail = 'PASS'
    if Result == 'F':
        passfail = 'FAIL'
    os.chdir(r'C:\WinTest\LogFile')
    logname = str('TestLog_' + passfail + '.txt')
    with open(logname, 'a', encoding='utf-8', newline='') as f:
        # f.write('PAT_TEST,' + RUNITEM + ',' + SN + ',' + UPLIMIT + ',' + LOWLIMIT + ',' + passfail + ',' + NUM + ',' + LOGINFO + ',' + str(Starttime) + ',' + str(TestTimes) + '\n')
        f.write('PAT_TEST,' + SN + ',' + RUNITEM + ',' + str(Starttime) + ',' + str(EndTimes) + ',' + Result + ',' + NUM + ',' + LOGINFO + ',' + str(TestTimes) + '\n')
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
    # r = os.popen(instruct)
    # print(instruct, r.readlines())
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
    # print(getID)
    os.system(getID)
    logname = ItemName + '.txt'
    # print(logname)
    str = '.'
    with open(logname, 'r', encoding='utf-8', newline='') as f:
        for line in f.readlines():
            if ItemName in line:
                str = line
                # print(str)
    # os.remove(logname)
    ItemID1 = re.sub(r'\|.*$', '', str)
    ItemID = re.sub(r'\D', '', ItemID1)
    # print(ItemID)

    if rea == 0:
        para = "%s %s %s %d %s %s" % ("sdtCreateResult.exe", Fixed, ItemName, Result, ItemID, ItemTag)
        print(para)
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


def wrtDMI(var_list, vaule_list):
    os.chdir(r'C:\WinTest\Tools')
    for i in range(0, len(var_list)):
        instruct = 'EEPROM64.exe -s -%s -c "%s"' % (var_list[i], vaule_list[var_list[i]])
        print(instruct)
        if os.system(instruct) == 0:
            continue
        else:
            ex = Exception(instruct + '，执行失败')
            # 抛出异常对象
            raise ex
    return


def getDMI(var_list):
    os.chdir(r'C:\WinTest\Tools')
    result = dict()
    for i in var_list:
        filename = i + '.txt'
        if os.path.exists(filename):
            os.remove(filename)
        instruct = 'EEPROM64.exe -g -%s -f %s' % (var_list[i], filename)
        print(instruct)
        res = os.system(instruct)
        if res == 0:
            strs = '.'
            with open(filename, 'r', encoding='utf-8', newline='') as f:
                for line in f.readlines():
                    strs = line.strip()
                    result[i] = strs
                    # result[var_list[i]] = strs
            if strs == '.':
                ex = Exception(var_list + ' 变量信息获取失败！！！')
                # 抛出异常对象
                raise ex
        else:
            ex = Exception('"' + instruct + '"' + ' 执行失败！！！')
            # 抛出异常对象
            raise ex
    return result


def is_equal(read_list, check_list):
    for i in read_list:
        if read_list[i] == check_list[i]:
            print('"' + i + '"' + ' Check Pass,实际写入值为："' + read_list[i] + '"，应写入值为："' + check_list[i] + '"\n')
            continue
        else:
            print('"' + i + '"' + ' Check Fail,实际写入值为："' + read_list[i] + '"，应写入值为："' + check_list[i] + '"\n')
            return False
    return True

def wrtUUID(value):
    os.chdir(r'C:\WinTest\Tools')
    instruct = 'EEPROM64.exe -s -uu -b %s' % (value)
    print(instruct)
    if os.system(instruct) == 0:
        return
    else:
        ex = Exception(instruct + '，执行失败')
        # 抛出异常对象
        raise ex


def setmsg(Errorcode, msg):
    os.chdir(r'C:\WinTest\Messge')
    filename = Errorcode + '_1.txt'
    print(filename)
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        f.write(msg)