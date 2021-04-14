# Coding by LiXiao
# Datatime:3/1/2021 2:28 PM
# Filename:WriteDMI.py
# Toolby: PyCharm
import os
import support

"""
WriteDMI = {
    'dictor': {
        'FailRetry': '0',
        'FailRetrytimes': '3',
        'UPLIMIT': '9999.900',
        'LOWLIMIT': '-9999.900',
        'RUNITEM': 'WriteDMI',
        'Errorcode': 'MBCF4',
        'OS_TYPE': 'WIN10P',
        'DBS': '172.24.249.12',  # DatabaseServer
        'DBN': 'MESFA',          # DatabaseName
        'SYS': 'NCBD',           # system
        'STAT': 'GETMESBOM',     # station
        'STEP': 'REQUEST',       # step
        'RFP': 'MB_SN.TXT'       # RequestFilePath
    },
    'check_info': {
        'del_log_path': [r'C:\WinTest\Tools\mbsn.txt', r'C:\WinTest\Tools\MB_SN.TXT', r'C:\WinTest\Tools\Response.bat'],
        'get_response_info_list': ['mktnm', 'osp', 'oa3keyid', 'mt', 'ln', 'KB_PN'],
        'get_response_info_data': ['SET MarketingName=', 'SET MTM_DPKPN=', 'SET ProductkeyID=', 'SET Cust_PN_1=', 'SET SN=', 'SET KBPN='],
        'log_name_list': ['KB.CSV', 'PN.CSV', 'OA3.CSV'],
        'param_list': ['KB_PN', 'mktnm', 'OS_TYPE'],
        'data_list': ['KBID', 'pn', 'oa3key'],
        'DMI_list': ['pn', 'fd', 'mt', 'ln', 'bt', 'pjn', 'oss', 'kd', 'osp', 'oa3keyid'],
        'read_list': {
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
            },
        'check_list': ['OA3Key', 'ProductName', 'MTMPN', 'LenovoSN', 'Brandtype', 'FamilyName', 'ProjectName', 'OS_Descriptor', 'Keyboard_ID', 'DPKPN']
    }
}
support.write_json(
    data=WriteDMI,
    path=r'C:\WinTest\JSON\data',
    filename='WriteDMI.json'
)
"""

