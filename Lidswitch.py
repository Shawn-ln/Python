# Coding by LiXiao
# Datatime:3/4/2021 2:25 PM
# Filename:Lidswitch.py
# Toolby: PyCharm
import os
import support

# 开头模板信息
dictor = {
    'FailRetry': '0',
    'FailRetrytimes': '10',
    'UPLIMIT': '9999.900',
    'LOWLIMIT': '-9999.900',
    'RUNITEM': 'Lidswitch',
    'Errorcode': 'MBCF4',
    'tool_path': 'C:\WinTest\FFT\LidSwitch',
    'instruct1': 'SwitchLid.exe -E',
    'result_log_name1': 'LID.log',
    'check_item1': 'Disable LID Successful',
    'instruct2': 'WinLidSw.exe',
    'result_log_name2': 'WinLidSw.log',
    'check_item2': 'Result=PASS'
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
    MB_SN = support.getSN()

    # 判断是否有测试pass的log记录
    if 1 == 0:
        # creatResult
        support.creatResult(Fixed=currentPath, ItemName=dictor['RUNITEM'], Result=1, ItemTag=0)
    else:
        # 测试正文
        for n in range(1, 200):
            # 测试内容和结果

            print('测试正文')
            LID = support.test(tool_path=dictor['tool_path'], act='find', result_log_name=dictor['result_log_name2'],
                               check_item=dictor['check_item2'], instruct=dictor['instruct2'],
                               check_data='PASS')
            Errorcode = '.'
            print('LID:', LID)
            if LID:
                result = 'pass'
            else:
                Errorcode = 'MBCF4'
                result = 'fail'

            # 判断测试结果
            if result == 'fail':
                if support.judge(FailRetry=dictor['FailRetry'], FailRetrytimes=dictor['FailRetrytimes']):
                    dictor['FailRetry'] = str(int(dictor['FailRetry']) + 1)
                    print('测试循环次数：' + dictor['FailRetry'], '，测试结果：fail！！！')
                    continue

                # creatResult
                support.creatResult(Fixed=currentPath, ItemName=dictor['RUNITEM'], Result=-1, ItemTag=0)
                # setinfo
                support.setinfo(RUNITEM=dictor['RUNITEM'], SN=MB_SN, Result='F', NUM='0',
                                LOGINFO=dictor['RUNITEM'] + ' Fail', Starttime=StartTime)
                print('测试循环次数:', n, '，测试结果：fail！！！！')
                support.message(Code=Errorcode)
                break

            elif result == 'pass':
                print('测试循环次数:', n, '，测试结果：pass！！！')
                print('测试SN:', MB_SN)
                # creatResult
                support.creatResult(Fixed=currentPath, ItemName=dictor['RUNITEM'], Result=1, ItemTag=0)
                # setinfo
                support.setinfo(RUNITEM=dictor['RUNITEM'], SN=MB_SN, Result='P', NUM='1',
                                LOGINFO=dictor['RUNITEM'] + ' Pass', Starttime=StartTime)
                break

            else:
                print('无测试结果！！！')


except AttributeError as e:
    print(e)
    print("SN匹配信息错误，请检查正则表达式！！！")

except Exception as e:
    print(e)
