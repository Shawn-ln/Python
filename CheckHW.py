# Coding by LiXiao
# Datatime:3/8/2021 3:25 PM
# Filename:CheckHW.py
# Toolby: PyCharm

import os
from shutil import copyfile
import support

# 开头模板信息

CheckHW = {
    # 开头模板信息
    'dictor': {
        'FailRetry': '0',
        'FailRetrytimes': '1',
        'UPLIMIT': '9999.900',
        'LOWLIMIT': '-9999.900',
        'RUNITEM': 'CheckHW',
        'instruct': 'BlueTooth.exe',
        'Errorcode': 'HT942',
        'tool_path': r'C:\WinTest\Tools',
        'result_log_name': 'bluetooth.log'
    },
    # HWConfig
    'HWConfig': {
        'CPUES': 'AMD',
        'ODD': 'NO',
        'CPU': 'OnBoard',
        'GPU': 'NO',
        'RAM': 'OnBoard',
        'LCD': 'YES',
        'LCM': 'NO',
        'SSD': 'YES',
        'HDD': 'NO',
        'CAM': 'YES',
        'FCAM': 'NO',
        'RCAM': 'NO',
        'KB': 'YES',
        'DOCKPN': 'NO',
        'KBLT': 'YES',
        'WLAN': 'OnBoard',
        'BT': 'OnBoard',
        'LTE': 'NO',
        'FP': 'NO',
        'TPFW': 'YES',
        'PDFW': 'YES',
        'TBTFW': 'YES',
        'HDDC1': '1',
        'HDDC2': '2'
    },
    # 测试项信息
    'check_info': {
        'get_response_info_list': ['ptdcode', 'MBPN', 'SSDPN', 'HDDPN', 'LCDPN', 'LCMPN', 'WIFIPN', 'FCAMPN', 'CAMPN', 'RCAMPN', 'BATTPN', 'TPPN', 'DOCKPN', 'KBPN'],
        'get_response_info_data': ['SET ToolAuthenticationCodeByPSN=', 'SET MBPN=', 'SET SSDPN=', 'SET HDDPN=', 'SET LCDPN=', 'SET LCMPN=', 'SET WIFIPN=', 'SET FCAMPN=', 'SET CAMPN=', 'SET RCAMPN=', 'SET BATTPN=', 'SET TPPN=', 'SET DOCKPN=', 'SET KBPN='],
        'log_name_list': ['CPU.CSV', 'BATT.CSV', 'TPD.CSV', 'RAM.CSV'],
        'data_list': ['cpu_info_list', 'batt_info_list', 'tpd_info_list', 'ram_info_list']
    }
}

support.write_json(
    data=CheckHW,
    path=r'C:\WinTest\JSON\data',
    filename='CheckHW.json'
)

print('1------------------------------------------------------------------------\n')

