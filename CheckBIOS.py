# Coding by LiXiao
# Datatime:2/26/2021 5:37 PM
# Filename:CheckBIOS.py
# Toolby: PyCharm
import os
import support

# 开头模板信息
dictor = {
    'FailRetry':'0',
    'FailRetrytimes':'10',
    'UPLIMIT':'9999.900',
    'LOWLIMIT':'-9999.900',
    'RUNITEM':'CheckBIOS',
    'Errorcode':'MBCF4',
    'tool_path':'C:\WinTest\Tools',
    'instruct':'call BiosVersion_x64.exe >BIOSVER.BAT',
    'result_log_name':'BIOSVER.BAT',
    'check_item':'BiosVersion',
    'instruct1': 'call ECVersion_NB6067.exe',
    'result_log_name1':'ECVersion_NB6067.BAT',
    'check_item1':'EC_VER',
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
            # 测试内容和结果

            # 读取Model_ini.BAT中Model信息
            MODEL = support.get_ini_info(param='Model')
            print(MODEL)
            BIOSver = support.get_ini_info(param='BIOSver')
            print(BIOSver)
            ECver = support.get_ini_info(param='ECver')
            print(ECver)
            print('测试正文')
            chkbios = support.test(tool_path=dictor['tool_path'], result_log_name=dictor['result_log_name'],
                         check_item=dictor['check_item'], instruct=dictor['instruct'],
                         check_data=BIOSver)
            chkec = support.test(tool_path=dictor['tool_path'], result_log_name=dictor['result_log_name1'],
                         check_item=dictor['check_item1'], instruct=dictor['instruct1'],
                         check_data=ECver)
            Errorcode = '.'
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

