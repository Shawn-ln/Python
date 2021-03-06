# Coding by LiXiao
# Datatime:3/8/2021 3:25 PM
# Filename:CheckHW.py
# Toolby: PyCharm

import os
from shutil import copyfile
import support

"""
dictor = {
    'dictor':
        {
            'FailRetry': '0',
            'FailRetrytimes': '0',
            'UPLIMIT': '9999.900',
            'LOWLIMIT': '-9999.900',
            'RUNITEM': 'CheckHW',
            'instruct': 'BlueTooth.exe',
            'Errorcode': 'HT942',
            'tool_path': r'C:\WinTest\Tools',
            'ptd_chk_item': 'Activation',
            'ptd_chk_data': 'Activation Successful',
            'device_chk_struct': 'DeviceYellowCheck.exe >Device.bat',
            'device_chk_item': 'CheckDevice',
            'device_chk_data': 'CheckDevice=PASS',
            'gpu_chk_stract': r'AT_VramInfo.exe >GPUinfo.BAT',
            'gpu_check_list': ['VGA1Description', 'VGA1VGA_RAM'],
            'cpu_chk_stract': 'PC_CPU.exe /set >CPU.BAT',
            'cpu_check_list': ['CPU_Model', 'CPU_ID', 'CPU_Speed'],
            'ram_chk_stract': 'SMBIOS.exe >RAM.BAT',
            'ram_chk_list': ['RAMTotalSize', 'Slot1_Vendor', 'Slot1_RAMFrequency'],
            'ssd_chk_stract': 'HDDInfo.exe >SSD.BAT',
            'ssd_chk_list': ['HDD1_MD', 'HDD1_FW', 'HDD1_SZ'],
            'lcd_chk_stract': 'EDID.exe >LCD.BAT',
            'lcd_chk_list': ['LCDID'],
            'wlan_check_list': ['PCI'],
            'bt_check_list': ['USB\\VID'],
            'fcam_check_list': ['USB\\VID'],
            'ircam_check_list': ['USB\\VID'],
            'batt_chk_stract': r'Battery.exe -A >BATT.BAT&Battery.exe -B >>BATT.BAT',
            'batt_chk_list': ['BatteryDeviceName', 'BatteryDesignCapacity'],
            'tpd_chk_stract_Synaptics': r'GetPackrat.exe /v /s 3 >FWversion.txt',
            'tpd_chk_list_Synaptics': ['FW'],
            'tpd_chk_stract_Elan': r'ElanFWVerReader.exe -autoclose 1',
            'tpd_chk_list_Elan': ['0x']
        },
    'HWConfig': {
        'CPUES': 'AMD',
        'ODD': 'NO',
        'CPU': 'OnBoard',
        'GPU': 'NO',
        'RAM': 'OnBoard',
        'LCD': 'NO',
        'LCM': 'YES',
        'SSD': 'YES',
        'HDD': 'NO',
        'CAM': 'YES',
        'IRCAM': 'NO',
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
    'check_info': {
        'get_response_info_list': ['ptdcode', 'MBPN', 'SSDPN', 'HDDPN', 'LCDPN', 'LCMPN', 'WIFIPN', 'FCAMPN', 'CAMPN', 'RCAMPN', 'BATTPN', 'TPPN', 'DOCKPN', 'KBPN'],
        'get_response_info_data': ['SET ToolAuthenticationCodeByPSN=', 'SET MBPN=', 'SET SSDPN=', 'SET HDDPN=', 'SET LCDPN=', 'SET LCMPN=', 'SET WIFIPN=', 'SET FCAMPN=', 'SET CAMPN=', 'SET RCAMPN=', 'SET BATTPN=', 'SET TPPN=', 'SET DOCKPN=', 'SET KBPN='],
        'log_name_list': ['MB.CSV', 'BATT.CSV', 'TPD.CSV', 'RAM.CSV'],
        'data_list': ['cpu_info_list', 'batt_info_list', 'tpd_info_list', 'ram_info_list']
        }
}
support.write_json(
    data=dictor,
    path=r'C:\WinTest\JSON\data',
    filename='CheckHW.json'
)
"""

