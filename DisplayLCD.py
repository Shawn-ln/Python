# Coding by LiXiao
# Datatime:21/04/16 2:54 PM
# Filename:DisplayLCD.py
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
    'RUNITEM': 'DisplayLCD',
    'Errorcode': 'MBCF4',
    'tool_path': r'C:\WinTest\FFT\DisplayLCD',
    'instruct': r'DisplayLCD.exe',
    'result_log_name': 'test_box.TXT',
    'kill_lists': ['DisplayLCD.exe']
}
support.write_json(
    data=dictor,
    path=r'C:\WinTest\JSON\data',
    filename='DisplayLCD.json'
)
"""

try:
    dictor = support.read_json(
        path=r'C:\WinTest\JSON\data',
        filename='DisplayLCD.json'
    )
    print('dictor:', dictor)

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
        # show 二维码
        os.chdir(r'C:\WinTest\FFT\QRCode')
        os.system(r'ShowQRCode.exe %s' % MB_SN)
        # 测试内容和结果
        support.killer(
            lists=dictor['kill_lists']
        )
        # 最小化测试窗口
        os.chdir(r'C:\WinTest\Tools')
        os.system(r'MiniTS.exe Min')

        support.del_log(
            log_path=r'C:\WinTest\FFT\DisplayLCD\DisplayLCD_Dbg.Log'
        )

        os.chdir(r'C:\WinTest\FFT\DisplayLCD')
        if not os.path.exists('SN.TXT'):
            support.writr_log(
                path=r'C:\WinTest\FFT\DisplayLCD\SN.TXT',
                date=R'Serial Number = 0x04 : "%s"' % MB_SN,
                act='w'
            )
        os.system(r'DisplayLCD.exe')

        # 最大化测试窗口
        os.chdir(r'C:\WinTest\Tools')
        os.system(r'MiniTS.exe Max')
        support.writr_log(
            path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
            date=R'Serial Number = 0x04 : "%s"' % MB_SN,
            act='w'
        )

        result = 'pass'

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
    print("SN匹配信息错误，请检查正则表达式！！！")
    print(e)
    support.message_showinfo('ERROR', e)

except Exception as e:
    print(e)
    support.message_showinfo('ERROR', e)
