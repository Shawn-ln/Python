# Coding by LiXiao
# Datatime:21/04/16 2:37 PM
# Filename:Touchpanel.py
# Toolby: PyCharm


import os
import time
import support


# 开头模板信息
dictor = {
    'FailRetry': '0',
    'FailRetrytimes': '0',
    'UPLIMIT': '9999.900',
    'LOWLIMIT': '-9999.900',
    'RUNITEM': 'Touchpanel',
    'Errorcode': 'MBCF4',
    'tool_path': r'C:\WinTest\FFT\Type_C',
    'instruct': r'devcon.exe find "USB*">test_box.TXT',
    'result_log_name': 'test_box.TXT',
    'instruct_tycall': 'wmusbel_usbct-all.exe',
    'result_log_name_tycall': 'Result.txt',
    'check_item_tycall': 'PASS',
    'instruct_PHIYO': 'TypeCTester_1605.exe',
    'result_log_name_PHIYO': 'Result.txt',
    'check_item_PHIYO': 'PASS',
    'ini_dictor': {
        'tycall': ['Port3.ini', 'wmusbel_usbct-all_config.ini'],
        'PHIYO': ['USBPATHport3.INI', 'USBPATH.INI', 'TypeCTester_1605port3.ini', 'TypeCTester_1605.ini']
    },
    'kill_lists': ['AutoWebCam.exe', 'DisplayLCD.exe', 'wmusbel_usbct-all.exe', 'TypeCTester_1605.exe', 'notepad++.exe'],
    'BOX_TYPE_list': [r'PHIYO', r'VID_0483&PID_1314', r'USB\VID_13D3&PID_5419&MI_00'],
    'BOX_TYPE': {
        r'PHIYO': 'PHIYO',
        r'VID_0483&PID_1314': 'tycall',
        r'USB\VID_13D3&PID_5419&MI_00': 'TEST'  # 任意找个驱动用来判断是否能抓到盒子的驱动
    }
}
support.write_json(
    data=dictor,
    path=r'C:\WinTest\JSON\data',
    filename='Type-C_Port3.json'
)


try:
    dictor = support.read_json(
        path=r'C:\WinTest\JSON\data',
        filename='Type-C_Port3.json'
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
        # 获取BOX_TYPE
        BOX_TYPE = 'TEST'
        while BOX_TYPE == 'TEST':
            i = os.system("cls")
            print('** TypeC_port3功能测试 ,将Port1和2保持空插 *******')
            print('*** TypeC_port3功能测试 ,将Port1和2保持空插 *******')
            print('*** TypeC_port3功能测试 ,将Port1和2保持空插 *******')
            time.sleep(3)
            BOX_TYPE = support.test(
                tool_path=dictor['tool_path'],
                act='match',
                checklist='YES',
                result_log_name=dictor['result_log_name'],
                check_item=dictor['BOX_TYPE_list'],
                instruct=dictor['instruct'],
                check_data=dictor['BOX_TYPE']
            )
            print('BOX_TYPE:', BOX_TYPE)
        if BOX_TYPE == 'tycall':
            print('测试盒子为tycall，即将进行TypeC功能测试！！！')
            support.del_log(
                log_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name_tycall'])
            )
            os.system(r'del %s\log\*.* /q' % dictor['tool_path'])
            support.copyfile(
                src=r'%s\%s' % (dictor['tool_path'], dictor['ini_dictor']['tycall'][0]),
                dst=r'%s\%s' % (dictor['tool_path'], dictor['ini_dictor']['tycall'][1])
            )
            test_result = support.test(
                tool_path=dictor['tool_path'],
                act='find',
                checklist='NO',
                result_log_name=dictor['result_log_name_tycall'],
                check_item=dictor['check_item_tycall'],
                instruct=dictor['instruct_tycall'],
                check_data=''
            )
            if test_result:
                result = 'pass'
                os.system(r'copy %s\log\*.* %s\%s /y' % (dictor['tool_path'], dictor['tool_path'], dictor['result_log_name_tycall']))
                support.copy_log(
                    source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name_tycall']),
                    target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                    act='a'
                )
            else:
                result = 'fail'
        elif BOX_TYPE == 'PHIYO':
            print('测试盒子为tPHIYO，即将进行TypeC功能测试！！！')
            support.del_log(
                log_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name_PHIYO'])
            )
            os.system(r'del %s\log\*.* /q' % dictor['tool_path'])
            support.copyfile(
                src=r'%s\%s' % (dictor['tool_path'], dictor['ini_dictor']['PHIYO'][0]),
                dst=r'%s\%s' % (dictor['tool_path'], dictor['ini_dictor']['PHIYO'][1])
            )
            support.copyfile(
                src=r'%s\%s' % (dictor['tool_path'], dictor['ini_dictor']['PHIYO'][2]),
                dst=r'%s\%s' % (dictor['tool_path'], dictor['ini_dictor']['PHIYO'][3])
            )
            test_result = support.test(
                tool_path=dictor['tool_path'],
                act='find',
                checklist='NO',
                result_log_name=dictor['result_log_name_PHIYO'],
                check_item=dictor['check_item_PHIYO'],
                instruct=dictor['instruct_PHIYO'],
                check_data=''
            )
            if test_result:
                result = 'pass'
                os.system(r'copy %s\log\*.* %s\%s /y' % (dictor['tool_path'], dictor['tool_path'], dictor['result_log_name_PHIYO']))
                support.copy_log(
                    source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name_PHIYO']),
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
    print(e)
    print("SN匹配信息错误，请检查正则表达式！！！")

except Exception as e:
    print(e)
