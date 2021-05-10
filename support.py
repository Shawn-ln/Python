# Coding by LiXiao
# Datatime:2/26/2021 11:37 AM
# Filename:support.py
# Toolby: PyCharm

import os
import re
import datetime
import tkinter
from tkinter import messagebox
from shutil import copyfile
import json


def flash_bios(path, ver):
    Chk_AC = test(
        tool_path=path,
        act='find',
        checklist='NO',
        result_log_name='ACstatus.bat',
        check_item='AC_ST=ON_LINE',
        instruct='CheckAC.exe /set >ACstatus.bat',
        check_data=''
    )
    print(Chk_AC)
    if Chk_AC:
        os.chdir(path)
        os.system('call %s.exe' % ver)
    else:
        ex = Exception('电源线|电池未接入不可升级BIOS，请接入电源线先后重试')
        # 抛出异常对象
        raise ex


def killer(lists):
    for i in lists:
        os.system('taskkill /f /im "%s" /t' % i)
    return True


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


def save_jsondata(save_name, save_param, get_param, get_path, splits, take_numbers):
    if not get_path == 'NONE':
        with open(get_path, 'r', encoding='utf-8', newline='') as f:
            res = f.readlines()
            print('res:', res)
            for line in res:
                if get_param in line:
                    save_data = line.split(splits[0])[take_numbers[0]].split(splits[1])[take_numbers[1]].strip()
        print('save_data:', save_data)
        with open(save_name, 'a', encoding='utf-8', newline='') as f:
            f.write(save_param + save_data)
    else:
        with open(save_name, 'a', encoding='utf-8', newline='') as f:
            f.write(save_param + get_param)
    return


def del_log(log_path):
    res = os.path.exists(log_path)
    if res:
        os.remove(log_path)
        print('文件已成功删除！！！', log_path)
    else:
        print('文件不存在，无需删除！！！', log_path)
    return


def FileLog(item):
    if os.path.exists(r'C:\WinTest\LogFile\Response.bat'):
        print('Response.bat文件已找到！！！')
    elif os.path.exists(r'C:\WinTest\Tools\Response.bat'):
        print('Response.bat文件已找到！！！')
    else:
        ex = Exception('Response.bat文件未找到！！！')
        # 抛出异常对象
        raise ex
    STAGE_CODE = 'MP'
    responselists = get_response_info(
        lists=['MODEL', 'Line', 'STATION', 'STATUS', 'SN', 'WO', 'Cust_PN'],
        date=['SET MODEL', 'SET LINE', 'SET STATION', 'SET STATUS', 'SET SN', 'SET WO', 'SET Cust_PN_1']
    )
    print('responselists:', responselists)
    if responselists['Cust_PN'] == 'TBD':
        STAGE_CODE = 'FVT'
    if str(responselists['MODEL'] + 'FVT') == responselists['Cust_PN'][0:9]:
        STAGE_CODE = 'FVT'
    if str(responselists['MODEL'] + 'SIT') == responselists['Cust_PN'][0:9]:
        STAGE_CODE = 'SIT'
    if str(responselists['MODEL'] + 'SVT') == responselists['Cust_PN'][0:9]:
        STAGE_CODE = 'SVT'
    # print(str(lists['MODEL']+'FVT'), lists['MODEL']+'FVT', lists['MODEL']+'SIT', lists['MODEL']+'SVT', lists['Cust_PN'][0:9], STAGE_CODE)
    # write_json(
    #     data=lists,
    #     path=r'C:\WinTest\JSON\data',
    #     filename='FileLog_%s.json' % item
    # )
    i = str(datetime.datetime.now())
    # print(i)
    date = i[0:10]
    time = i[11:19]
    print('date:', date, 'time:', time)
    log_data = list()
    count = 0
    if not os.path.exists(r'C:\Wintest\LogFile\Filelog.log'):
        log_data = ['[init...]',
                    '\nSTARTDATE=' + date,
                    '\nSTARTTIME=' + time,
                    '\nPROJECT_NAME=' + responselists['MODEL'],
                    '\nSTAGE_CODE=' + STAGE_CODE,
                    '\nLINE=' + responselists['Line'],
                    '\nSTATION=' + responselists['STATION'],
                    '\nDEVICEID=' + responselists['STATUS'],
                    '\nISN=' + responselists['SN'],
                    '\nWO=' + responselists['WO'],
                    '\n[=========================================== LOG START ===========================================]\n']
        print(log_data)
    else:
        if not os.path.exists(r'C:\Wintest\LogFile\count.txt'):
            ex = Exception(r'即将打开的文件 C:\Wintest\LogFile\count.txt 不存在！！！')
            # 抛出异常对象
            raise ex
        with open(r'C:\Wintest\LogFile\count.txt', 'r+', encoding='utf-8') as f:
            data = f.readlines()
            for line in data:
                # print(line)
                count = int(line.strip()) + 1
    log_data.append('%s %s\n' % (date, time))
    log_data.append('[TESTITEM%s=%s]\n' % (count, item))
    for x in range(0, len(log_data)):
        print(log_data[x])
    print('count:', count)
    with open(r'C:\Wintest\LogFile\Filelog.log', 'a', encoding='utf-8') as f:
        for i in range(0, len(log_data)):
            f.write(log_data[i])
    copy_log(
        source_path=r'C:\WinTest\LogFile\%s.log' % item,
        target_path=r'C:\Wintest\LogFile\Filelog.log',
        act='a'
    )
    writr_log(
        path=r'C:\WinTest\LogFile\count.txt',
        date=str(count),
        act='w'
    )
    writr_log(
        path=r'C:\Wintest\LogFile\Filelog.log',
        date='\n===========================================测试项分界线===========================================\n\n',
        act='a'
    )
    return


