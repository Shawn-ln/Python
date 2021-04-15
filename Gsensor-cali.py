# Coding by LiXiao
# Datatime:21/04/14 11:09 AM
# Filename:Gsensor-cali.py
# Toolby: PyCharm

import os
import support
"""
# 开头模板信息
dictor = {
    'FailRetry': '0',
    'FailRetrytimes': '1',
    'UPLIMIT': '9999.900',
    'LOWLIMIT': '-9999.900',
    'RUNITEM': 'Gsensor-Cali',
    'Errorcode': 'MBCF4',
    'tool_path': r'C:\WinTest\FFT\Sensor-Calibration',
    'instruct': 'ISSU.exe -BIST>selftest.txt',
    'result_log_name': 'selftest.txt',
    'check_item': 'Operation succeeded',
    'instruct1': 'StartWithPen.exe',
    'result_log_name1': 'StartWithPen.log',
    'check_item1': 'RESULT=PASS',
    'instruct2': 'windowscalibrationtool.exe -Calibrate A -UpdateISS -ExportAllFiles results -Minimal -noEnter 2000 >calib1.txt',
    'result_log_name2': 'calib1.txt',
    'check_item2': 'Device should be placed'
}
support.write_json(
    data=dictor,
    path=r'C:\WinTest\JSON\data',
    filename='Gsensor-cali.json'
)
"""

try:
    dictor = support.read_json(
        path=r'C:\WinTest\JSON\data',
        filename='Gsensor-cali.json'
    )
    print('dictor:', dictor)


    # 测试开始时间
    StartTime = support.titles(
        RUNITEM=dictor['RUNITEM'],
        stage='start'
    )
    for i in dictor:
        print(i + ' : ' + dictor[i])

    # 脚本路径
    currentPath = os.getcwd()
    # currentPath = r'C:\WinTest\Work'
    # print(currentPath)

    # 读取主板写入的mbsn
    MB_SN = support.getSN()

    # 测试正文
    for n in range(1, 200):
        # 测试内容和结果

        # Selftest
        selfTest = support.test(
            tool_path=dictor['tool_path'],
            act='find',
            checklist='NO',
            result_log_name=dictor['result_log_name'],
            check_item=dictor['check_item'],
            instruct=dictor['instruct'],
            check_data=''
        )
        if selfTest:
            print('selfTest pass!!!')
            support.writr_log(
                path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                date='*****************************************************\n************selfTest pass!!!*************************\n*****************************************************\n',
                act='w'
            )
            support.copy_log(
                source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                act='a'
            )

            # StartWithPen
            startWithPen = support.test(
                tool_path=dictor['tool_path'],
                act='find',
                checklist='NO',
                result_log_name=dictor['result_log_name1'],
                check_item=dictor['check_item1'],
                instruct=dictor['instruct1'],
                check_data=''
            )
            print('startWithPen:', startWithPen)
            if startWithPen:
                print('startWithPen test pass!!!')
                support.writr_log(
                    path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                    date='\n*****************************************************\nstartWithPen test pass!!!\n*****************************************************\n',
                    act='a'
                )
                # 重力感应传感器校准
                print('****************************************************')
                print('******  重力感应传感器校准开始 *************************')
                print('****************************************************')
                calibrate = support.test(
                    tool_path=dictor['tool_path'],
                    act='find',
                    checklist='NO',
                    result_log_name=dictor['result_log_name2'],
                    check_item=dictor['check_item2'],
                    instruct=dictor['instruct2'],
                    check_data=''
                )
                if calibrate:
                    print('重力感应传感器校准成功!!!')
                    result = 'pass'
                    support.writr_log(
                        path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                        date='\n*****************************************************\n********重力感应传感器校准成功!!!********************\n*****************************************************\n',
                        act='a'
                    )
                    support.copy_log(
                        source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name2']),
                        target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                        act='a'
                    )
                else:
                    print('重力感应传感器校准失败!!!')
                    result = 'fail'
            else:
                print('startWithPen test fail!!!')
                result = 'fail'
        else:
            print('selfTest fail!!!')
            result = 'fail'

        # 判断测试结果
        if result == 'fail':
            if support.judge(
                    FailRetry=dictor['FailRetry'],
                    FailRetrytimes=dictor['FailRetrytimes']
            ):
                dictor['FailRetry'] = str(int(dictor['FailRetry']) + 1)
                print('测试循环次数：' + dictor['FailRetry'], '，测试结果：fail！！！')
                continue

            # creatResult
            support.creatResult(
                Fixed=r'%~dp0',
                ItemName=dictor['RUNITEM'],
                Result=-1,
                ItemTag=0
            )
            # setinfo
            support.setinfo(
                RUNITEM=dictor['RUNITEM'],
                SN=MB_SN,
                Result='F',
                NUM='0',
                LOGINFO=dictor['RUNITEM'] + ' Fail',
                Starttime=StartTime
            )
            print('测试循环次数:', n, '，测试结果：fail！！！！')
            support.message(
                Code=dictor['Errorcode']
            )
            break

        elif result == 'pass':
            # os.system(r'call \WinTest\tools\FileLog.cmd \WinTest\LogFile\%s.log' % dictor['RUNITEM'])
            support.FileLog(item=dictor['RUNITEM'])
            print('测试循环次数:', n, '，测试结果：pass！！！')
            print('测试SN:', MB_SN)
            # creatResult
            support.creatResult(
                Fixed=r'%~dp0',
                ItemName=dictor['RUNITEM'],
                Result=1,
                ItemTag=0
            )
            # setinfo
            support.setinfo(
                RUNITEM=dictor['RUNITEM'],
                SN=MB_SN,
                Result='P',
                NUM='1',
                LOGINFO=dictor['RUNITEM'] + ' Pass',
                Starttime=StartTime
            )
            break

        else:
            print('无测试结果！！！')


except AttributeError as e:
    print(e)
    print("SN匹配信息错误，请检查正则表达式！！！")

except Exception as e:
    print(e)
