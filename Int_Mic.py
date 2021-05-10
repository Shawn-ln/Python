# Coding by LiXiao
# Datatime:21/04/16 3:28 PM
# Filename:Int_Mic.py
# Toolby: PyCharm


import os
import time
import support

"""
# 开头模板信息
dictor = {
    'FailRetry': '0',
    'FailRetrytimes': '1',
    'UPLIMIT': '9999.900',
    'LOWLIMIT': '-9999.900',
    'RUNITEM': 'Int_MIC',
    'Errorcode': 'MBCF4',
    'tool_path': r'C:\WinTest\FFT\Internal_Mic',
    'instruct': r'ScanLog.exe >Internal_Mic_result.log',
    'result_log_name': 'Internal_Mic_result.log',
    'kill_lists': ['Playback.exe', 'Recode.exe'],
    'check_item': 'scanResultstr=pass'
}
support.write_json(
    data=dictor,
    path=r'C:\WinTest\JSON\data',
    filename='Int_Mic.json'
)
"""
try:
    dictor = support.read_json(
        path=r'C:\WinTest\JSON\data',
        filename='Int_Mic.json'
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
        # 测试内容和结果
        support.killer(
            lists=dictor['kill_lists']
        )
        os.chdir(dictor['tool_path'])
        os.system(r'AudioBalance.exe')
        os.system(r'ApoAnalyzer64.exe -default -eAll -disabletp')
        JDSTATUS = False
        while not JDSTATUS:
            print('********************    请移除音源线做内部麦克风测试   *********************')
            print('********************    请移除音源线做内部麦克风测试   *********************')
            print('********************    请移除音源线做内部麦克风测试   *********************')
            time.sleep(2)
            support.del_log(
                log_path=r'%s\JDSTATUS.LOG' % dictor['tool_path']
            )
            # 判断音源线是否拔掉
            JDSTATUS = support.test(
                tool_path=dictor['tool_path'],
                act='find',
                checklist='NO',
                result_log_name=r'JDSTATUS.LOG',
                check_item='not plug in',
                instruct=r'GetJDStatus.exe 21 >JDSTATUS.LOG',
                check_data=''
            )
        support.copy_log(
            source_path=r'%s\JDSTATUS.LOG' % dictor['tool_path'],
            target_path=r'C:\WinTest\LogFile\%s.log' % (dictor['RUNITEM']),
            act='w'
        )
        # print('JDSTATUS:', JDSTATUS)
        os.system('start Playback.exe')
        os.system('Recode.exe')
        os.system('AnalyseSNR.exe')
        rst = support.test(
            tool_path=dictor['tool_path'],
            act='find',
            checklist='NO',
            result_log_name=dictor['result_log_name'],
            check_item=dictor['check_item'],
            instruct=dictor['instruct'],
            check_data=''
        )
        print(rst)
        if rst:
            print('********************内部麦克风测试PASS*********************')
            result = 'pass'
            support.copy_log(
                source_path=r'%s\all.txt' % (dictor['tool_path']),
                target_path=r'%s\Internal_Mic_data.log' % (dictor['tool_path']),
                act='w'
            )

            support.copy_log(
                source_path=r'%s\all.txt' % dictor['tool_path'],
                target_path=r'C:\WinTest\LogFile\%s.log' % (dictor['RUNITEM']),
                act='a'
            )
            support.copy_log(
                source_path=r'%s\Internal_Mic_result.log' % dictor['tool_path'],
                target_path=r'C:\WinTest\LogFile\%s.log' % (dictor['RUNITEM']),
                act='a'
            )
            support.copyfile(
                src=r'%s\testAudio.wav' % dictor['tool_path'],
                dst=r'C:\WinTest\Log\%s.wav' % dictor['RUNITEM']
            )
        else:
            print('********************内部麦克风测试FAIL*********************')
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
    print("SN匹配信息错误，请检查正则表达式！！！")
    print(e)
    support.message_showinfo('ERROR', e)

except Exception as e:
    print(e)
    support.message_showinfo('ERROR', e)