def copy_log(source_path, target_path, act):
    print('source_path:', source_path, 'target_path:', target_path)

    with open(source_path, 'r+', encoding='utf-8') as f:
        date = f.readlines()
    print('date:', date)
    with open(target_path, act, encoding='utf-8') as g:
        for line in date:
            g.write(line)
    return


def read_json(path, filename):
    if not os.path.exists(r'%s\%s' % (path, filename)):
        ex = Exception(r'即将打开的文件 %s\%s 不存在！！！' % (path, filename))
        # 抛出异常对象
        raise ex
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
    if not os.path.exists(r'C:\win\FRTITEM\Battery\battery.log'):
        ex = Exception(r'即将打开的文件 C:\win\FRTITEM\Battery\battery.log 不存在！！！')
        # 抛出异常对象
        raise ex
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
    if checklist == 'YES':
        print('check_item:', check_item)
        result = dict()
        os.chdir(tool_path)
        del_log(r'%s\%s' % (tool_path, result_log_name))
        res = os.system(instruct)
        if not os.path.exists(result_log_name):
            ex = Exception(result_log_name + '不存在,请勿手动关闭测试窗口！！！')
            # 抛出异常对象
            raise ex
        print(instruct, res)

        for i in range(0, len(check_item)):
            print(check_item[i])
            if act == 'write':
                with open(result_log_name, 'w', encoding='utf-8', newline='') as f:
                    if f.write(check_data) == 0:
                        return True
                return False
            if not os.path.exists(r'%s\%s' % (tool_path, result_log_name)):
                ex = Exception(r'即将打开的文件 %s\%s 不存在！！！' % (tool_path, result_log_name))
                # 抛出异常对象
                raise ex
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
                        if act == 'match':
                            result = check_data[check_item[i]]
                            return result
        return result

    elif checklist == 'NO':
        os.chdir(tool_path)
        del_log(r'%s\%s' % (tool_path, result_log_name))
        if act == 'write':
            with open(result_log_name, 'w', encoding='utf-8', newline='') as f:
                if f.write(check_data) == 0:
                    return True
            return False
        res = os.system(instruct)
        if not os.path.exists(result_log_name):
            ex = Exception(result_log_name + '不存在,请勿手动关闭测试窗口！！！')
            # 抛出异常对象
            raise ex
        print(instruct, res)
        if not os.path.exists(r'%s\%s' % (tool_path, result_log_name)):
            ex = Exception(r'即将打开的文件 %s\%s 不存在！！！' % (tool_path, result_log_name))
            # 抛出异常对象
            raise ex
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
    if not os.path.exists(r'C:\WinTest\Tools\WIFIBTMAC.BAT'):
        ex = Exception(r'即将打开的文件 C:\WinTest\Tools\WIFIBTMAC.BAT 不存在！！！')
        # 抛出异常对象
        raise ex
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
        if not os.path.exists(r'%s\%s' % (file_path, file_name)):
            ex = Exception(r'即将打开的文件 %s\%s 不存在！！！' % (file_path, file_name))
            # 抛出异常对象
            raise ex
        with open(file_name, 'r', encoding='utf-8', newline='') as f:
            for line in f.readlines():
                if param in line:
                    strs = re.sub(r'^.*=', '', line).strip()
                    return strs
    if act == 'find':
        if not os.path.exists(r'%s\%s' % (file_path, file_name)):
            ex = Exception(r'即将打开的文件 %s\%s 不存在！！！' % (file_path, file_name))
            # 抛出异常对象
            raise ex
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
        if not os.path.exists(r'C:\WinTest\HW\HWDATA\%s' % log_name_list[i]):
            ex = Exception(r'即将打开的文件 C:\WinTest\HW\HWDATA\%s 不存在！！！' % log_name_list[i])
            # 抛出异常对象
            raise ex
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