try:
    dictor = support.read_json(
        path=r'C:\WinTest\JSON\data',
        filename='WriteDMI.json'
    )
    # 测试开始时间
    StartTime = support.titles(
        RUNITEM=dictor['dictor']['RUNITEM'],
        stage='start'
    )
    for i in dictor['dictor']:
        print(i + ' : ' + dictor['dictor'][i])

    # 脚本路径
    currentPath = os.getcwd()
    # currentPath = r'C:\WinTest\Work'
    # print(currentPath)

    # 读取主板写入的mbsn
    MB_SN = support.getMBSN()


    print('WriteDMI信息为: ', dictor)

    # 判断是否有测试pass的log记录
    if support.passlog(
            dictor['dictor']['RUNITEM']
    ):
        # creatResult
        support.creatResult(
            Fixed=currentPath,
            ItemName=dictor['dictor']['RUNITEM'],
            Result=1,
            ItemTag=0
        )
    else:
        # 测试正文
        for n in range(1, 200):
            # 删除历史遗留测试log
            print(dictor['check_info']['del_log_path'])
            for i in dictor['check_info']['del_log_path']:
                print(i)
                support.del_log(
                    log_path=i
                )
            # 获取 Response.bat
            support.MonitorAgent64(
                DatabaseServer=dictor['dictor']['DBS'],
                DatabaseName=dictor['dictor']['DBN'],
                system=dictor['dictor']['SYS'],
                station=dictor['dictor']['STAT'],
                step=dictor['dictor']['STEP'],
                RequestFilePath=dictor['dictor']['RFP'],
                SN=MB_SN
            )
            # Write DMI
            get_response_info_list = dictor['check_info']['get_response_info_list']
            get_response_info_data = dictor['check_info']['get_response_info_data']

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
                    log_name_list=dictor['check_info']['log_name_list'],
                    param_list=[response_info_list['KB_PN'], response_info_list['mktnm'], dictor['dictor']['OS_TYPE']],
                    data_list=dictor['check_info']['data_list']
                )
                oa3keyid = csv_info['oa3key'].split(',')[1]
                response_info_list['osp'] = 'NONE'
                # print('oa3keyid:', oa3keyid)
            else:
                csv_info = support.get_csv_info(
                    log_name_list=dictor['check_info']['log_name_list'].remove['OA3.CSV'],
                    param_list=[response_info_list['KB_PN'], response_info_list['mktnm']],
                    data_list=dictor['check_info']['data_list'].remove['oa3key']
                )
            print('csv_info:', csv_info)
            pn = csv_info['pn'].split(',')[1]
            fd = csv_info['pn'].split(',')[2]
            print('pn:' + pn + '\nfd:' + fd)

            if pn == '.':
                ex = Exception("ProductName信息获取失败，当前MarketingName信息为：", pn)
                # 抛出异常对象
                raise ex
            DMI_list = dictor['check_info']['DMI_list']
            DMI_info = {
                dictor['check_info']['DMI_list'][0]: csv_info['pn'].split(',')[1],
                dictor['check_info']['DMI_list'][1]: csv_info['pn'].split(',')[2],
                dictor['check_info']['DMI_list'][2]: response_info_list['mt'],
                dictor['check_info']['DMI_list'][3]: response_info_list['ln'],
                dictor['check_info']['DMI_list'][4]: 'C',
                dictor['check_info']['DMI_list'][5]: 'LNVNB161216',
                dictor['check_info']['DMI_list'][6]: 'WIN',
                dictor['check_info']['DMI_list'][7]: csv_info['KBID'].split(',')[2],
                dictor['check_info']['DMI_list'][8]: response_info_list['osp'],
                dictor['check_info']['DMI_list'][9]: oa3keyid
            }
            support.wrtDMI(
                var_list=DMI_list,
                vaule_list=DMI_info
            )

            # Read & Check DMI
            res = ['fail'] * 10
            read_list = dictor['check_info']['read_list']
            read_list_info = support.getDMI(
                var_list=read_list
            )
            print('read_list_info', read_list_info)
            check_list = {
                dictor['check_info']['check_list'][0]: oa3keyid,
                dictor['check_info']['check_list'][1]: csv_info['pn'].split(',')[1],
                dictor['check_info']['check_list'][2]: response_info_list['mt'],
                dictor['check_info']['check_list'][3]: response_info_list['ln'],
                dictor['check_info']['check_list'][4]: 'C',
                dictor['check_info']['check_list'][5]: csv_info['pn'].split(',')[2],
                dictor['check_info']['check_list'][6]: 'LNVNB161216',
                dictor['check_info']['check_list'][7]: 'WIN',
                dictor['check_info']['check_list'][8]: csv_info['KBID'].split(',')[2],
                dictor['check_info']['check_list'][9]: response_info_list['osp']
            }
            print('check_list', check_list)
            result = support.is_equal(read_list_info, check_list)
            print(result)
            Errorcode = ''
            if not result:
                result = 'fail'
                Errorcode = 'HS910'
                break
            elif result:
                result = 'pass'
            else:
                ex = Exception('DMI Check 结果异常！！！', result)
                # 抛出异常对象
                raise ex


            # 判断测试结果
            if result == 'fail':
                if support.judge(
                        FailRetry=dictor['dictor']['FailRetry'],
                        FailRetrytimes=dictor['dictor']['FailRetrytimes']
                ):
                    dictor['dictor']['FailRetry'] = str(int(dictor['dictor']['FailRetry']) + 1)
                    print('测试循环次数：' + dictor['dictor']['FailRetry'], '，测试结果：fail！！！')
                    continue

                # creatResult
                support.creatResult(
                    Fixed=currentPath,
                    ItemName=dictor['dictor']['RUNITEM'],
                    Result=-1,
                    ItemTag=0
                )
                # setinfo
                support.setinfo(
                    RUNITEM=dictor['dictor']['RUNITEM'],
                    SN=MB_SN,
                    Result='F',
                    NUM='0',
                    LOGINFO=dictor['dictor']['RUNITEM'] + ' Fail',
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
                    ItemName=dictor['dictor']['RUNITEM'],
                    Result=1,
                    ItemTag=0
                )
                # setinfo
                support.setinfo(
                    RUNITEM=dictor['dictor']['RUNITEM'],
                    SN=MB_SN,
                    Result='P',
                    NUM='1',
                    LOGINFO=dictor['dictor']['RUNITEM'] + ' Pass',
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
