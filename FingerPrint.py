# Coding by LiXiao
# Datatime:21/04/15 2:27 PM
# Filename:FingerPrint.py
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
    'RUNITEM': 'FingerPrint',
    'Errorcode': 'MBCF4',
    'tool_path': r'C:\WinTest\tools',
    'instruct': r'DEVCON.EXE find "USB\VID*">FP.TXT',
    'result_log_name': 'FP.TXT',
    'tool_path_Synaptics': r'C:\WinTest\FFT\FPTest\Synaptics-FingerPrint',
    'instruct_Synaptics': '587-000994-01r7-Stimulus.bat',
    'result_log_name_Synaptics': 'SynaTestResult.log',
    'check_item_Synaptics': 'Test Result: PASS',
    'tool_path_Goodix': r'C:\WinTest\FFT\FPTest\Goodix-FingerPrint',
    'instruct_Goodix': 'GFMPTest.exe',
    'result_log_name_Goodix': 'customer.log',
    'check_item_Goodix': 'PASS',
    'tool_path_ELAN': r'C:\WinTest\FFT\FPTest\Elan_FingerPrint',
    'instruct_ELAN': r'"eFSAX System Test Manager.exe"',
    'result_log_name_ELAN': 'Result.txt',
    'check_item_ELAN': 'PASS',
    'FP_TYPE_list': [r'Synaptics WBDI', r'USB\VID_06CB&PID_00BE', r'USB\VID_27C6&PID_55A2', r'USB\VID_04F3&PID_0C4D', r'ELAN WBF Fingerprint Sensor', r'USB\VID_13D3&PID_5419&MI_00'],
    'FP_TYPE': {
        r'Synaptics WBDI': 'Synaptics',
        r'USB\VID_06CB&PID_00BE': 'Synaptics',
        r'USB\VID_27C6&PID_55A2': 'Goodix',
        r'USB\VID_04F3&PID_0C4D': 'ELAN',
        r'ELAN WBF Fingerprint Sensor': 'ELAN',
        r'USB\VID_13D3&PID_5419&MI_00': 'TEST'
    }
}
support.write_json(
    data=dictor,
    path=r'C:\WinTest\JSON\data',
    filename='FingerPrint.json'
)
"""

try:
    dictor = support.read_json(
        path=r'C:\WinTest\JSON\data',
        filename='FingerPrint.json'
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

        # 获取FP_TYPE
        FP_TYPE = support.test(
            tool_path=dictor['tool_path'],
            act='match',
            checklist='YES',
            result_log_name=dictor['result_log_name'],
            check_item=dictor['FP_TYPE_list'],
            instruct=dictor['instruct'],
            check_data=dictor['FP_TYPE']
        )
        print('FP_TYPE:', FP_TYPE)
        if FP_TYPE == 'Synaptics':
            print('指纹厂商为Synaptics，即将进行指纹测试！！！')
            test_result = support.test(
                tool_path=dictor['tool_path_Synaptics'],
                act='find',
                checklist='NO',
                result_log_name=dictor['result_log_name_Synaptics'],
                check_item=dictor['check_item_Synaptics'],
                instruct=dictor['instruct_Synaptics'],
                check_data=''
            )
            if test_result:
                result = 'pass'
                support.copy_log(
                    source_path=r'%s\%s' % (dictor['tool_path_Synaptics'], dictor['result_log_name_Synaptics']),
                    target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                    act='a'
                )
            else:
                result = 'fail'

        if FP_TYPE == 'ELAN':
            print('指纹厂商为ELAN，即将进行指纹测试！！！')
            test_result = support.test(
                tool_path=dictor['tool_path_ELAN'],
                act='find',
                checklist='NO',
                result_log_name=dictor['result_log_name_ELAN'],
                check_item=dictor['check_item_ELAN'],
                instruct=dictor['instruct_ELAN'],
                check_data=''
            )
            if test_result:
                result = 'pass'
                support.copy_log(
                    source_path=r'%s\%s' % (dictor['tool_path_ELAN'], dictor['result_log_name_ELAN']),
                    target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                    act='a'
                )
            else:
                result = 'fail'

        elif FP_TYPE == 'Goodix':
            print('指纹厂商为Goodix，即将进行指纹测试！！！')
            test_result = support.test(
                tool_path=dictor['tool_path_Goodix'],
                act='find',
                checklist='NO',
                result_log_name=dictor['result_log_name_Goodix'],
                check_item=dictor['check_item_Goodix'],
                instruct=dictor['instruct_Goodix'],
                check_data=''
            )
            if test_result:
                result = 'pass'
                support.copy_log(
                    source_path=r'%s\%s' % (dictor['tool_path_Goodix'], dictor['result_log_name_Goodix']),
                    target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                    act='a'
                )
            else:
                result = 'fail'
        else:
            ex = Exception('FP_TYPE信息获取失败，请检查配置信息！！！')
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
    print("SN匹配信息错误，请检查正则表达式！！！")
    print(e)
    support.message_showinfo('ERROR', e)

except Exception as e:
    print(e)
    support.message_showinfo('ERROR', e)
