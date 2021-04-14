# Coding by LiXiao
# Datatime:21/04/14 10:58 AM
# Filename:FCTSTART.py
# Toolby: PyCharm
import os
import support

# 开头模板信息
dictor = {
    'FailRetry': '0',
    'FailRetrytimes': '1',
    'UPLIMIT': '9999.900',
    'LOWLIMIT': '-9999.900',
    'RUNITEM': 'FCTSTART',
    'Errorcode': 'MBCF4',
    'tool_path': 'C:\WinTest\Tools',
    'instruct': 'ShowPassFail.exe',
    'result_log_name': 'FCTSTART.BAT',
    'check_item': ''
}
support.write_json(
    data=dictor,
    path=r'C:\WinTest\JSON\data',
    filename='FCTSTART.json'
)

try:
    FCTSTART = support.read_json(
        path=r'C:\WinTest\JSON\data',
        filename='FCTSTART.json'
    )
    print('FCTSTART:', FCTSTART)
    # 测试开始时间
    StartTime = support.titles(
        RUNITEM=FCTSTART['RUNITEM'],
        stage='start'
    )
    for i in FCTSTART:
        print(i + ' : ' + FCTSTART[i])

    # 脚本路径
    currentPath = os.getcwd()
    # currentPath = r'C:\WinTest\Work'
    # print(currentPath)

    # 读取主板写入的mbsn
    MB_SN = support.getMBSN()

    # 判断是否有测试pass的log记录
    if support.passlog(FCTSTART['RUNITEM']):
        # creatResult
        support.creatResult(
            Fixed=currentPath,
            ItemName=FCTSTART['RUNITEM'],
            Result=1,
            ItemTag=0
        )
    else:
        # 测试正文
        for n in range(1, 200):
            # 测试内容和结果


            chkec = support.test(
                tool_path=FCTSTART['tool_path'],
                act='read',
                checklist='NO',
                result_log_name=FCTSTART['result_log_name1'],
                check_item=FCTSTART['check_item1'],
                instruct=FCTSTART['instruct1'],
                check_data=‘
            )
            chkec = FCTSTART[0:2] + chkec[2:]
            Errorcode = '.'
            result = 'fail'
            if chkbios == BIOSver:
                print('BIOS版本检查PASS，MES定义BIOSVer为%s,实际查询BIOSVer为%s' % (BIOSver, chkbios))
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
                if chkec == ECver:
                    result = 'pass'
                    print('EC版本检查PASS，MES定义ECVer为%s,实际查询ECVer为%s' % (ECver, chkec))
                    support.writr_log(
                    path=r'C:\WinTest\FailLog\%s.log' % CheckBIOS['RUNITEM'],
                        date=ECver + '\n',
                        act='a'
                    )
                else:
                    Errorcode = 'HS946'
                    result = 'fail'
            else:
                print('begin to flash %s BIOS at %s' % (BIOSver, StartTime))
                support.writr_log(
                    path=r'C:\WinTest\FailLog\%s.log' % CheckBIOS['RUNITEM'],
                    date='begin to flash %s BIOS at %s' % (BIOSver, StartTime) + '\n',
                    act='w'
                )
                support.flash_bios(
                    path=r'C:\WinTest\Tools',
                    ver=BIOSver
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

                # creatResult
                support.creatResult(
                    Fixed=currentPath,
                    ItemName=CheckBIOS['RUNITEM'],
                    Result=-1,
                    ItemTag=0
                )
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
                    ItemName=CheckBIOS['RUNITEM'],
                    Result=1,
                    ItemTag=0
                )
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
    print(e)
    print("SN匹配信息错误，请检查正则表达式！！！")

except Exception as e:
    print(e)
