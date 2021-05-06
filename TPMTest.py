# Coding by LiXiao
# Datatime:4/26/2021 11:38 AM
# Filename:TPMTest.py
# Toolby: PyCharm

import os
import support


# 开头模板信息
# dictor = {
#     'FailRetry': '0',
#     'FailRetrytimes': '1',
#     'UPLIMIT': '9999.900',
#     'LOWLIMIT': '-9999.900',
#     'RUNITEM': 'TPMTest',
#     'Errorcode': 'MBCF4',
#     'tool_path_ST': r'C:\WinTest\FFT\TPMTest\ST',
#     'instruct_ST': r'TPM2_CHK_x64.exe -p -v -l TPMFW.LOG',
#     'result_log_name_ST': 'TPMFW.LOG',
#     'check_item_ST': [r'Firmware Version 1 : 0.1.1.2 (1.258)', r'TPM SelfTest Successful'],
#     'tool_path_Nuvoton': r'C:\WinTest\FFT\TPMTest\Nuvoton',
#     'instruct_Nuvoton': [r'wSkCmd.exe -getversion2 >TPMFW.LOG', r'wSkCmd.exe -selftest2 >TPMSelfTest.LOG'],
#     'result_log_name_Nuvoton': ['TPMFW.LOG', 'TPMSelfTest.LOG'],
#     'check_item_Nuvoton': [r'FW Version is:   7.2.2.0', r'Command Passed']
# }
# support.write_json(
#     data=dictor,
#     path=r'C:\WinTest\JSON\data',
#     filename='TPMTest.json'
# )


try:
    dictor = support.read_json(
        path=r'C:\WinTest\JSON\data',
        filename='TPMTest.json'
    )
    print('dictor:', dictor)

    TPM = support.read_json(
        path=r'C:\WinTest\LogFile',
        filename='HWConfig.json'
    )['Config_CPU']['TPM']
    print('TPM:', TPM)
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
        if TPM == 'ST':
            print('当前配置TPM类型为ST，即将进行TPM FW测试！！！')
            test_result = support.test(
                tool_path=dictor['tool_path_ST'],
                act='find',
                checklist='YES',
                result_log_name=dictor['result_log_name_ST'],
                check_item=dictor['check_item_ST'],
                instruct=dictor['instruct_ST'],
                check_data=dictor['check_item_ST']
            )
            if test_result:
                result = 'pass'
                support.copy_log(
                    source_path=r'%s\%s' % (dictor['tool_path_ST'], dictor['result_log_name_ST']),
                    target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                    act='a'
                )
            else:
                result = 'fail'
        elif TPM == 'Nuvoton':
            print('当前配置TPM类型为Nuvoton，即将进行TPM FW测试！！！')
            test_result = support.test(
                tool_path=dictor['tool_path_Nuvoton'],
                act='find',
                checklist='NO',
                result_log_name=dictor['result_log_name_Nuvoton'][0],
                check_item=dictor['check_item_Nuvoton'][0],
                instruct=dictor['instruct_Nuvoton'][0],
                check_data=''
            )
            if test_result:
                test_result1 = support.test(
                    tool_path=dictor['tool_path_Nuvoton'],
                    act='find',
                    checklist='NO',
                    result_log_name=dictor['result_log_name_Nuvoton'][1],
                    check_item=dictor['check_item_Nuvoton'][1],
                    instruct=dictor['instruct_Nuvoton'][1],
                    check_data=''
                )
                if test_result1:
                    result = 'pass'
                    support.copy_log(
                        source_path=r'%s\%s' % (dictor['tool_path_Nuvoton'], dictor['result_log_name_Nuvoton'][0]),
                        target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                        act='w'
                    )
                    support.copy_log(
                        source_path=r'%s\%s' % (dictor['tool_path_Nuvoton'], dictor['result_log_name_Nuvoton'][1]),
                        target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                        act='a'
                    )
                else:
                    result = 'fail'
            else:
                result = 'fail'
        elif TPM == 'NONE':
            print('当前配置不带TPM,无需测试！！！')
            result = 'pass'
        else:
            ex = Exception('BOX_TYPE信息获取失败，请检查配置信息！！！')
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