try:
    result = 'fail'
    CheckHW = support.read_json(
        path=r'C:\WinTest\JSON\data',
        filename='CheckHW.json'
    )
    # print(CheckHW)
    # 测试开始时间
    StartTime = support.titles(
        RUNITEM=CheckHW['dictor']['RUNITEM'],
        stage='start'
    )

    # 脚本路径
    currentPath = os.getcwd()
    # currentPath = r'C:\WinTest\Work'
    # print(currentPath)

    # 读取主板写入的mbsn
    MB_SN = support.getSN()
    HWConfig = {
        'SN': MB_SN
    }
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
            print('param_list:', param_list)

            # 获取LCD信息
            if CheckHW['HWConfig']['LCD'] == 'YES':
                CheckHW['check_info']['log_name_list'].append('LCD.CSV')
                param_list.append(response_info_list['LCDPN'])
                CheckHW['check_info']['data_list'].append('lcd_info_list')
                LCD = response_info_list['LCDPN'] + '(LCDPN)'
            elif CheckHW['HWConfig']['LCM'] == 'YES':
                CheckHW['check_info']['log_name_list'].append('LCD.CSV')
                param_list.append(response_info_list['LCMPN'])
                CheckHW['check_info']['data_list'].append('lcd_info_list')
                LCD = response_info_list['LCMPN'] + '(LCMPN)'
            else:
                ex = Exception('LCD信息获取失败，请检查"HWConfig"中定义信息！！！')
                # 抛出异常对象
                raise ex
            print('获取LCD信息:', CheckHW['check_info'])

            # 获取SSD信息
            if CheckHW['HWConfig']['SSD'] == 'OnBoard':
                CheckHW['check_info']['log_name_list'].append('SSD.CSV')
                param_list.append(response_info_list['MBPN'])
                CheckHW['check_info']['data_list'].append('ssd_info_list')
                SSD = response_info_list['MBPN'] + '(MBPN)'
            elif CheckHW['HWConfig']['SSD'] == 'YES':
                CheckHW['check_info']['log_name_list'].append('SSD.CSV')
                param_list.append(response_info_list['SSDPN'])
                CheckHW['check_info']['data_list'].append('ssd_info_list')
                SSD = response_info_list['SSDPN'] + '(SSDPN)'
            elif CheckHW['HWConfig']['HDD'] == 'YES':
                CheckHW['check_info']['log_name_list'].append('SSD.CSV')
                param_list.append(response_info_list['HDDPN'])
                CheckHW['check_info']['data_list'].append('ssd_info_list')
                SSD = response_info_list['HDDPN'] + '(HDDPN)'
            else:
                ex = Exception('SSD信息获取失败，请检查"HWConfig"中定义信息！！！')
                # 抛出异常对象
                raise ex
            print('获取SSD信息:', CheckHW['check_info'])

            # 获取WLAN信息
            if CheckHW['HWConfig']['WLAN'] == 'OnBoard':
                CheckHW['check_info']['log_name_list'].append('WLAN.CSV')
                param_list.append(response_info_list['MBPN'])
                CheckHW['check_info']['data_list'].append('wlan_info_list')
                WLAN = response_info_list['MBPN'] + '(MBPN)'
            elif CheckHW['HWConfig']['WLAN'] == 'COMBO':
                CheckHW['check_info']['log_name_list'].append('WLAN.CSV')
                param_list.append(response_info_list['WIFIPN'])
                CheckHW['check_info']['data_list'].append('wlan_info_list')
                WLAN = response_info_list['WIFIPN'] + '(WIFIPN)'
            else:
                ex = Exception('WLAN信息获取失败，请检查"HWConfig"中定义信息！！！')
                # 抛出异常对象
                raise ex
            print('获取WLAN信息:', CheckHW['check_info'])

            # 获取KB信息
            if CheckHW['HWConfig']['KB'] == 'YES':
                CheckHW['check_info']['log_name_list'].append('KB.CSV')
                param_list.append(response_info_list['KBPN'])
                CheckHW['check_info']['data_list'].append('kb_info_list')
                KB = response_info_list['KBPN'] + '(KBPN)'
            elif CheckHW['HWConfig']['DOCKPN'] == 'YES':
                CheckHW['check_info']['log_name_list'].append('KB.CSV')
                param_list.append(response_info_list['DOCKPN'])
                CheckHW['check_info']['data_list'].append('kb_info_list')
                KB = response_info_list['DOCKPN'] + '(DOCKPN)'
            else:
                ex = Exception('KB信息获取失败，请检查"HWConfig"中定义信息！！！')
                # 抛出异常对象
                raise ex
            print('获取KB信息:', CheckHW['check_info'])

            # 获取FCAM信息
            if CheckHW['HWConfig']['CAM'] == 'YES':
                CheckHW['check_info']['log_name_list'].append('FCAM.CSV')
                param_list.append(response_info_list['CAMPN'])
                CheckHW['check_info']['data_list'].append('fcam_info_list')
                FCAM = response_info_list['CAMPN'] + '(CAMPN)'
            elif CheckHW['HWConfig']['FCAM'] == 'YES':
                CheckHW['check_info']['log_name_list'].append('FCAM.CSV')
                param_list.append(response_info_list['FCAMPN'])
                CheckHW['check_info']['data_list'].append('fcam_info_list')
                FCAM = response_info_list['FCAMPN'] + '(FCAMPN)'
            else:
                ex = Exception('FCAM信息获取失败，请检查"HWConfig"中定义信息！！！')
                # 抛出异常对象
                raise ex
            print('获取FCAM信息:', CheckHW['check_info'])

            # 获取RCAM信息
            if CheckHW['HWConfig']['RCAM'] == 'SPECIAL':
                CheckHW['check_info']['log_name_list'].append('RCAM.CSV')
                param_list.append(response_info_list['RCAMPN'])
                CheckHW['check_info']['data_list'].append('rcam_info_list')
                RCAM = response_info_list['RCAMPN'] + '(RCAMPN)'
            elif CheckHW['HWConfig']['RCAM'] == 'YES':
                CheckHW['check_info']['log_name_list'].append('RCAM.CSV')
                param_list.append(response_info_list['RCAMPN'])
                CheckHW['check_info']['data_list'].append('rcam_info_list')
                RCAM = response_info_list['RCAMPN'] + '(RCAMPN)'
            elif CheckHW['HWConfig']['RCAM'] == 'NO':
                print('此配置不带后摄,无需获取RCAM信息！！！')
            else:
                ex = Exception('RCAM信息获取失败，请检查"HWConfig"中定义信息！！！')
                # 抛出异常对象
                raise ex
            print('获取RCAM信息:', CheckHW['check_info'])
            print('param_list:', param_list)

            support.write_json(
                data=CheckHW['check_info'],
                path=r'C:\WinTest\JSON\data',
                filename='CheckHW_info.json'
            )

            csv_info_list = support.get_csv_info(
                log_name_list=CheckHW['check_info']['log_name_list'],
                param_list=param_list,
                data_list=CheckHW['check_info']['data_list']
            )
            print('csv_info_list:', csv_info_list)

            support.write_json(
                data=csv_info_list,
                path=r'C:\WinTest\JSON\data',
                filename='HWinfo_mes.json'
            )

            ptd_chk_struct = r'PTDRegRun.exe %s >regist.txt' % response_info_list['ptdcode']
            ptd_chk_item = CheckHW['dictor']['ptd_chk_item']
            ptd_chk_data = CheckHW['dictor']['ptd_chk_data']
            print('ptd_chk_struct:', ptd_chk_struct)
            ptd_res = support.test(
                tool_path=CheckHW['dictor']['tool_path'],
                result_log_name='regist.txt',
                act='find',
                checklist='NO',
                instruct=ptd_chk_struct,
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
            device_chk_struct = CheckHW['dictor']['device_chk_struct']
            device_chk_item = CheckHW['dictor']['device_chk_item']
            device_chk_data = CheckHW['dictor']['device_chk_data']
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
                Errorcode = '设备管理器有黄标，或是工具运行不了，请逐个排查！！！'
                result = 'fail'

            if Errorcode == '.':
                print('CPU类型检查')
                support.del_log(r'C:\WinTest\Tools\CPU.BAT')
                cpu_info = csv_info_list['cpu_info_list']
                # print('cpu_info:', cpu_info)
                cpu_info_list = cpu_info.split(',')  # 用”,“将CPU信息分隔开
                # print('cpu_info_list', cpu_info_list)
                cpu_chk_stract = CheckHW['dictor']['cpu_chk_stract']
                cpu_check_list = CheckHW['dictor']['cpu_check_list']
                cpu_info_uut = support.test(
                    tool_path=CheckHW['dictor']['tool_path'],
                    result_log_name='CPU.BAT',
                    checklist='YES',
                    act='read',
                    instruct=cpu_chk_stract,
                    check_item=cpu_check_list,
                    check_data=''
                )
                # 显卡类型检查
                gpu_chk_stract = CheckHW['dictor']['gpu_chk_stract']
                gpu_check_list = CheckHW['dictor']['gpu_check_list']
                gpu_info_uut = support.test(
                    tool_path=CheckHW['dictor']['tool_path'],
                    result_log_name='GPUinfo.BAT',
                    checklist='YES',
                    act='read',
                    instruct=gpu_chk_stract,
                    check_item=gpu_check_list,
                    check_data=''
                )
                if gpu_info_uut[gpu_check_list[0]] == cpu_info_list[4]:
                    if gpu_info_uut[gpu_check_list[1]] == cpu_info_list[5]:
                        copyfile(
                            src=r'C:\WinTest\Tools\GPUinfo.BAT',
                            dst=r'C:\WinTest\LogFile' + '\\' + 'Check_GPU.log'
                        )
                        print('GPU类型VGADescription检查PASS!!!MES定义VGADescription为:' + cpu_info_list[4] + ',实际组装VGADescription为:' + gpu_info_uut[gpu_check_list[0]])
                        print('GPU类型VGA_RAM检查PASS!!!MES定义VGA_RAM为:' + cpu_info_list[5] + ',实际组装VGA_RAM类型为:' + gpu_info_uut[gpu_check_list[1]])
                    else:
                        code = 'MBCF2'
                        msg1 = 'GPU类型VGA_RAM检查失败!!!MES定义VGA_RAM为:' + cpu_info_list[5] + ',实际组装VGA_RAM类型为:' + gpu_info_uut[gpu_check_list[1]]
                        print(msg1)
                        support.setmsg(
                            Errorcode=code,
                            msg=msg1
                        )
                        ex = Exception(msg1)
                        # 抛出异常对象
                        raise ex
                else:
                    code = 'MBCF2'
                    msg1 = 'GPU类型VGADescription检查失败!!!MES定义VGADescription为:' + cpu_info_list[4] + ',实际组装VGADescription为:' + gpu_info_uut[gpu_check_list[0]]
                    print(msg1)
                    support.setmsg(
                        Errorcode=code,
                        msg=msg1
                    )
                    ex = Exception(msg1)
                    # 抛出异常对象
                    raise ex

                print('gpu_info_uut:', gpu_info_uut)
                print(len(gpu_check_list), gpu_check_list)
                print('cpu_info_uut:', cpu_info_uut)
                print('cpu_info_list', cpu_info_list)
                if cpu_info_uut['CPU_Model'] == cpu_info_list[1]:
                    if cpu_info_uut['CPU_ID'][12:] == cpu_info_list[2]:
                        if cpu_info_uut['CPU_Speed'] == cpu_info_list[3]:
                            print(
                                'CPU类型CPU_Speed检查PASS!!!' + 'MES定义CPU_Speed为:' + cpu_info_list[3] + ',实际组装CPU_Speed为:' + cpu_info_uut['CPU_Speed'])
                            print('CPU类型CPU_ID检查PASS!!!' + 'MES定义CPU_ID为:' + cpu_info_list[2] + ',实际组装CPU_ID类型为:' + cpu_info_uut['CPU_ID'][12:])
                            print('CPU类型CPU_Model检查PASS!!!' + 'MES定义CPU_Model为:' + cpu_info_list[1] + ',实际组装CPU_Model类型为:' + cpu_info_uut['CPU_Model'])
                            copyfile(
                                src=r'C:\WinTest\Tools\CPU.BAT',
                                dst=r'C:\WinTest\LogFile' + '\\' + 'Check_CPU.log'
                            )
                            json_cpu = {
                                'MBPN': cpu_info_list[0],
                                'CPUTYPE': cpu_info_list[1],
                                'CPUID': cpu_info_list[2],
                                'MCCLOK': cpu_info_list[3],
                                'GPUTYPE': cpu_info_list[4],
                                'VRAMSIZE': cpu_info_list[5],
                                'TPM': cpu_info_list[6]
                            }
                            HWConfig['Config_CPU'] = json_cpu

                            print('HWConfig:', HWConfig)
                        else:
                            code = 'MBCF2'
                            msg1 = 'CPU_Speed检查失败,MES定义CPU_Speed为:' + cpu_info_list[3] + ',实际组装CPU_Speed为:' + cpu_info_uut['CPU_Speed']
                            print(msg1)
                            support.setmsg(
                                Errorcode=code,
                                msg=msg1
                            )
                            ex = Exception(msg1)
                            # 抛出异常对象
                            raise ex

                    else:
                        code = 'MBCF2'
                        msg1 = 'CPU_ID检查失败,MES定义CPU_ID为:' + cpu_info_list[2] + ',实际组装CPU_ID类型为:' + cpu_info_uut['CPU_ID'][12:]
                        print(msg1)
                        support.setmsg(
                            Errorcode=code,
                            msg=msg1
                        )
                        ex = Exception(msg1)
                        # 抛出异常对象
                        raise ex
                else:
                    code = 'MBCF2'
                    result = 'fail'
                    msg1 = 'CPU_Model检查失败,MES定义CPU_Model为:' + cpu_info_list[1] + ',实际组装CPU_Model类型为:' + cpu_info_uut['CPU_Model']
                    print(msg1)
                    support.setmsg(
                        Errorcode=code,
                        msg=msg1
                    )
                    ex = Exception(msg1)
                    # 抛出异常对象
                    raise ex

            if Errorcode == '.':
                print('RAM类型检查')
                support.del_log(r'C:\WinTest\Tools\RAM.BAT')
                ram_info = csv_info_list['ram_info_list']
                # print('ram_info:', ram_info)
                ram_info_list = ram_info.split(',')  # 用”,“将RAM信息分隔开
                # print('ram_info_list', ram_info_list)
                ram_chk_stract = CheckHW['dictor']['ram_chk_stract']
                ram_chk_list = CheckHW['dictor']['ram_chk_list']
                ram_info_uut = support.test(
                    tool_path=CheckHW['dictor']['tool_path'],
                    result_log_name='RAM.BAT',
                    act='read',
                    checklist='YES',
                    instruct=ram_chk_stract,
                    check_item=ram_chk_list,
                    check_data=''
                )
                print('ram_info_list', ram_info_list)
                print('ram_info_uut:', ram_info_uut)

                if ram_info_uut['Slot1_Vendor'] == ram_info_list[1]:
                    if ram_info_uut['RAMTotalSize'] == ram_info_list[2]:
                        if ram_info_uut['Slot1_RAMFrequency'] == ram_info_list[3]:
                            print('RAM类型RAMFrequency检查PASS!!!' + 'MES定义RAMFrequency为:' + ram_info_list[3] + ',实际组装RAMFrequency为:' + ram_info_uut['Slot1_RAMFrequency'])
                            print('RAM类型RAMTotalSize检查PASS!!!' + 'MES定义RAMTotalSize为:' + ram_info_list[2] + ',实际组装RAMTotalSize为:' + ram_info_uut['RAMTotalSize'])
                            print('RAM类型厂商检查PASS!!!' + 'MES定义RAM厂商类型为:' + ram_info_list[1] + ',实际组装RAM厂商类型为:' + ram_info_uut['Slot1_Vendor'])
                            copyfile(
                                src=r'C:\WinTest\Tools\RAM.BAT',
                                dst=r'C:\WinTest\LogFile' + '\\' + 'Check_RAM.log'
                            )
                            json_ram = {
                                'MB料号': ram_info_list[0],
                                '内存厂商': ram_info_list[1],
                                '内存容量': ram_info_list[2],
                                '内存频率': ram_info_list[3]
                            }
                            HWConfig['Config_RAM'] = json_ram
                        else:
                            code = 'MBCF3'
                            msg1 = 'RAMFrequency检查失败,MES定义RAMFrequency为:' + ram_info_list[3] + ',实际组装RAMFrequency为:' + ram_info_uut['Slot1_RAMFrequency']
                            print(msg1)
                            support.setmsg(
                                Errorcode=code,
                                msg=msg1
                            )
                            ex = Exception(msg1)
                            # 抛出异常对象
                            raise ex
                    else:
                        code = 'MBCF3'
                        msg1 = 'RAMTotalSize检查失败,MES定义RAMTotalSize为:' + ram_info_list[2] + ',实际组装RAMTotalSize为:' + ram_info_uut['RAMTotalSize']
                        print(msg1)
                        support.setmsg(
                            Errorcode=code,
                            msg=msg1
                        )
                        ex = Exception(msg1)
                        # 抛出异常对象
                        raise ex
                else:
                    code = 'MBCF3'
                    result = 'fail'
                    msg1 = 'RAM厂商类型检查失败,MES定义RAM厂商类型为:' + ram_info_list[1] + ',实际组装RAM厂商类型为:' + ram_info_uut['Slot1_Vendor']
                    print(msg1)
                    support.setmsg(
                        Errorcode=code,
                        msg=msg1
                    )
                    ex = Exception(msg1)
                    # 抛出异常对象
                    raise ex

            if Errorcode == '.':
                print('SSD类型检查')
                support.del_log(r'C:\WinTest\Tools\SSD.BAT')
                ssd_info = csv_info_list['ssd_info_list']
                # print('ssd_info:', ssd_info)
                ssd_info_list = ssd_info.split(',')  # 用”,“将SSD信息分隔开
                # print('ssd_info_list', ssd_info_list)
                ssd_chk_stract = CheckHW['dictor']['ssd_chk_stract']
                ssd_chk_list = CheckHW['dictor']['ssd_chk_list']
                ssd_info_uut = support.test(
                    tool_path=CheckHW['dictor']['tool_path'],
                    result_log_name='SSD.BAT',
                    checklist='YES',
                    act='read',
                    instruct=ssd_chk_stract,
                    check_item=ssd_chk_list,
                    check_data=''
                )
                print('ssd_info_uut:', ssd_info_uut)
                print('ssd_info_list:', ssd_info_list)
                if ssd_info_uut['HDD1_MD'] == ssd_info_list[1]:
                    if ssd_info_uut['HDD1_FW'] == ssd_info_list[3]:
                        if ssd_info_uut['HDD1_SZ'] == ssd_info_list[2]:
                            print('SSD类型HDD1_SZ检查PASS!!!' + 'MES定义HDD1_SZ为:' + ssd_info_list[2] + ',实际组装HDD1_SZ为:' + ssd_info_uut['HDD1_SZ'])
                            print('SSD类型HDD1_FW检查PASS!!!' + 'MES定义HDD1_SZ为:' + ssd_info_list[3] + ',实际组装HDD1_SZ为:' + ssd_info_uut['HDD1_FW'])
                            print('SSD类型HDD1_MD检查PASS!!!' + 'MES定义HDD1_SZ为:' + ssd_info_list[1] + ',实际组装HDD1_SZ为:' + ssd_info_uut['HDD1_MD'])
                            copyfile(
                                src=r'C:\WinTest\Tools\SSD.BAT',
                                dst=r'C:\WinTest\LogFile' + '\\' + 'Check_SSD.log'
                            )
                            json_ssd = {
                                'SSD料号': SSD,
                                'SSD型号': ssd_info_list[1],
                                'SSD容量': ssd_info_list[2],
                                'SSD分位': ssd_info_list[3]
                            }
                            HWConfig['Config_SSD'] = json_ssd
                        else:
                            code = 'MBCF2'
                            msg1 = 'HDD1_SZ检查失败,MES定义HDD1_SZ为:' + ssd_info_list[2] + ',实际组装HDD1_SZ为:' + ssd_info_uut['HDD1_SZ']
                            print(msg1)
                            support.setmsg(
                                Errorcode=code,
                                msg=msg1
                            )
                            ex = Exception(msg1)
                            # 抛出异常对象
                            raise ex
                    else:
                        code = 'MBCF2'
                        msg1 = 'HDD1_FW检查失败,MES定义HDD1_FW为:' + ssd_info_list[3] + ',实际组装CPU_ID类型为:' + ssd_info_uut['HDD1_FW']
                        print(msg1)
                        support.setmsg(
                            Errorcode=code,
                            msg=msg1
                        )
                        ex = Exception(msg1)
                        # 抛出异常对象
                        raise ex
                else:
                    code = 'MBCF2'
                    msg1 = 'HDD1_MD检查失败,MES定义HDD1_MD为:' + ssd_info_list[1] + ',实际组装HDD1_MD类型为:' + ssd_info_uut['HDD1_MD']
                    print(msg1)
                    support.setmsg(
                        Errorcode=code,
                        msg=msg1
                    )
                    ex = Exception(msg1)
                    # 抛出异常对象
                    raise ex

            if Errorcode == '.':
                print('LCD类型检查')
                support.del_log(r'C:\WinTest\Tools\LCD.BAT')
                lcd_info = csv_info_list['lcd_info_list']
                # print('lcd_info:', lcd_info)
                lcd_info_list = lcd_info.split(',')  # 用”,“将LCD信息分隔开
                # print('lcd_info_list', lcd_info_list)
                lcd_chk_stract = CheckHW['dictor']['lcd_chk_stract']
                lcd_chk_list = CheckHW['dictor']['lcd_chk_list']
                lcd_info_uut = support.test(
                    tool_path=CheckHW['dictor']['tool_path'],
                    result_log_name='LCD.BAT',
                    checklist='YES',
                    act='read',
                    instruct=lcd_chk_stract,
                    check_item=lcd_chk_list,
                    check_data=''
                )
                # print("csv_info_list:", csv_info_list)
                print('lcd_info_uut:', lcd_info_uut)
                print('lcd_info_list:', lcd_info_list)
                if lcd_info_uut['LCDID'][8:] == lcd_info_list[2]:
                    print('LCD类型检查PASS!!!' + 'MES定义LCDID为:' + lcd_info_list[2] + ',实际组装LCDID为:' + lcd_info_uut['LCDID'][8:])
                    copyfile(
                        src=r'C:\WinTest\Tools\LCD.BAT',
                        dst=r'C:\WinTest\LogFile' + '\\' + 'Check_LCD.log'
                    )
                    json_lcd = {
                        'LCD料号': LCD,
                        'LCD类型': lcd_info_list[1],
                        'LCD厂商': lcd_info_list[3],
                        'LCDEDID': lcd_info_list[2],
                        'LCDTYPE': lcd_info_list[4]
                    }
                    HWConfig['Config_LCD'] = json_lcd
                else:
                    code = 'MBCF2'
                    msg1 = 'LCD类型检查失败,MES定义LCDID为:' + lcd_info_list[2] + ',实际组装LCDID为:' + lcd_info_uut['LCDID'][8:]
                    print(msg1)
                    support.setmsg(
                        Errorcode=code,
                        msg=msg1
                    )
                    ex = Exception(msg1)
                    # 抛出异常对象
                    raise ex

            if Errorcode == '.':
                print('WLAN&BT类型检查')
                support.del_log(r'C:\WinTest\Tools\WLAN.BAT')
                wlan_info = csv_info_list['wlan_info_list']
                # print('wlan_info:', wlan_info)
                wlan_info_list = wlan_info.split(',')  # 用”,“将WLAN信息分隔开
                print('wlan_info_list', wlan_info_list)
                WLAN_HWID = 'PCI\\VEN_%s&DEV_%s&SUBSYS_%s%s&REV_%s' % (wlan_info_list[3], wlan_info_list[4], wlan_info_list[5], wlan_info_list[6], wlan_info_list[7])
                BT_HWID = 'USB\\VID_%s&PID_%s&REV_%s' % (wlan_info_list[8], wlan_info_list[9], wlan_info_list[10])
                print('WLAN_HWID:', WLAN_HWID)
                print('BT_HWID:', BT_HWID)
                wlan_chk_stract = 'devcon.exe  find /i "PCI*" | find /i "%s" >WLAN.BAT' % WLAN_HWID
                bt_chk_stract = 'devcon.exe  HWIDS "USB\VID*" | find /i "%s" >BT.BAT' % BT_HWID
                wlan_check_list = CheckHW['dictor']['wlan_check_list']
                bt_check_list = CheckHW['dictor']['bt_check_list']
                wlan_info_uut = support.test(
                    tool_path=CheckHW['dictor']['tool_path'],
                    result_log_name='WLAN.BAT',
                    checklist='YES',
                    act='read',
                    instruct=wlan_chk_stract,
                    check_item=wlan_check_list,
                    check_data=''
                )
                bt_info_uut = support.test(
                    tool_path=CheckHW['dictor']['tool_path'],
                    result_log_name='BT.BAT',
                    checklist='YES',
                    act='read',
                    instruct=bt_chk_stract,
                    check_item=bt_check_list,
                    check_data=''
                )
                print('bt_info_uut:', bt_info_uut, 'wlan_info_uut:', wlan_info_uut)
                bt_info_uut = bt_info_uut['USB\\VID']
                wlan_info_uut = wlan_info_uut['PCI'].split(':')[0].split('&')[0] + '&' + wlan_info_uut['PCI'].split(':')[0].split('&')[1] + '&' + wlan_info_uut['PCI'].split(':')[0].split('&')[2] + '&' + wlan_info_uut['PCI'].split(':')[0].split('&')[3].split('\\')[0]
                print('bt_info_uut:', bt_info_uut, 'wlan_info_uut:', wlan_info_uut)
                if WLAN_HWID == wlan_info_uut:
                    print('WLAN类型检查PASS!!!' + 'MES定义WLAN_HWID为:' + WLAN_HWID + ',实际组装WLAN_HWID为:' + wlan_info_uut)
                    copyfile(
                        src=r'C:\WinTest\Tools\WLAN.BAT',
                        dst=r'C:\WinTest\LogFile' + '\\' + 'Check_WLAN.log'
                    )
                    json_wlan = {
                        'WLAN料号': WLAN,
                        'WLAN型号': wlan_info_list[1] + wlan_info_list[2],
                        'WLANID': WLAN_HWID,
                        'BTID': BT_HWID
                    }
                    HWConfig['Config_WLAN'] = json_wlan
                else:
                    code = 'MBCF2'
                    msg1 = 'WLAN类型WLAN_HWID检查失败,MES定义WLAN_HWID为:' + wlan_info_list[2] + ',实际组装WLAN_HWID为:' + wlan_info_uut['LCDID'][8:]
                    print(msg1)
                    support.setmsg(
                        Errorcode=code,
                        msg=msg1
                    )
                    ex = Exception(msg1)
                    # 抛出异常对象
                    raise ex

                if BT_HWID == bt_info_uut:
                    print('BT类型检查PASS!!!' + 'MES定义BT_HWID为:' + BT_HWID + ',实际组装BT_HWID为:' + bt_info_uut)
                    copyfile(
                        src=r'C:\WinTest\Tools\BT.BAT',
                        dst=r'C:\WinTest\LogFile' + '\\' + 'Check_BT.log'
                    )
                else:
                    code = 'MBCF2'
                    msg1 = 'BT类型BT_HWID检查失败,MES定义BT_HWID为:' + BT_HWID + ',实际组装BT_HWID为:' + bt_info_uut
                    print(msg1)
                    support.setmsg(
                        Errorcode=code,
                        msg=msg1
                    )
                    ex = Exception(msg1)
                    # 抛出异常对象
                    raise ex

            if Errorcode == '.':
                print('FCAM类型检查')
                support.del_log(r'C:\WinTest\Tools\FCAM.BAT')
                fcam_info = csv_info_list['fcam_info_list']
                # print('fcam_info:', fcam_info)
                fcam_info_list = fcam_info.split(',')  # 用”,“将FCAM信息分隔开
                print('fcam_info_list', fcam_info_list)
                FCAM_HWID = 'USB\\VID_%s&PID_%s&REV_%s&MI_00' % (fcam_info_list[2], fcam_info_list[3], fcam_info_list[4])
                # print('FCAM_HWID:', FCAM_HWID)
                fcam_chk_stract = 'devcon.exe  HWIDS "USB\\VID*" | find /i "%s" >FCAM.BAT' % FCAM_HWID
                fcam_check_list = CheckHW['dictor']['fcam_check_list']
                fcam_info_uut = support.test(
                    tool_path=CheckHW['dictor']['tool_path'],
                    result_log_name='FCAM.BAT',
                    checklist='YES',
                    act='read',
                    instruct=fcam_chk_stract,
                    check_item=fcam_check_list,
                    check_data=''
                )
                print('fcam_info_uut:', fcam_info_uut)
                fcam_info_uut = fcam_info_uut['USB\\VID']
                print('fcam_info_uut:', fcam_info_uut)
                print('FCAM_HWID:', FCAM_HWID)
                if FCAM_HWID == fcam_info_uut:
                    if CheckHW['HWConfig']['IRCAM'] == 'YES':
                        print('IRCAM类型检查')
                        support.del_log(r'C:\WinTest\Tools\IRCAM.BAT')
                        IRCAM_HWID = 'USB\\VID_%s&PID_%s&REV_%s&MI_02' % (fcam_info_list[2], fcam_info_list[3], fcam_info_list[4])
                        # print('IRCAM_HWID:', IRCAM_HWID)
                        ircam_chk_stract = 'devcon.exe  HWIDS "USB\\VID*" | find /i "%s" >IRCAM.BAT' % IRCAM_HWID
                        ircam_check_list = CheckHW['dictor']['ircam_check_list']
                        ircam_info_uut = support.test(
                            tool_path=CheckHW['dictor']['tool_path'],
                            result_log_name='IRCAM.BAT',
                            checklist='YES',
                            act='read',
                            instruct=ircam_chk_stract,
                            check_item=ircam_check_list,
                            check_data=''
                        )
                        # print('ircam_info_uut:', ircam_info_uut)
                        ircam_info_uut = ircam_info_uut['USB\\VID']
                        # print('ircam_info_uut:', ircam_info_uut)
                        # print('IRCAM_HWID:', IRCAM_HWID)
                        if IRCAM_HWID == ircam_info_uut:
                            print(
                                'IRCAM类型检查PASS!!!' + 'MES定义IRCAM_HWID为:' + IRCAM_HWID + ',实际组装IRCAM_HWID为:' + ircam_info_uut)
                            copyfile(
                                src=r'C:\WinTest\Tools\IRCAM.BAT',
                                dst=r'C:\WinTest\LogFile' + '\\' + 'Check_IRCAM.log'
                            )
                            json_ircam = {
                                'IRCAM料号': FCAM,
                                'IRCAMHWID': IRCAM_HWID
                            }
                            HWConfig['Config_IRCAM'] = json_ircam
                        else:
                            code = 'MBCF2'
                            msg1 = 'IRCAM类型IRCAM_HWID检查失败,MES定义IRCAM_HWID为:' + IRCAM_HWID + ',实际组装IRCAM_HWID为:' + ircam_info_uut
                            print(msg1)
                            support.setmsg(
                                Errorcode=code,
                                msg=msg1
                            )
                            ex = Exception(msg1)
                            # 抛出异常对象
                            raise ex

                    print('FCAM类型检查PASS!!!' + 'MES定义FCAM_HWID为:' + FCAM_HWID + ',实际组装FCAM_HWID为:' + fcam_info_uut)
                    copyfile(
                        src=r'C:\WinTest\Tools\FCAM.BAT',
                        dst=r'C:\WinTest\LogFile' + '\\' + 'Check_FCAM.log'
                    )
                    json_fcam = {
                        'FCAM料号': FCAM,
                        'FCAMHWID': FCAM_HWID
                    }
                    HWConfig['Config_FCAM'] = json_fcam
                else:
                    code = 'MBCF2'
                    msg1 = 'FCAM类型FCAM_HWID检查失败,MES定义FCAM_HWID为:' + FCAM_HWID + ',实际组装FCAM_HWID为:' + fcam_info_uut
                    print(msg1)
                    support.setmsg(
                        Errorcode=code,
                        msg=msg1
                    )
                    ex = Exception(msg1)
                    # 抛出异常对象
                    raise ex

            if Errorcode == '.':
                print('BATT类型检查')
                support.del_log(r'C:\WinTest\FRT\Battery\BATT.BAT')
                batt_info = csv_info_list['batt_info_list']
                print('batt_info:', batt_info)
                batt_info_list = batt_info.split(',')  # 用”,“将BATT信息分隔开
                print('batt_info_list', batt_info_list)
                batt_chk_stract = CheckHW['dictor']['batt_chk_stract']
                batt_chk_list = CheckHW['dictor']['batt_chk_list']
                batt_info_uut = support.test(
                    tool_path=r'C:\WinTest\FRT\Battery',
                    result_log_name='BATT.BAT',
                    checklist='YES',
                    act='read',
                    instruct=batt_chk_stract,
                    check_item=batt_chk_list,
                    check_data=''
                )
                print('batt_info_uut:', batt_info_uut)
                print('batt_info_list:', batt_info_list)
                if batt_info_uut['BatteryDeviceName'] == batt_info_list[2]:
                    if batt_info_uut['BatteryDesignCapacity'] == batt_info_list[3]:
                        print('BATT类型BatteryDesignCapacity检查PASS!!!' + 'MES定义BatteryDesignCapacity为:' + batt_info_list[3] + ',实际组装BatteryDesignCapacity为:' + batt_info_uut['BatteryDesignCapacity'])
                        print('BATT类型BatteryDeviceName检查PASS!!!' + 'MES定义BatteryDeviceName为:' + batt_info_list[2] + ',实际组装BatteryDeviceName为:' + batt_info_uut['BatteryDeviceName'])
                        copyfile(
                            src=r'C:\WinTest\FRT\Battery\BATT.BAT',
                            dst=r'C:\WinTest\LogFile' + '\\' + 'Check_BATT.log'
                        )
                        json_batt = {
                            'BATT料号': batt_info_list[0],
                            'BattName': batt_info_list[2],
                            'DesignCap': batt_info_list[3]
                        }
                        HWConfig['Config_BATT'] = json_batt
                    else:
                        code = 'MBCF2'
                        msg1 = 'BatteryDesignCapacity检查失败,MES定义BatteryDesignCapacity为:' + batt_info_list[3] + ',实际组装BatteryDesignCapacity为:' + batt_info_uut['BatteryDesignCapacity']
                        print(msg1)
                        support.setmsg(
                            Errorcode=code,
                            msg=msg1
                        )
                        ex = Exception(msg1)
                        # 抛出异常对象
                        raise ex
                else:
                    code = 'MBCF2'
                    msg1 = 'BatteryDeviceName检查失败,MES定义BatteryDeviceName为:' + batt_info_list[2] + ',实际组装BatteryDeviceName为:' + batt_info_uut['BatteryDeviceName']
                    print(msg1)
                    support.setmsg(
                        Errorcode=code,
                        msg=msg1
                    )
                    ex = Exception(msg1)
                    # 抛出异常对象
                    raise ex

            if Errorcode == '.':
                print('TPD类型检查')
                if CheckHW['HWConfig']['DOCKPN'] == 'YES':
                    support.del_log(r'C:\WinTest\LogFile\Check_TPD.log')
                    msg = '此类机型下半身类型为DUCKN,无需TPD类型检查!!!'
                    print(msg)
                    support.writr_log(
                        path=r'C:\WinTest\LogFile\Check_TPD.log',
                        date='此类机型下半身类型为DUCKN,无需TPD类型检查!!!',
                        act='w'
                    )
                elif CheckHW['HWConfig']['TPFW'] == 'YES':
                    print('haha')
                    tpd_info = csv_info_list['tpd_info_list']
                    print('tpd_info:', tpd_info)
                    tpd_info_list = tpd_info.split(',')  # 用”,“将TPD信息分隔开
                    print('tpd_info_list:', tpd_info_list)
                    if tpd_info_list[1] == 'Synaptics':
                        support.del_log(r'C:\WinTest\Tools\FWversion.txt')
                        TPD_FW = 'FW Version: %s' % tpd_info_list[2]
                        print('TPD_FW:', TPD_FW)
                        tpd_chk_stract_Synaptics = CheckHW['dictor']['tpd_chk_stract_Synaptics']
                        tpd_chk_list_Synaptics = CheckHW['dictor']['tpd_chk_list_Synaptics']
                        tpd_info_uut = support.test(
                            tool_path=CheckHW['dictor']['tool_path'],
                            result_log_name='FWversion.txt',
                            checklist='YES',
                            act='read',
                            instruct=tpd_chk_stract_Synaptics,
                            check_item=tpd_chk_list_Synaptics,
                            check_data=''
                        )
                        print('tpd_info_uut:', tpd_info_uut)
                        if tpd_info_uut['FW'] == TPD_FW:
                            print('TPD类型检查PASS!!!MES定义TPD_FW为:' + TPD_FW + ',实际组装TPD_FW为:' + tpd_info_uut['FW'])
                            copyfile(
                                src=r'C:\WinTest\Tools\FWversion.txt',
                                dst=r'C:\WinTest\LogFile' + '\\' + 'Check_TPD.log'
                            )
                            json_tpd = {
                                'TPD料号': tpd_info_list[0],
                                'TPDVendor': tpd_info_list[1],
                                'TPDFW': tpd_info_list[2],
                                'TPDTYPE': tpd_info_list[3]
                            }
                            HWConfig['Config_TPD'] = json_tpd

                        else:
                            code = 'MBCF2'
                            msg1 = 'TPD类型检查失败!!!MES定义TPD_FW为:' + TPD_FW + ',实际组装TPD_FW为:' + tpd_info_uut['FW']
                            print(msg1)
                            support.setmsg(
                                Errorcode=code,
                                msg=msg1
                            )
                            ex = Exception(msg1)
                            # 抛出异常对象
                            raise ex

                    elif tpd_info_list[1] == 'ELAN':
                        support.del_log(r'C:\WinTest\Tools\ElanFWVerReader.log')
                        TPD_FW = tpd_info_list[2]
                        print('TPD_FW:', TPD_FW)
                        tpd_chk_stract_Elan = CheckHW['dictor']['tpd_chk_stract_Elan']
                        tpd_chk_list_Elan = CheckHW['dictor']['tpd_chk_list_Elan']
                        tpd_info_uut = support.test(
                            tool_path=CheckHW['dictor']['tool_path'],
                            result_log_name='ElanFWVerReader.log',
                            checklist='YES',
                            act='read',
                            instruct=tpd_chk_stract_Elan,
                            check_item=tpd_chk_list_Elan,
                            check_data=''
                        )
                        print('tpd_info_uut:', tpd_info_uut)
                        if tpd_info_uut['0x'] == TPD_FW:
                            print('TPD类型检查PASS!!!MES定义TPD_FW为:' + TPD_FW + ',实际组装TPD_FW为:' + tpd_info_uut['0x'])
                            copyfile(
                                src=r'C:\WinTest\Tools\ElanFWVerReader.log',
                                dst=r'C:\WinTest\LogFile' + '\\' + 'Check_TPD.log'
                            )
                            json_tpd = {
                                'TPD料号': tpd_info_list[0],
                                'TPDVendor': tpd_info_list[1],
                                'TPDFW': tpd_info_list[2],
                                'TPDTYPE': tpd_info_list[3]
                            }
                            HWConfig['Config_TPD'] = json_tpd
                        else:
                            code = 'MBCF2'
                            msg1 = 'TPD类型检查失败!!!MES定义TPD_FW为:' + TPD_FW + ',实际组装TPD_FW为:' + tpd_info_uut['0x']
                            print(msg1)
                            support.setmsg(
                                Errorcode=code,
                                msg=msg1
                            )
                            ex = Exception(msg1)
                            # 抛出异常对象
                            raise ex

                    else:
                        code = 'MBCF2'
                        msg1 = 'TPD厂商信息获取失败!!!'
                        print(msg1)
                        support.setmsg(
                            Errorcode=code,
                            msg=msg1
                        )
                        ex = Exception(msg1)
                        # 抛出异常对象
                        raise ex

                else:
                    ex = Exception('TPD类型信息获取失败，请检查CheckHW.json中的TPD配置信息！！！')
                    # 抛出异常对象
                    raise ex

            if Errorcode == '.':
                print('KB类型检查')
                support.del_log(r'C:\WinTest\LogFile\Check_KB.log')
                if CheckHW['HWConfig']['DOCKPN'] == 'YES':
                    msg = '此类机型下半身类型为DUCKN,无需KB类型检查!!!'
                    print(msg)
                    support.writr_log(
                        path=r'C:\WinTest\LogFile\Check_KB.log',
                        date='此类机型下半身类型为DUCKN,无需KB类型检查!!!',
                        act='w'
                    )
                    json_kb = {
                        'KBTYPE': 'DOCKPN'
                    }
                    HWConfig['Config_KB'] = json_kb
                    result = 'pass'
                elif CheckHW['HWConfig']['KB'] == 'YES':
                    print('haha')
                    kb_info = csv_info_list['kb_info_list']
                    print('kb_info:', kb_info)
                    kb_info_list = kb_info.split(',')  # 用”,“将TPD信息分隔开
                    print('kb_info_list:', kb_info_list)
                    support.writr_log(
                        path=r'C:\WinTest\LogFile\Check_KB.log',
                        date='set KB_TYPE=%s' % kb_info_list[1],
                        act='w'
                    )
                    json_kb = {
                        'KB料号': kb_info_list[0],
                        'KBTYPE': kb_info_list[1],
                        'KBID': kb_info_list[2]
                    }
                    HWConfig['Config_KB'] = json_kb
                    result = 'pass'

                else:
                    ex = Exception('KB类型信息获取失败，请检查CheckHW.json中的KB配置信息！！！')
                    # 抛出异常对象
                    raise ex

            support.write_json(
                data=HWConfig,
                path=r'c:\WinTest\LogFile',
                filename='HWConfig.json'
            )

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
