# Coding by LiXiao
# Datatime:4/26/2021 11:36 AM
# Filename:TPRefer.py
# Toolby: PyCharm

import os
import support
"""
# 开头模板信息
dictor = {
    'FailRetry': '0',
    'FailRetrytimes': '0',
    'UPLIMIT': '9999.900',
    'LOWLIMIT': '-9999.900',
    'RUNITEM': 'TPMTest',
    'Errorcode': 'MBCF4',
    'tool_path': r'C:\WinTest\FFT\TPReferTest',
    'instruct': r'SCheckCapG14T_v0.02.3k.exe',
    'instruct1': r'echo TPRefer FW 检查开始',
    'result_log_name': 'result.log',
    'check_item': [r'Total:1 OK:1 NG:0', r'FWVER_MAJOR', r'FWVER_MINOR', r'PID                 ='],
    'fw_list': {
        '0x52A8': ['0x0002', '0x00'],
        '0x52A9': ['0x0002', '0x00'],
        '0x52AA': ['0x0002', '0x03'],
    }
}
support.write_json(
    data=dictor,
    path=r'C:\WinTest\JSON\data',
    filename='TPRefer.json'
)
"""
try:
    dictor = support.read_json(
        path=r'C:\WinTest\JSON\data',
        filename='TPRefer.json'
    )
    print('dictor:', dictor)
    support.copyfile(
        src=r'C:\WinTest\LogFile\Response.bat',
        dst=r'C:\WinTest\Tools\Response.bat'
    )

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
        # 测试内容和结果
        if LCD == 'NOTOUCH':
            print('此配置为NOTOUCH，不需测试TPRefer！！！')
            result = 'pass'
            support.writr_log(
                path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                date='此配置为%s，不需测试TPRefer！！！' % LCD,
                act='w'
            )
        elif LCD == 'TOUCH':
            test_result = support.test(
                tool_path=dictor['tool_path'],
                act='find',
                checklist='NO',
                result_log_name=dictor['result_log_name'],
                check_item=dictor['check_item'][0],
                instruct=dictor['instruct'],
                check_data=''
            )
            print('test_result:', test_result)
            if test_result:
                fw = support.test(
                    tool_path=dictor['tool_path'],
                    act='read',
                    checklist='YES',
                    result_log_name=dictor['result_log_name'],
                    check_item=[dictor['check_item'][1], dictor['check_item'][2], dictor['check_item'][3]],
                    instruct=dictor['instruct1'],
                    check_data=''
                )
                print('fw:', fw)
                # 需要拿掉删除log动作
                if dictor['fw_list'][fw['PID                 =']][0] == fw['FWVER_MAJOR']:
                    print('FWVER_MAJOR Check Pass,系统定义FW为:%s,实际读取FW为:%s' % (dictor['fw_list'][fw['PID                 =']][0], fw['FWVER_MAJOR']))
                    if dictor['fw_list'][fw['PID                 =']][1] == fw['FWVER_MINOR']:
                        result = 'pass'
                        print('FWVER_MINOR Check Pass,系统定义FW为:%s,实际读取FW为:%s' % (dictor['fw_list'][fw['PID                 =']][1], fw['FWVER_MINOR']))
                        support.copy_log(
                            source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                            target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                            act='w'
                        )
                    else:
                        print('FWVER_MINOR Check fail,系统定义FW为:%s,实际读取FW为:%s' % (dictor['fw_list'][fw['PID                 =']][1], fw['FWVER_MINOR']))
                        result = 'fail'
                else:
                    print('FWVER_MAJOR Check fail,系统定义FW为:%s,实际读取FW为:%s' % (dictor['fw_list'][fw['PID                 =']][0], fw['FWVER_MAJOR']))
                    result = 'fail'
            else:
                result = 'fail'
        else:
            print('LCD Type获取失败，请检查配置信息！！！')
            ex = Exception('LCD Type获取失败，请检查配置信息！！！')
            # 抛出异常对象
            raise ex

        # 判断测试结果
        if result == 'fail':
            if support.judge(FailRetry=dictor['FailRetry'], FailRetrytimes=dictor['FailRetrytimes']):
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
