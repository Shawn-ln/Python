# Coding by LiXiao
# Datatime:4/28/2021 8:34 AM
# Filename:NovoHole.py
# Toolby: PyCharm

import os
import support


# # 开头模板信息
# dictor = {
#     'FailRetry': '0',
#     'FailRetrytimes': '0',
#     'UPLIMIT': '9999.900',
#     'LOWLIMIT': '-9999.900',
#     'RUNITEM': 'NovoHole',
#     'Errorcode': 'MBCF4',
#     'tool_path': r'C:\WinTest\FFT\NovoHole',
#     'instruct': [r'NoveHoleCmd.exe -E', r'NoveHole.exe', r'NoveHoleCmd.exe -D'],
#     'result_log_name': ['NoveHoleCmd.log', r'NoveHole.log', r'NoveHoleCmd.log'],
#     'check_item': [r'Enable NoveHole Test Mode Successful', r'RESULT=PASS', r'Disable NoveHole Test Mode Successful'],
#     'check_data': ''
# }
# support.write_json(
#     data=dictor,
#     path=r'C:\WinTest\JSON\data',
#     filename='NovoHole.json'
# )


try:
    dictor = support.read_json(
        path=r'C:\WinTest\JSON\data',
        filename='NovoHole.json'
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
    result = 'fail'

    # 测试正文
    for n in range(1, 200):
        # 测试内容和结果
        for i in range(0, len(dictor['instruct'])):
            res = support.test(
                tool_path=dictor['tool_path'],
                act='find',
                checklist='NO',
                result_log_name=dictor['result_log_name'][i],
                check_item=dictor['check_item'][i],
                instruct=dictor['instruct'][i],
                check_data=''
            )
            print('res:', res)
            if res:
                print('%s 执行成功!!!' % dictor['instruct'][i])
                result = 'pass'
                if i == 0:
                    support.copy_log(
                        source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name'][i]),
                        target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                        act='w'
                    )
                else:
                    support.copy_log(
                        source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name'][i]),
                        target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                        act='a'
                    )
            else:
                print('%s 执行失败!!!' % dictor['instruct'][i])
                result = 'fail'
                support.copy_log(
                    source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name'][i]),
                    target_path=r'C:\WinTest\LogFile\FAIL_%s.log' % dictor['RUNITEM'],
                    act='a'
                )
                break

        # 判断测试结果
        if result == 'fail':
            Errorcode = 'NovoHole测试fail'
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
