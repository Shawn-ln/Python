# Coding by LiXiao
# Datatime:21/04/14 10:58 AM
# Filename:FCTSTART.py
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
    'RUNITEM': 'FCTSTART',
    'Errorcode': 'MBCF4',
    'tool_path': 'C:\WinTest\Tools',
    'instruct': 'ShowPassFail.exe>FCTSTART.BAT',
    'result_log_name': 'FCTSTART.BAT',
    'check_item': ''
}
support.write_json(
    data=dictor,
    path=r'C:\WinTest\JSON\data',
    filename='FCTSTART.json'
)
"""
try:
    dictor = support.read_json(
        path=r'C:\WinTest\JSON\data',
        filename='FCTSTART.json'
    )
    print('FCTSTART:', dictor)
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
    MB_SN = support.getMBSN()

    # 测试正文
    for n in range(1, 200):
        # 测试内容和结果


        support.test(
            tool_path=dictor['tool_path'],
            act='read',
            checklist='NO',
            result_log_name=dictor['result_log_name'],
            check_item=dictor['check_item'],
            instruct=dictor['instruct'],
            check_data=''
        )
        result = 'pass'


        # 判断测试结果
        if result == 'fail':
            Errorcode = 'FCTSTART fail'
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
