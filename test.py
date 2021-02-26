import support
import os
import time   # 测试时拿掉

# 开头模板信息
dict = {
    'FailRetry':'0',
    'FailRetrytimes':'10',
    'UPLIMIT':'9999.900',
    'LOWLIMIT':'-9999.900',
    'RUNITEM':'UpdatePatch',
}
try:
    # currentPath = os.getcwd()
    currentPath = r'C:\WinTest\Work'
    print(currentPath)
    MB_SN = support.getSN()
    StartTime = support.titles(RUNITEM = dict['RUNITEM'], stage = 'start')
    for i in dict:
        print(i + ' : ' + dict[i])

    # 测试正文
    for n in range(1, 200):
        # 测试内容和结果
        print('测试正文')
        if dict['FailRetry'] == '5':
            result = 'pass'
        else:
            result = 'fail'
        # result = 'fail'

        # 判断测试结果
        if result == 'fail':
            if support.judge(FailRetry=dict['FailRetry'], FailRetrytimes=dict['FailRetrytimes']):
                dict['FailRetry'] = str(int(dict['FailRetry']) + 1)
                print('测试循环次数：' + dict['FailRetry'], '，测试结果：fail！！！')
                continue

            TestTimes = support.gettesttime(start=StartTime)
            print('测试用时:', TestTimes)
            support.creatResult(Fixed = currentPath, ItemName = dict['RUNITEM'], Result = -1, ItemTag = 0)
            support.setinfo(RUNITEM=dict['RUNITEM'], SN=MB_SN, UPLIMIT=dict['UPLIMIT'],
                            LOWLIMIT=dict['LOWLIMIT'], Result='F', NUM='0',
                            LOGINFO='UpdatePatch Fail', Starttime=StartTime, TestTime=TestTimes)
            print('测试循环次数:', n, '，测试结果：fail！！！！')
            break

        if result == 'pass':
            print('测试循环次数:', n, '，测试结果：pass！！！')
            time.sleep(3)    # 测试时拿掉
            print('测试SN:', MB_SN)
            support.creatResult(Fixed = currentPath, ItemName = dict['RUNITEM'], Result = 1, ItemTag = 0)
            TestTimes = support.gettesttime(start=StartTime)
            print('测试用时:', TestTimes)
            support.setinfo(RUNITEM=dict['RUNITEM'], SN=MB_SN, UPLIMIT=dict['UPLIMIT'],
                            LOWLIMIT=dict['LOWLIMIT'], Result='P', NUM='1',
                            LOGINFO='UpdatePatch Success', Starttime=StartTime, TestTime=TestTimes)
            break

        else:
            print('无测试结果！！！')


except AttributeError as e:
    print(e)
    print("SN匹配信息错误，请检查正则表达式！！！")

except Exception as e:
    print(e)

"""
python中时间日期格式化符号：
%y 两位数的年份表示（00-99）
%Y 四位数的年份表示（000-9999）
%m 月份（01-12）
%d 月内中的一天（0-31）
%H 24小时制小时数（0-23）
%I 12小时制小时数（01-12）
%M 分钟数（00=59）
%S 秒（00-59）
%a 本地简化星期名称
%A 本地完整星期名称
%b 本地简化的月份名称
%B 本地完整的月份名称
%c 本地相应的日期表示和时间表示
%j 年内的一天（001-366）
%p 本地A.M.或P.M.的等价符
%U 一年中的星期数（00-53）星期天为星期的开始
%w 星期（0-6），星期天为星期的开始
%W 一年中的星期数（00-53）星期一为星期的开始
%x 本地相应的日期表示
%X 本地相应的时间表示
%Z 当前时区的名称
%% %号本身
"""