# Coding by LiXiao
# Datatime:2/26/2021 5:37 PM
# Filename:CheckBIOS_3629.py
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
    'RUNITEM': 'CheckBIOS_3629',
    'Errorcode': 'MBCF4',
    'tool_path': r'C:\WinTest\Tools',
    'instruct': r'call CheckBIOS_Version.bat',
    'result_log_name': r'BIOSversionFlag.txt',
    'check_item': r'In Index/Data/Offset 0x72/0x73/0x72 = 0x22'
}
support.write_json(
    data=dictor,
    path=r'C:\WinTest\JSON\data',
    filename='CheckBIOS_3629.json'
)
"""

try:
    CheckBIOS = support.read_json(
        path=r'C:\WinTest\JSON\data',
        filename='CheckBIOS_3629.json'
    )
    print('CheckBIOS:', CheckBIOS)
    # 测试开始时间
    StartTime = support.titles(
        RUNITEM=CheckBIOS['RUNITEM'],
        stage='start'
    )
    for i in CheckBIOS:
        print(i + ' : ' + CheckBIOS[i])

    # 脚本路径
    currentPath = os.getcwd()
    # currentPath = r'C:\WinTest\Work'
    # print(currentPath)

    # 读取主板写入的mbsn
    MB_SN = support.getMBSN()

    # 判断是否有测试pass的log记录
    if support.passlog(CheckBIOS['RUNITEM']):
        # creatResult
        support.creatResult(
            Fixed=currentPath,
            ItemName=CheckBIOS['RUNITEM'],
            Result=1,
            ItemTag=0
        )
    else:
        # 测试正文
        for n in range(1, 200):
            # 测试内容和结果

            # 读取Model_ini.BAT中信息
            BIOSver = support.get_ini_info(
                param='BIOSVER'
            )
            print(BIOSver)
            print('测试正文')
            chkbios = support.test(
                tool_path=CheckBIOS['tool_path'],
                act='find',
                checklist='NO',
                result_log_name=CheckBIOS['result_log_name'],
                check_item=CheckBIOS['check_item'],
                instruct=CheckBIOS['instruct'],
                check_data=BIOSver
            )
            result = 'fail'
            if chkbios:
                print('BIOS信息检查PASS')
                result = 'pass'
                support.writr_log(
                    path=r'C:\WinTest\LogFile\Check_ECBIOS.log',
                    date='BIOS版本检查PASS，MES定义BIOSVer为%s,实际查询BIOSVer为%s' % (BIOSver, chkbios),
                    act='w'
                )
                support.writr_log(
                    path=r'C:\WinTest\FailLog\%s.log' % CheckBIOS['RUNITEM'],
                    date=BIOSver + '\n',
                    act='a'
                )
            else:
                print('begin to flash %s BIOS at %s' % (BIOSver, StartTime))
                support.writr_log(
                    path=r'C:\WinTest\FailLog\%s.log' % CheckBIOS['RUNITEM'],
                    date='begin to flash %s BIOS at %s' % (BIOSver, StartTime) + '\n',
                    act='w'
                )
                support.flash_bios(
                    path=r'C:\WinTest\Tools',
                    ver=BIOSver + '_SVT2'
                )

            # 判断测试结果
            if result == 'fail':
                if support.judge(
                        FailRetry=CheckBIOS['FailRetry'],
                        FailRetrytimes=CheckBIOS['FailRetrytimes']
                ):
                    CheckBIOS['FailRetry'] = str(int(CheckBIOS['FailRetry']) + 1)
                    print('测试循环次数：' + CheckBIOS['FailRetry'], '，测试结果：fail！！！')
                    continue

                # setinfo
                support.setinfo(
                    RUNITEM=CheckBIOS['RUNITEM'],
                    SN=MB_SN,
                    Result='F',
                    NUM='0',
                    LOGINFO=CheckBIOS['RUNITEM'] + ' Fail',
                    Starttime=StartTime
                )
                print('测试循环次数:', n, '，测试结果：fail！！！！')
                break

            elif result == 'pass':
                print('测试循环次数:', n, '，测试结果：pass！！！')
                print('测试SN:', MB_SN)
                # setinfo
                support.setinfo(
                    RUNITEM=CheckBIOS['RUNITEM'],
                    SN=MB_SN,
                    Result='P',
                    NUM='1',
                    LOGINFO=CheckBIOS['RUNITEM'] + ' Pass',
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
