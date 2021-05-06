# Coding by LiXiao
# Datatime:21/04/16 2:37 PM
# Filename:Touchpanel.py
# Toolby: PyCharm


import os
import time
import support

"""
# 开头模板信息
dictor = {
    'FailRetry': '0',
    'FailRetrytimes': '0',
    'UPLIMIT': '9999.900',
    'LOWLIMIT': '-9999.900',
    'RUNITEM': 'TouchPanel',
    'Errorcode': 'MBCF4',
    'tool_path': r'C:\WinTest\FFT\TouchPanel',
    'instruct': r'MultiTouch.exe',           # 多指测试
    'result_log_name': 'MultiTouch.log',     # 多指测试
    'check_item': 'Result=PASS',             # 多指测试
    'instruct1': 'TouchPanel.exe SETTING.CSV',    # 划线测试
    'result_log_name1': 'TouchPanel.log',         # 划线测试
    'check_item1': 'Result=PASS'                  # 划线测试
}
support.write_json(
    data=dictor,
    path=r'C:\WinTest\JSON\data',
    filename='TouchPanel.json'
)
"""

try:
    dictor = support.read_json(
        path=r'C:\WinTest\JSON\data',
        filename='TouchPanel.json'
    )
    print('dictor:', dictor)

    LCD = support.read_json(
        path=r'C:\WinTest\LogFile',
        filename='HWConfig.json'
    )['Config_LCD']['LCDTYPE']
    print('LCD:', LCD)

    # 测试开始时间
    StartTime = support.titles(
        RUNITEM=dictor['RUNITEM'],
        stage='start'
    )

    # 脚本路径
    currentPath = os.getcwd()
    # currentPath = r'C:\WinTest\Work'
    # print(currentPath)

    # 读取主板写入的mbsn
    MB_SN = support.getSN()

    # 测试正文
    for n in range(1, 200):
        if LCD == 'NOTOUCH':
            print('此配置为NOTOUCH，不需测试TouchPanel！！！')
            result = 'pass'
            support.writr_log(
                path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                date='此配置为%s，不需测试TouchPanel！！！' % LCD,
                act='w'
            )
        elif LCD == 'TOUCH':
            multitouch = support.test(
                tool_path=dictor['tool_path'],
                act='find',
                checklist='NO',
                result_log_name=dictor['result_log_name'],
                check_item=dictor['check_item'],
                instruct=dictor['instruct'],
                check_data=''
            )
            print('multitouch:', multitouch)
            if multitouch:
                print('多指测试PASS')
                support.copy_log(
                    source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                    target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                    act='w'
                )
                touch = support.test(
                    tool_path=dictor['tool_path'],
                    act='find',
                    checklist='NO',
                    result_log_name=dictor['result_log_name1'],
                    check_item=dictor['check_item1'],
                    instruct=dictor['instruct1'],
                    check_data=''
                )
                print('touch:', touch)
                if touch:
                    print('多指测试PASS')
                    result = 'pass'
                    support.copy_log(
                        source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name1']),
                        target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                        act='a'
                    )
                else:
                    print('TouchPanel test fail')
                    result = 'fail'
            else:
                print('多指测试FAIL')
                result = 'fail'
        else:
            print('LCD Type获取失败，请检查配置信息！！！')
            ex = Exception('LCD Type获取失败，请检查配置信息！！！')
            # 抛出异常对象
            raise ex

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
