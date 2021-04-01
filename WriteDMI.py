# Coding by LiXiao
# Datatime:3/1/2021 2:28 PM
# Filename:WriteDMI.py
# Toolby: PyCharm
import os
import support

dictor = {
    'FailRetry': '0',
    'FailRetrytimes': '3',
    'UPLIMIT': '9999.900',
    'LOWLIMIT': '-9999.900',
    'RUNITEM': 'WriteDMI',
    'Errorcode': 'MBCF4',
    'OS_TYPE': 'WIN10P',
    'DBS': '172.24.249.12',    # DatabaseServer
    'DBN': 'MESFA',            # DatabaseName
    'SYS': 'NCBD',             # system
    'STAT': 'GETMESBOM',       # station
    'STEP': 'REQUEST',         # step
    'RFP': 'MB_SN.TXT'         # RequestFilePath
}

try:
    # 测试开始时间
    StartTime = support.titles(
        RUNITEM=dictor['RUNITEM'],
        stage='start'
    )
    for i in dictor:
        print(i + ' : ' + dictor[i])

    # 脚本路径
    currentPath = os.getcwd()
    # currentPath = r'C:\WinTest\Work'
    # print(currentPath)

    # 读取主板写入的mbsn
    MB_SN = support.getMBSN()

    # 判断是否有测试pass的log记录
    if support.passlog(
            dictor['RUNITEM']
    ):
        # creatResult
        support.creatResult(
            Fixed=currentPath,
            ItemName=dictor['RUNITEM'],
            Result=1,
            ItemTag=0
        )
    else:
        # 测试正文
        for n in range(1, 200):
            # 删除历史遗留测试log
            support.del_log(
                log_path=r'C:\WinTest\Tools\mbsn.txt'
            )
            support.del_log(
                log_path=r'C:\WinTest\Tools\MB_SN.TXT'
            )
            support.del_log(
                log_path=r'C:\WinTest\Tools\Response.bat'
            )
            # 获取 Response.bat
            support.MonitorAgent64(
                DatabaseServer=dictor['DBS'],
                DatabaseName=dictor['DBN'],
                system=dictor['SYS'],
                station=dictor['STAT'],
                step=dictor['STEP'],
                RequestFilePath=dictor['RFP'],
                SN=MB_SN
            )
            # Write DMI
            get_response_info_list = ('mktnm', 'osp', 'oa3keyid', 'mt', 'ln', 'KB_PN')
            get_response_info_data = ('SET MarketingName=', 'SET MTM_DPKPN=', 'SET ProductkeyID=', 'SET Cust_PN_1=', 'SET SN=', 'SET KBPN=')
            response_info_list = support.get_response_info(
                lists=get_response_info_list,
                date=get_response_info_data
            )
            print('response_info_list:', response_info_list)
            oa3keyid = response_info_list['oa3keyid']
            print('oa3keyid:', oa3keyid)

            pn = '.'
            fd = '.'

            if response_info_list['oa3keyid'] == 'NONE':
                csv_info = support.get_csv_info(
                    log_name_list=('KB.CSV', 'PN.CSV', 'OA3.CSV'),
                    param_list=(response_info_list['KB_PN'], response_info_list['mktnm'], dictor['OS_TYPE']),
                    data_list=('KBID', 'pn', 'oa3key')
                )
                oa3keyid = csv_info['oa3key'].split(',')[1]
                response_info_list['osp'] = 'NONE'
                # print('oa3keyid:', oa3keyid)
            else:
                csv_info = support.get_csv_info(
                    log_name_list=('KB.CSV', 'PN.CSV'),
                    param_list=(response_info_list['KB_PN'], response_info_list['mktnm']),
                    data_list=('KBID', 'pn')
                )
            print('csv_info:', csv_info)
            pn = csv_info['pn'].split(',')[1]
            fd = csv_info['pn'].split(',')[2]
            print('pn:' + pn + '\nfd:' + fd)

            if pn == '.':
                ex = Exception("ProductName信息获取失败，当前MarketingName信息为：", pn)
                # 抛出异常对象
                raise ex
            DMI_list = ('pn', 'fd', 'mt', 'ln', 'bt', 'pjn', 'oss', 'kd', 'osp', 'oa3keyid')
            DMI_info = {
                'pn': csv_info['pn'].split(',')[1],
                'fd': csv_info['pn'].split(',')[2],
                'mt': response_info_list['mt'],
                'ln': response_info_list['ln'],
                'bt': 'C',
                'pjn': 'LNVNB161216',
                'oss': 'WIN',
                'kd': csv_info['KBID'].split(',')[2],
                'osp': response_info_list['osp'],
                'oa3keyid': oa3keyid
            }
            support.wrtDMI(
                var_list=DMI_list,
                vaule_list=DMI_info
            )

            # Read & Check DMI
            res = ['fail'] * 10
            read_list = {
                'OA3Key': 'oa3keyid',
                'ProductName': 'pn',
                'MTMPN': 'mt',
                'LenovoSN': 'ln',
                'Brandtype': 'bt',
                'FamilyName': 'fd',
                'ProjectName': 'pjn',
                'OS_Descriptor': 'oss',
                'Keyboard_ID': 'kd',
                'DPKPN': 'osp'
            }
            read_list_info = support.getDMI(var_list=read_list)
            print('read_list_info', read_list_info)
            check_list = {
                'OA3Key': oa3keyid,
                'ProductName': csv_info['pn'].split(',')[1],
                'MTMPN': response_info_list['mt'],
                'LenovoSN': response_info_list['ln'],
                'Brandtype': 'C',
                'FamilyName': csv_info['pn'].split(',')[2],
                'ProjectName': 'LNVNB161216',
                'OS_Descriptor': 'WIN',
                'Keyboard_ID': csv_info['KBID'].split(',')[2],
                'DPKPN': response_info_list['osp']
            }
            print('check_list', check_list)
            result = ''
            result = support.is_equal(read_list_info, check_list)
            print(result)
            Errorcode = ''
            if result == False:
                result = 'fail'
                Errorcode = 'HS910'
                break
            elif result == True:
                result = 'pass'
            else:
                ex = Exception('DMI Check 结果异常！！！', result)
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
