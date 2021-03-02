# Coding by LiXiao
# Datatime:3/1/2021 2:28 PM
# Filename:WriteDMI.py
# Toolby: PyCharm
import os
import support

dictor = {
    'FailRetry':'0',
    'FailRetrytimes':'10',
    'UPLIMIT':'9999.900',
    'LOWLIMIT':'-9999.900',
    'RUNITEM':'WriteDMI',
    'Errorcode':'MBCF4',
    'tool_path':'C:\WinTest\Tools',
    'instruct':'call BiosVersion_x64.exe >BIOSVER.BAT',
    'result_log_name':'BIOSVER.BAT',
    'check_item':'BiosVersion',
    'DBS' : '172.24.249.12',    # DatabaseServer
    'DBN' : 'MESFA',            # DatabaseName
    'SYS' : 'NCBD',             # system
    'STAT' : 'GETMESBOM',       # station
    'STEP' : 'REQUEST',         # step
    'RFP' : 'MB_SN.TXT'         # RequestFilePath
}

try:
    # 测试开始时间
    StartTime = support.titles(RUNITEM=dictor['RUNITEM'], stage='start')
    for i in dictor:
        print(i + ' : ' + dictor[i])

    # 脚本路径
    currentPath = os.getcwd()
    # currentPath = r'C:\WinTest\Work'
    # print(currentPath)

    # 读取主板写入的mbsn
    MB_SN = support.getMBSN()

    # 判断是否有测试pass的log记录
    if support.passlog(dictor['RUNITEM']):
        # creatResult
        support.creatResult(Fixed=currentPath, ItemName=dictor['RUNITEM'], Result=1, ItemTag=0)
    else:
        # 测试正文
        for n in range(1, 200):

            # 删除历史遗留测试log
            support.del_log(log_path=r'C:\WinTest\Tools\mbsn.txt')
            support.del_log(log_path=r'C:\WinTest\Tools\MB_SN.TXT')
            # support.del_log(log_path=r'C:\WinTest\Tools\Response.bat')
            # 测试内容和结果
            # 获取 Response.bat
            # res = support.MonitorAgent64(DatabaseServer=dictor['DBS'], DatabaseName=dictor['DBN'],
            #                              system=dictor['SYS'], station=dictor['STAT'], step=dictor['STEP'],
            #                              RequestFilePath=dictor['RFP'], SN=MB_SN)
            # Write DMI
            pn = support.get_response_info(param='SET SubSeries')[0:25]
            print(pn)
            mt = support.get_response_info(param='SET Cust_PN_1')[0:10]
            print(mt)
            ln = support.get_response_info(param='SET SN')[0:8]
            print(ln)
            KB_PN = support.get_response_info(param='SET KBPN')[0:13]
            print(KB_PN)
            KBID = support.get_csv_info(log_name='KB.CSV', param=KB_PN)[17:18]
            print(KBID)
            osp = support.get_response_info(param='SET MTM_DPKPN')[0:10]
            print(osp)
            oa3keyid = support.get_response_info(param='SET ProductkeyID')[0:13]
            print(oa3keyid)
            support.wrtDMI(var='pn', vaule=pn)
            support.wrtDMI(var='fd', vaule=pn)
            support.wrtDMI(var='mt', vaule=mt)
            support.wrtDMI(var='ln', vaule=ln)
            support.wrtDMI(var='bt', vaule='C')
            support.wrtDMI(var='pjn', vaule='LNVNB161216')
            support.wrtDMI(var='oss', vaule='WIN')
            support.wrtDMI(var='kd', vaule=KBID)
            support.wrtDMI(var='osp', vaule=osp)
            support.wrtDMI(var='oa3keyid', vaule=oa3keyid)

            Errorcode = '.'
            chkbios = 1
            chkec = 1
            if chkbios:
                if chkec:
                    result = 'pass'
                else:
                    Errorcode = 'HS946'
                    result = 'fail'
            else:
                Errorcode = 'MBCF4'
                result = 'fail'

            # 判断测试结果
            if result == 'fail':
                if support.judge(FailRetry=dictor['FailRetry'], FailRetrytimes=dictor['FailRetrytimes']):
                    dictor['FailRetry'] = str(int(dictor['FailRetry']) + 1)
                    print('测试循环次数：' + dictor['FailRetry'], '，测试结果：fail！！！')
                    continue

                # 计算测试时间
                TestTimes = support.gettesttime(start=StartTime)
                print('测试用时:', TestTimes)
                # creatResult
                support.creatResult(Fixed=currentPath, ItemName=dictor['RUNITEM'], Result=-1, ItemTag=0)
                # setinfo
                support.setinfo(RUNITEM=dictor['RUNITEM'], SN=MB_SN, UPLIMIT=dictor['UPLIMIT'],
                                LOWLIMIT=dictor['LOWLIMIT'], Result='F', NUM='0',
                                LOGINFO=dictor['RUNITEM'] + ' Fail', Starttime=StartTime, TestTime=TestTimes)
                print('测试循环次数:', n, '，测试结果：fail！！！！')
                support.message(Code=Errorcode)
                break

            elif result == 'pass':
                print('测试循环次数:', n, '，测试结果：pass！！！')
                print('测试SN:', MB_SN)
                # 计算测试时间
                TestTimes = support.gettesttime(start=StartTime)
                print('测试用时:', TestTimes)
                # creatResult
                support.creatResult(Fixed=currentPath, ItemName=dictor['RUNITEM'], Result=1, ItemTag=0)
                # setinfo
                support.setinfo(RUNITEM=dictor['RUNITEM'], SN=MB_SN, UPLIMIT=dictor['UPLIMIT'],
                                LOWLIMIT=dictor['LOWLIMIT'], Result='P', NUM='1',
                                LOGINFO=dictor['RUNITEM'] + ' Pass', Starttime=StartTime, TestTime=TestTimes)
                break

            else:
                print('无测试结果！！！')


except AttributeError as e:
    print(e)
    print("SN匹配信息错误，请检查正则表达式！！！")

except Exception as e:
    print(e)
