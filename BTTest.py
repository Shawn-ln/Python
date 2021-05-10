# Coding by LiXiao
# Datatime:3/8/2021 3:07 PM
# Filename:BTTest.py
# Toolby: PyCharm
import os
import support

try:
    BTTest = support.read_json(
        path=r'C:\WinTest\JSON\data',
        filename='BTTest.json'
    )
    print('BTTest:', BTTest)
    # 测试开始时间
    StartTime = support.titles(
        RUNITEM=BTTest['RUNITEM'],
        stage='start'
    )

    # 脚本路径
    currentPath = os.getcwd()
    # currentPath = r'C:\WinTest\Work'
    # print(currentPath)

    # 读取主板写入的mbsn
    MB_SN = support.getSN()

    # 判断是否有测试pass的log记录
    if support.passlog(
            RUNITEM=BTTest['RUNITEM']
    ):
        # creatResult
        support.creatResult(
            Fixed=currentPath,
            ItemName=BTTest['RUNITEM'],
            Result=1,
            ItemTag=0
        )
    else:
        # 测试正文
        for n in range(1, 200):
            # 测试内容和结果
            if support.test(
                    tool_path=BTTest['test']['tool_path'],
                    checklist=BTTest['test']['checklist'],
                    result_log_name=BTTest['test']['result_log_name'],
                    act=BTTest['test']['act'],
                    instruct=BTTest['test']['instruct'],
                    check_item=BTTest['test']['check_item'],
                    check_data=BTTest['test']['check_data']
            ):
                result = 'pass'
            else:
                result = 'fail'

            # 判断测试结果
            if result == 'fail':
                if support.judge(
                        FailRetry=BTTest['FailRetry'],
                        FailRetrytimes=BTTest['FailRetrytimes']
                ):
                    BTTest['FailRetry'] = str(int(BTTest['FailRetry']) + 1)
                    print('测试循环次数：' + BTTest['FailRetry'], '，测试结果：fail！！！')
                    continue

                # creatResult
                support.creatResult(
                    Fixed=currentPath,
                    ItemName=BTTest['RUNITEM'],
                    Result=-1,
                    ItemTag=0
                )
                # setinfo
                support.setinfo(
                    RUNITEM=BTTest['RUNITEM'],
                    SN=MB_SN,
                    Result='F',
                    NUM='0',
                    LOGINFO=BTTest['RUNITEM'] + ' Fail',
                    Starttime=StartTime
                )
                print('测试循环次数:', n, '，测试结果：fail！！！！')
                support.message(
                    Code=BTTest['Errorcode']
                )
                break

            elif result == 'pass':
                print('测试循环次数:', n, '，测试结果：pass！！！')
                print('测试SN:', MB_SN)
                # creatResult
                support.creatResult(
                    Fixed=currentPath,
                    ItemName=BTTest['RUNITEM'],
                    Result=1,
                    ItemTag=0
                )
                # setinfo
                support.setinfo(
                    RUNITEM=BTTest['RUNITEM'],
                    SN=MB_SN,
                    Result='P',
                    NUM='1',
                    LOGINFO=BTTest['RUNITEM'] + ' Pass',
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