def message_showinfo(message_type, message_data):
    top = tkinter.Tk()  # *********
    top.withdraw()      # ****实现主窗口隐藏
    top.update()        # *********需要update一下
    messagebox.showinfo(message_type, message_data)
    top.destroy()
    return


def get_response_info(lists, date):
    os.chdir(r'C:\WinTest\Tools')
    log_name = 'Response.bat'
    if not os.path.exists(r'C:\WinTest\Tools/%s' % log_name):
        copyfile(
            src=r'C:\WinTest\LogFile/%s' % log_name,
            dst=r'C:\WinTest\Tools/%s' % log_name
        )
    result = dict()
    for i in range(0, len(lists)):
        if not os.path.exists(r'C:\WinTest\Tools\%s' % log_name):
            ex = Exception(r'即将打开的文件 C:\WinTest\Tools\%s 不存在！！！' % log_name)
            # 抛出异常对象
            raise ex
        with open(log_name, 'r', encoding='ANSI', newline='') as f:
            for line in f.readlines():
                sts = '.'
                print(date[i], line)
                if date[i] in line:
                    # 截取'param='后面的内容
                    sts = re.sub(r'^.*=', '', line).rstrip()  # rstrip()—>right strip(),清除了右边末尾的空格
                    # print('sts:', sts)
                    result[lists[i]] = sts
                    break
    return result
    # ex = Exception(param + "信息在Response.bat未找到！！！")
    # # 抛出异常对象
    # raise ex


def MonitorAgent64(DatabaseServer, DatabaseName, system, station, step, RequestFilePath, SN):
    path = r'C:\WinTest\Tools'
    os.chdir(path)
    with open(RequestFilePath, 'w', encoding='utf-8', newline='') as f:
        f.write('MBSN=' + SN)
    instruct1 = 'MonitorAgent64.exe %s %s %s %s %s %s' % (
    DatabaseServer, DatabaseName, system, station, step, RequestFilePath)
    os.system(instruct1)


def get_ini_info(param):
    os.chdir(r'C:\WinTest')
    logname = 'Model_ini.BAT'
    if not os.path.exists(r'C:\WinTest\Model_ini.BAT'):
        ex = Exception(r'即将打开的文件 C:\WinTest\Model_ini.BAT 不存在！！！')
        # 抛出异常对象
        raise ex
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


def writr_log(path, date, act):
    with open(path, act, encoding='utf-8', newline='') as f:
        f.write(date)
    return True


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
        f.write('PAT_TEST,' + SN + ',' + RUNITEM + ',' + str(Starttime) + ',' + str(
            EndTimes) + ',' + Result + ',' + NUM + ',' + LOGINFO + ',' + str(TestTimes) + '\n')
        return


def getMBSN():
    os.chdir(r'C:\WinTest\Tools')
    instruct = 'EEPROM64.exe -g -mbsn -f mbsn.txt'
    os.system(instruct)
    log_name = 'mbsn.txt'
    if not os.path.exists(r'C:\WinTest\Tools\%s' % log_name):
        ex = Exception(r'即将打开的文件 C:\WinTest\Tools\%s 不存在！！！' % log_name)
        # 抛出异常对象
        raise ex
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
    if not os.path.exists(r'C:\WinTest\Tools\%s' % log_name):
        ex = Exception(r'即将打开的文件 C:\WinTest\Tools\%s 不存在！！！' % log_name)
        # 抛出异常对象
        raise ex
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
    log_name = ItemName + '.txt'
    # print(logname)
    strs = '.'
    if not os.path.exists(r'C:\WinTest\TestStand\%s' % log_name):
        ex = Exception(r'即将打开的文件 C:\WinTest\TestStand\%s 不存在！！！' % log_name)
        # 抛出异常对象
        raise ex
    with open(log_name, 'r', encoding='utf-8', newline='') as f:
        for line in f.readlines():
            if ItemName in line:
                strs = line
                # print(str)
    # os.remove(logname)
    ItemID1 = re.sub(r'\|.*$', '', strs)
    ItemID = re.sub(r'\D', '', ItemID1)
    print('ItemID:', ItemID)

    if rea == 0:
        para = "%s %s %s %d %s %s" % ("sdtCreateResult.exe", Fixed, ItemName, Result, ItemID, ItemTag)
        print(para)
        os.system(para)
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
        return res
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
            if not os.path.exists(r'C:\WinTest\Tools\%s' % filename):
                ex = Exception(r'即将打开的文件 C:\WinTest\Tools\%s 不存在！！！' % filename)
                # 抛出异常对象
                raise ex
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