try:
    CheckHW = support.read_json(
        path=r'C:\WinTest\JSON\data',
        filename='CheckHW.json'
    )
    print(CheckHW)
    # 测试开始时间
    StartTime = support.titles(
        RUNITEM=CheckHW['dictor']['RUNITEM'],
        stage='start'
    )
    for i in CheckHW['dictor']:
        print(i + ' : ' + CheckHW['dictor'][i])

    # 脚本路径
    currentPath = os.getcwd()
    # currentPath = r'C:\WinTest\Work'
    # print(currentPath)

    # 读取主板写入的mbsn
    MB_SN = support.getSN()

    # 判断是否有测试pass的log记录
    if support.passlog(CheckHW['dictor']['RUNITEM']):
        # creatResult
        support.creatResult(
            Fixed=currentPath,
            ItemName=CheckHW['dictor']['RUNITEM'],
            Result=1,
            ItemTag=0
        )
    else:
        # 测试正文
        for n in range(1, 200):
            # 测试内容和结果
            Errorcode = '.'
            print('测试工具注册')
            response_info_list = support.get_response_info(
                lists=CheckHW['check_info']['get_response_info_list'],
                date=CheckHW['check_info']['get_response_info_data']
            )
            print('response_info_list:', response_info_list)
            if response_info_list['ptdcode'] is None:
                ex = Exception('工具注册码获取失败！！！')
                # 抛出异常对象
                raise ex
            param_list = [response_info_list['MBPN'], response_info_list['BATTPN'], response_info_list['TPPN'], response_info_list['MBPN']]

            # 获取LCD信息
            if CheckHW['HWConfig']['LCD'] == 'YES':
                CheckHW['check_info']['log_name_list'].append('LCD.CSV')
                param_list.append('LCDPN')
                CheckHW['check_info']['data_list'].append('lcd_info_list')
            elif CheckHW['HWConfig']['LCM'] == 'YES':
                CheckHW['check_info']['log_name_list'].append('LCD.CSV')
                param_list.append('LCMPN')
                CheckHW['check_info']['data_list'].append('lcd_info_list')
            else:
                ex = Exception('LCD信息获取失败，请检查"HWConfig"中定义信息！！！')
                # 抛出异常对象
                raise ex

            # 获取SSD信息
            if CheckHW['HWConfig']['SSD'] == 'OnBoard':
                CheckHW['check_info']['log_name_list'].append('SSD.CSV')
                param_list.append('MBPN')
                CheckHW['check_info']['data_list'].append('ssd_info_list')
            elif CheckHW['HWConfig']['SSD'] == 'YES':
                CheckHW['check_info']['log_name_list'].append('SSD.CSV')
                param_list.append('SSDPN')
                CheckHW['check_info']['data_list'].append('ssd_info_list')
            elif CheckHW['HWConfig']['HDD'] == 'YES':
                CheckHW['check_info']['log_name_list'].append('SSD.CSV')
                param_list.append('HDDPN')
                CheckHW['check_info']['data_list'].append('ssd_info_list')
            else:
                ex = Exception('SSD信息获取失败，请检查"HWConfig"中定义信息！！！')
                # 抛出异常对象
                raise ex

            # 获取WLAN信息
            if CheckHW['HWConfig']['WLAN'] == 'OnBoard':
                CheckHW['check_info']['log_name_list'].append('WLAN.CSV')
                param_list.append('MBPN')
                CheckHW['check_info']['data_list'].append('wlan_info_list')
            elif CheckHW['HWConfig']['WLAN'] == 'COMBO':
                CheckHW['check_info']['log_name_list'].append('WLAN.CSV')
                param_list.append('WIFIPN')
                CheckHW['check_info']['data_list'].append('wlan_info_list')
            else:
                ex = Exception('WLAN信息获取失败，请检查"HWConfig"中定义信息！！！')
                # 抛出异常对象
                raise ex

            # 获取KB信息
            if CheckHW['HWConfig']['KB'] == 'YES':
                CheckHW['check_info']['log_name_list'].append('KB.CSV')
                param_list.append('KBPN')
                CheckHW['check_info']['data_list'].append('kb_info_list')
            elif CheckHW['HWConfig']['DOCKPN'] == 'YES':
                CheckHW['check_info']['log_name_list'].append('KB.CSV')
                param_list.append('DOCKPN')
                CheckHW['check_info']['data_list'].append('kb_info_list')
            else:
                ex = Exception('KB信息获取失败，请检查"HWConfig"中定义信息！！！')
                # 抛出异常对象
                raise ex

            # 获取FCAM信息
            if CheckHW['HWConfig']['CAM'] == 'YES':
                CheckHW['check_info']['log_name_list'].append('FCAM.CSV')
                param_list.append('CAMPN')
                CheckHW['check_info']['data_list'].append('fcam_info_list')
            elif CheckHW['HWConfig']['FCAM'] == 'YES':
                CheckHW['check_info']['log_name_list'].append('FCAM.CSV')
                param_list.append('FCAMPN')
                CheckHW['check_info']['data_list'].append('fcam_info_list')
            else:
                ex = Exception('FCAM信息获取失败，请检查"HWConfig"中定义信息！！！')
                # 抛出异常对象
                raise ex

            # 获取RCAM信息
            if CheckHW['HWConfig']['RCAM'] == 'SPECIAL':
                CheckHW['check_info']['log_name_list'].append('RCAM.CSV')
                param_list.append('RCAMPN')
                CheckHW['check_info']['data_list'].append('rcam_info_list')
            elif CheckHW['HWConfig']['RCAM'] == 'YES':
                CheckHW['check_info']['log_name_list'].append('RCAM.CSV')
                param_list.append('RCAMPN')
                CheckHW['check_info']['data_list'].append('rcam_info_list')
            elif CheckHW['HWConfig']['RCAM'] == 'NO':
                print('此配置不带后摄！！！')
            else:
                ex = Exception('RCAM信息获取失败，请检查"HWConfig"中定义信息！！！')
                # 抛出异常对象
                raise ex

            a = ['cpu', 'batt', 'tpd', 'ram', 'lcd', 'ssd', 'wlan', 'kb', 'fcam', 'rcam']

            csv_info_list = support.get_csv_info(
                log_name_list=CheckHW['check_info']['log_name_list'],
                param_list=[response_info_list['MBPN'], response_info_list['BATTPN'], response_info_list['TPPN'], response_info_list['MBPN']],
                data_list=CheckHW['check_info']['data_list']
            )
            print('csv_info_list:', csv_info_list)
            struct = 'PTDRegRun.exe %s >regist.txt' % response_info_list['ptdcode']
            print(struct)
            ptd_res = support.test(
                tool_path=CheckHW['dictor']['tool_path'],
                result_log_name='regist.txt',
                act='find',
                checklist='NO',
                instruct=struct,
                check_item='Activation',
                check_data='Activation Successful'
            )
            if ptd_res:
                print('注册结果:', ptd_res)
            else:
                ex = Exception('工具注册失败！！！')
                # 抛出异常对象
                raise ex

            print('设备管理器黄标检查')
            support.del_log(
                log_path=r'C:\WinTest\Tools\Device.bat'
            )
            device_chk_struct = 'DeviceYellowCheck.exe >Device.bat'
            device_chk_res = support.test(
                tool_path=CheckHW['dictor']['tool_path'],
                result_log_name='Device.bat',
                checklist='NO',
                act='find',
                instruct=device_chk_struct,
                check_item='CheckDevice',
                check_data='CheckDevice=PASS'
            )
            if device_chk_res:
                print('Device check pass!!!')
                copyfile(
                    src='Device.bat',
                    dst=r'C:\WinTest\LogFile' + '\\' + 'CheckDevice.log'
                )
            else:
                print('Device check fail!!!')
                Errorcode = 'Yellow'
                result = 'fail'

            if Errorcode == '.':
                print('CPU类型检查')
                support.del_log(r'C:\WinTest\Tools\CPU.BAT')
                cpu_info = support.get_csv_info(
                    log_name_list=CheckHW['check_info']['log_name_list'],
                    param_list=[response_info_list['KB_PN'], response_info_list['mktnm'], CheckHW['dictor']['OS_TYPE']],
                    data_list=CheckHW['check_info']['data_list']
                )
                print('cpu_info:', cpu_info)
                cpu_info_list = cpu_info.split(',')  # 用”,“将CPU信息分隔开
                print('cpu_info_list', cpu_info_list)
                cpu_chk_stract = 'PC_CPU.exe /set >CPU.BAT'
                check_list = ['CPU_Model', 'CPU_ID', 'CPU_Speed']
                cpu_info_uut = support.test(
                    tool_path=CheckHW['dictor']['tool_path'],
                    result_log_name='CPU.BAT',
                    checklist='YES',
                    act='read',
                    instruct=cpu_chk_stract,
                    check_item=check_list,
                    check_data=''
                )
                print('cpu_info_uut:', cpu_info_uut)
                if cpu_info_uut['CPU_Model'] == cpu_info_list[1]:
                    if cpu_info_uut['CPU_ID'][12:] == cpu_info_list[2]:
                        if cpu_info_uut['CPU_Speed'] == cpu_info_list[3]:
                            print('CPU类型检查PASS!!!')
                            copyfile(
                                src=r'C:\WinTest\Tools\CPU.BAT',
                                dst=r'C:\WinTest\LogFile' + '\\' + 'Check_CPU.log'
                            )
                        else:
                            code = 'MBCF2'
                            msg1 = 'CPU_Speed检查失败,MES定义CPU_Speed为:' + cpu_info_list[3] + ',实际组装CPU_Speed为:' + cpu_info_uut['CPU_Speed']
                            print(msg1)
                            support.setmsg(
                                Errorcode=code,
                                msg=msg1
                            )
                    else:
                        code = 'MBCF2'
                        msg1 = 'CPU_ID检查失败,MES定义CPU_ID为:' + cpu_info_list[2] + ',实际组装CPU_ID类型为:' + cpu_info_uut['CPU_ID'][12:]
                        print(msg1)
                        support.setmsg(
                            Errorcode=code,
                            msg=msg1
                        )
                else:
                    code = 'MBCF2'
                    msg1 = 'CPU_Model检查失败,MES定义CPU_Model为:' + cpu_info_list[1]+ ',实际组装CPU_Model类型为:' + cpu_info_uut['CPU_Model']
                    print(msg1)
                    support.setmsg(
                        Errorcode=code,
                        msg=msg1
                    )

            if Errorcode == '.':
                print('RAM类型检查')
                support.del_log(r'C:\WinTest\Tools\RAM.BAT')
                mbpn = support.get_response_info(
                    param='MBPN'
                )
                print('mbpn', mbpn)
                ram_info = support.get_csv_info(
                    log_name='RAM.CSV',
                    param=mbpn
                )
                print('ram_info:', ram_info)
                ram_info_list = ram_info.split(',')
                print(ram_info_list)
                ram_chk_stract = 'SMBIOS.exe >RAM.BAT'
                ram_size = support.test(
                    tool_path=CheckHW['dictor']['tool_path'],
                    result_log_name='RAM.BAT',
                    act='read',
                    checklist='NO',
                    instruct=ram_chk_stract,
                    check_item='RAMTotalSize',
                    check_data=''
                )
                ram_vender = support.test(
                    tool_path=CheckHW['dictor']['tool_path'],
                    result_log_name='RAM.BAT',
                    act='read',
                    checklist='NO',
                    instruct=ram_chk_stract,
                    check_item='Slot1_Vendor',
                    check_data=''
                )

                print(ram_size, ram_info_list[2], ram_vender, ram_info_list[1])
                if ram_size == ram_info_list[2]:
                    if ram_vender == ram_info_list[1]:
                        print('RAM类型检查PASS!!!')
                        copyfile(
                            src=r'C:\WinTest\Tools\RAM.BAT',
                            dst=r'C:\WinTest\LogFile' + '\\' + 'Check_RAM.log'
                        )
                    else:
                        code = 'MBCF3'
                        msg1 = 'RAM厂商类型检查失败,MES定义RAM厂商类型为:' + ram_vender + ',实际组装RAM厂商类型为:' + ram_info_list[1]
                        print(msg1)
                        support.setmsg(Errorcode=code, msg=msg1)
                        result = 'fail'

            result = 'fail'

            # 判断测试结果
            if result == 'fail':
                if support.judge(
                        FailRetry=CheckHW['dictor']['FailRetry'],
                        FailRetrytimes=CheckHW['dictor']['FailRetrytimes']
                ):
                    CheckHW['dictor']['FailRetry'] = str(int(CheckHW['dictor']['FailRetry']) + 1)
                    print('测试循环次数：' + CheckHW['dictor']['FailRetry'], '，测试结果：fail！！！')
                    continue

                # CreateResult
                support.creatResult(
                    Fixed=currentPath,
                    ItemName=CheckHW['dictor']['RUNITEM'],
                    Result=-1,
                    ItemTag=0
                )
                # SetInfo
                support.setinfo(
                    RUNITEM=CheckHW['dictor']['RUNITEM'],
                    SN=MB_SN,
                    Result='F',
                    NUM='0',
                    LOGINFO=CheckHW['dictor']['RUNITEM'] + ' Fail',
                    Starttime=StartTime
                )
                print('测试循环次数:', n, '，测试结果：fail！！！！')
                support.message(Code=Errorcode)
                break

            elif result == 'pass':
                print('测试循环次数:', n, '，测试结果：pass！！！')
                print('测试SN:', MB_SN)
                # CreateResult
                support.creatResult(
                    Fixed=currentPath,
                    ItemName=CheckHW['dictor']['RUNITEM'],
                    Result=1,
                    ItemTag=0
                )
                # SetInfo
                support.setinfo(
                    RUNITEM=CheckHW['dictor']['RUNITEM'],
                    SN=MB_SN,
                    Result='P',
                    NUM='1',
                    LOGINFO=CheckHW['dictor']['RUNITEM'] + ' Pass',
                    Starttime=StartTime
                )
                break

            else:
                print('无测试结果！！！')


except AttributeError as e:
    print(e)
    print('SN匹配信息错误，请检查正则表达式！！！')

except Exception as e:
    print(e)
