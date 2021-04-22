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
    filename='Touchpanel.json'
)


try:
    dictor = support.read_json(
        path=r'C:\WinTest\JSON\data',
        filename='Touchpanel.json'
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
        if BOX_TYPE == 'tycall':
            print('aaa')
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
