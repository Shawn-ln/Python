# Coding by LiXiao
# Datatime:3/3/2021 5:56 PM
# Filename:WriteUUID.py
# Toolby: PyCharm
import os
import support

# 开头模板信息
dictor = {
    'FailRetry':'0',
    'FailRetrytimes':'10',
    'UPLIMIT':'9999.900',
    'LOWLIMIT':'-9999.900',
    'RUNITEM':'WriteUUID',
    'Errorcode':'MBCF4',
    'tool_path':'C:\WinTest\Work'
}

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
    MB_SN = support.getSN()

    # 判断是否有测试pass的log记录
    if support.passlog(dictor['RUNITEM']):
        # creatResult
        support.creatResult(Fixed=currentPath, ItemName=dictor['RUNITEM'], Result=1, ItemTag=0)
    else:
        # 测试正文
        for n in range(1, 200):
            # 测试内容和结果
            Y = StartTime[0:4]
            print(Y)
            M = StartTime[5:7]
            print(M)
            D = StartTime[8:10]
            print(D)
            WIFIMAC = support.getMAC(MACID='WirelessMAC')
            BTMAC = support.getMAC(MACID='BluetoothMAC')
            if len(WIFIMAC) == 12:
                print('WIFIMAC:' + WIFIMAC)
            else:
                ex = Exception('WLAN_MAC地址长度错误，正确应为12码，实际' + str(len(WIFIMAC)) + '码请到设备管理器检查无线网卡和蓝牙是否能抓到，没被禁用，没黄标')
                # 抛出异常对象
                raise ex
            if len(BTMAC) == 12:
                print('BTMAC:' + BTMAC)
            else:
                ex = Exception('BT_MAC地址长度错误，正确应为12码，实际' + str(len(BTMAC)) + '码请到设备管理器检查无线网卡和蓝牙是否能抓到，没被禁用，没黄标')
                # 抛出异常对象
                raise ex
            UUID_BTMAC = BTMAC[0:2] + ' ' + BTMAC[2:4] + ' ' + BTMAC[4:6] + ' ' + BTMAC[6:8] + ' ' + BTMAC[8:10] + ' ' + BTMAC[10:12]
            UUID_WIFIMAC = WIFIMAC[2:4] + ' ' + WIFIMAC[0:2] + ' ' + WIFIMAC[6:8] + ' ' + WIFIMAC[4:6] + ' ' + WIFIMAC[8:10] + ' ' + WIFIMAC[10:12]
            print(UUID_BTMAC)
            print(UUID_WIFIMAC)

            UUIDW = D + ' ' + M + ' ' + Y[2:4] + ' ' + Y[0:2] + ' ' + UUID_WIFIMAC + ' ' + UUID_BTMAC
            UUIDR = Y + M + D + '-' + WIFIMAC[0:4] + '-' + WIFIMAC[4:8] + '-' + WIFIMAC[8:12] + '-' + BTMAC
            print(UUIDW)
            print(UUIDR)


            print('测试正文')
            Errorcode = '.'
            result = '.'
            if WIFIMAC == '.':
                if BTMAC == '.':
                    Errorcode = 'HS946'
                    result = 'fail'
            else:
                result = 'pass'

            # 判断测试结果
            if result == 'fail':
                if support.judge(FailRetry=dictor['FailRetry'], FailRetrytimes=dictor['FailRetrytimes']):
                    dictor['FailRetry'] = str(int(dictor['FailRetry']) + 1)
                    print('测试循环次数：' + dictor['FailRetry'], '，测试结果：fail！！！')
                    continue

                # 计算测试时间
                TestTimes = support.gettesttime(start=StartTime)
                print('测试用时:', TestTimes)
                # creatResult
                support.creatResult(Fixed=currentPath, ItemName=dictor['RUNITEM'], Result=-1, ItemTag=0)
                # setinfo
                support.setinfo(RUNITEM=dictor['RUNITEM'], SN=MB_SN, UPLIMIT=dictor['UPLIMIT'],
                                LOWLIMIT=dictor['LOWLIMIT'], Result='F', NUM='0',
                                LOGINFO=dictor['RUNITEM'] + ' Fail', Starttime=StartTime, TestTime=TestTimes)
                print('测试循环次数:', n, '，测试结果：fail！！！！')
                support.message(Code=Errorcode)
                break

            elif result == 'pass':
                print('测试循环次数:', n, '，测试结果：pass！！！')
                print('测试SN:', MB_SN)
                # 计算测试时间
                TestTimes = support.gettesttime(start=StartTime)
                print('测试用时:', TestTimes)
                # creatResult
                support.creatResult(Fixed=currentPath, ItemName=dictor['RUNITEM'], Result=1, ItemTag=0)
                # setinfo
                support.setinfo(RUNITEM=dictor['RUNITEM'], SN=MB_SN, UPLIMIT=dictor['UPLIMIT'],
                                LOWLIMIT=dictor['LOWLIMIT'], Result='P', NUM='1',
                                LOGINFO=dictor['RUNITEM'] + ' Pass', Starttime=StartTime, TestTime=TestTimes)
                break

            else:
                print('无测试结果！！！')


except AttributeError as e:
    print(e)
    print("SN匹配信息错误，请检查正则表达式！！！")

except Exception as e:
    print(e)

