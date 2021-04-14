# Coding by LiXiao
# Datatime:3/4/2021 2:25 PM
# Filename:Lidswitch.py
# Toolby: PyCharm
import os
import support

try:
    dictor = support.read_json(
        path=r'C:\WinTest\JSON\data',
        filename='Lidswitch.json'
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

    # 读取主板写入的SN
    MB_SN = support.getSN()

    # 测试正文
    for n in range(1, 200):
        # 测试内容和结果

        print('测试正文')
        LID = support.test(
            tool_path=dictor['tool_path'],
            act='find',
            checklist='NO',
            result_log_name=dictor['result_log_name2'],
            check_item=dictor['check_item2'],
            instruct=dictor['instruct2'],
            check_data='PASS'
        )
        Errorcode = '.'
        print('LID:', LID)
        if LID:
            result = 'pass'
            support.copy_log(
                source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name2']),
                target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                act='w'
            )
        else:
            Errorcode = 'MBCF4'
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
            support.message(
                Code=Errorcode
            )
            break

        elif result == 'pass':
            # os.system(r'call \WinTest\tools\FileLog.cmd \WinTest\LogFile\%s.log' % dictor['RUNITEM'])
            # dates = support.FileLog(item=dictor['RUNITEM'])
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
    print(e)
    print("SN匹配信息错误，请检查正则表达式！！！")

except Exception as e:
    print(e)
