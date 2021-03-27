# Coding by LiXiao
# Datatime:2/26/2021 11:37 AM
# Filename:test.py
# Toolby: PyCharm
import os
import support
import time   # 测试时拿掉

# 开头模板信息
dictor = {
    'FailRetry':'0',
    'FailRetrytimes':'10',
    'UPLIMIT':'9999.900',
    'LOWLIMIT':'-9999.900',
    'RUNITEM':'UpdatePatch',
}

pdtkey = (
    'PUKM-WUQ5-851W-09U6-TQ0W',
    'PUKM-QP10-9IP1-808W-QRE6',
    'PUKM-T9EP-R9IE-5RPE-8U0O',
    'PUKM-QQIR-IOPQ-6QTQ-09P9',
    'PUKM-00I9-EPOE-OQ8O-I0II',
    'PUKM-9YWO-Q8RI-P969-TIUE',
    'PUKM-QI0P-E558-YI1R-W8T5',
    'PUKM-QP10-9IP1-808W-QRE6',
    'PUKM-WUQ5-851W-09U6-TQ0W',
    'PUKM-WTRY-165I-POOU-WR8P',
    'PUKM-YR0I-E6PY-1T9P-8UP0'
)

try:
    # 测试开始时间
    StartTime = support.titles(RUNITEM=dictor['RUNITEM'], stage='start')
    for i in dictor:
        print(i + ' : ' + dictor[i])

    # 脚本路径
    currentPath = os.getcwd()
    # currentPath = r'C:\WinTest\Work'
    # print(currentPath)

    # 读取主板写入的mbsn
    MB_SN = support.getMBSN()

    # 判断是否有测试pass的log记录
    if support.passlog(dictor['RUNITEM']):
        # creatResult
        support.SyncTime()
        support.creatResult(Fixed=currentPath, ItemName=dictor['RUNITEM'], Result=1, ItemTag=0)
    else:
        # disableIPV6
        support.disableIPV6()
        # 运行工具注册码
        for i in pdtkey:
            support.ptd(i)
        # 平板机种需要设定
        # support.padsetting()
        # 设置时区，同步时间
        support.SyncTime()
        # 测试正文
        for n in range(1, 200):
            # 测试内容和结果

            print('测试正文')
            if dictor['FailRetry'] == '5':
                result = 'pass'
            else:
                result = 'fail'
            # result = 'fail'

            # 判断测试结果
            if result == 'fail':
                if support.judge(FailRetry=dictor['FailRetry'], FailRetrytimes=dictor['FailRetrytimes']):
                    dictor['FailRetry'] = str(int(dictor['FailRetry']) + 1)
                    print('测试循环次数：' + dictor['FailRetry'], '，测试结果：fail！！！')
                    continue

                # creatResult
                support.creatResult(Fixed=currentPath, ItemName=dictor['RUNITEM'], Result=-1, ItemTag=0)
                # setinfo
                support.setinfo(RUNITEM=dictor['RUNITEM'], SN=MB_SN, Result='F', NUM='0',
                                LOGINFO='UpdatePatch Fail', Starttime=StartTime)
                print('测试循环次数:', n, '，测试结果：fail！！！！')
                break

            if result == 'pass':
                print('测试循环次数:', n, '，测试结果：pass！！！')
                time.sleep(3)    # 测试时拿掉
                print('测试SN:', MB_SN)
                # creatResult
                support.creatResult(Fixed=currentPath, ItemName=dictor['RUNITEM'], Result=1, ItemTag=0)
                # setinfo
                support.setinfo(RUNITEM=dictor['RUNITEM'], SN=MB_SN, Result='P', NUM='1',
                                LOGINFO='UpdatePatch Success', Starttime=StartTime)
                break

            else:
                print('无测试结果！！！')


except AttributeError as e:
    print(e)
    print("SN匹配信息错误，请检查正则表达式！！！")

except Exception as e:
    print(e)
