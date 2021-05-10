# Coding by LiXiao
# Datatime:4/27/2021 7:47 PM
# Filename:AutoKeyboard.py
# Toolby: PyCharm

import os
import support
from shutil import copyfile

"""
# 开头模板信息
dictor = {
    'FailRetry': '0',
    'FailRetrytimes': '0',
    'UPLIMIT': '9999.900',
    'LOWLIMIT': '-9999.900',
    'RUNITEM': 'AutoKeyboard',
    'Errorcode': 'MBCF4',
    'tool_path': r'C:\WinTest\FFT\AutoKeyboard',
    'instruct': r'Keyboard.exe',
    'result_log_name': 'Keyboard.txt',
    'check_item': r'Result    : PASS',
    'check_data': '',
    'enableFn': [r'SwitchFnKey.exe -A', r'SwitchFnKey.exe -C', r'KeyBoardTest.exe -A'],
    'disableFn': [r'SwitchFnKey.exe -E', r'SwitchFnKey.exe -B', r'SwitchFnKey.exe -D', r'KeyBoardTest.exe -B']
}
support.write_json(
    data=dictor,
    path=r'C:\WinTest\JSON\data',
    filename='AutoKeyboard.json'
)
"""

try:
    dictor = support.read_json(
        path=r'C:\WinTest\JSON\data',
        filename='AutoKeyboard.json'
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
        # 获取键盘类型信息
        KB_TYPE = support.read_json(
            path=r'C:\WinTest\LogFile',
            filename='HWConfig.json'
        )['Config_KB']['KBTYPE']
        print('KB_TYPE:', KB_TYPE)
        copyfile(
            src=r'%s\Keyboard_%s.ini' % (dictor['tool_path'], KB_TYPE),
            dst=r'%s\Keyboard.ini' % dictor['tool_path']
        )
        # ebableFn
        os.chdir(dictor['tool_path'])
        for i in dictor['enableFn']:
            os.system(i)
        # 测试内容和结果
        res = support.test(
            tool_path=dictor['tool_path'],
            act='find',
            checklist='NO',
            result_log_name=dictor['result_log_name'],
            check_item=dictor['check_item'],
            instruct=dictor['instruct'],
            check_data=''
        )
        print('res:', res)
        if res:
            print('KB Test pass!!!')
            result = 'pass'
            support.copy_log(
                source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                act='w'
            )
        else:
            print('KB Test fail!!!')
            result = 'fail'
            support.copy_log(
                source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                target_path=r'C:\WinTest\LogFile\FAIL_%s.log' % dictor['RUNITEM'],
                act='a'
            )

        os.chdir(dictor['tool_path'])
        for i in dictor['disableFn']:
            os.system(i)

        # 判断测试结果
        if result == 'fail':
            Errorcode = 'KB Test fail'
            if support.judge(
                    FailRetry=dictor['FailRetry'],
                    FailRetrytimes=dictor['FailRetrytimes']
            ):
                dictor['FailRetry'] = str(int(dictor['FailRetry']) + 1)
                print('测试循环次数：' + dictor['FailRetry'], '，测试结果：fail！！！')
                continue

            # creatResult
            support.creatResult(
                Fixed=currentPath,
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
            # support.message(
            #     Code=Errorcode
            # )
            break

        elif result == 'pass':
            support.FileLog(item=dictor['RUNITEM'])
            print('测试循环次数:', n, '，测试结果：pass！！！')
            print('测试SN:', MB_SN)
            # creatResult
            support.creatResult(
                Fixed=currentPath,
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
