# Coding by LiXiao
# Datatime:3/1/2021 2:28 PM
# Filename:WriteDMI.py
# Toolby: PyCharm
import os
import support

dictor = {
    'FailRetry':'0',
    'FailRetrytimes':'3',
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
            pn = support.get_response_info(param='SET SubSeries')
            fd = support.get_response_info(param='SET SubSeries')
            mt = support.get_response_info(param='SET Cust_PN_1')
            ln = support.get_response_info(param='SET SN')
            KB_PN = support.get_response_info(param='SET KBPN')
            KBID = support.get_csv_info(log_name='KB.CSV', param=KB_PN)[17:18]
            osp = support.get_response_info(param='SET MTM_DPKPN')
            oa3keyid = support.get_response_info(param='SET ProductkeyID')

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

            # Read & Check DMI
            res = ['fail'] * 10
            OA3Key = support.getDMI(var='oa3keyid', filaname='OA3Key.txt')
            res[0] = support.is_equal(a=oa3keyid, b=OA3Key, c='OA3Key')
            ProductName = support.getDMI(var='pn', filaname='Product_Name.txt')
            res[1] = support.is_equal(a=pn, b=ProductName, c='ProductName')
            MTMPN = support.getDMI(var='mt', filaname='MTMPN.txt')
            res[2] = support.is_equal(a=mt, b=MTMPN, c='MTMPN')
            LenovoSN = support.getDMI(var='ln', filaname='LenovoSN.txt')
            res[3] = support.is_equal(a=ln, b=LenovoSN, c='LenovoSN')
            Brandtype = support.getDMI(var='bt', filaname='Brandtype.txt')
            res[4] = support.is_equal(a='C', b=Brandtype, c='Brandtype')
            FamilyName = support.getDMI(var='fd', filaname='FamilyName.txt')
            res[5] = support.is_equal(a=fd, b=FamilyName, c='FamilyName')
            ProjectName = support.getDMI(var='pjn', filaname='ProjectName.txt')
            res[6] = support.is_equal(a='LNVNB161216', b=ProjectName, c='ProjectName')
            OS_Descriptor = support.getDMI(var='oss', filaname='OS_Descriptor.txt')
            res[7] = support.is_equal(a='WIN', b=OS_Descriptor, c='OS_Descriptor')
            Keyboard_ID = support.getDMI(var='kd', filaname='Keyboard_ID.txt')
            res[8] = support.is_equal(a=KBID, b=Keyboard_ID, c='Keyboard_ID')
            DPKPN = support.getDMI(var='osp', filaname='DPKPN.txt')
            res[9] = support.is_equal(a=osp, b=DPKPN, c='DPKPN')
            result = ''
            Errorcode = ''
            for x in res:
                if x == False:
                    result = 'fail'
                    Errorcode = 'HS910'
                    break
                elif x == True:
                    result = 'pass'
                else:
                    ex = Exception('DMI Check 结果异常！！！', x)
                    # 抛出异常对象
                    raise ex


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
