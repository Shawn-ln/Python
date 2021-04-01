# Coding by LiXiao
# Datatime:3/8/2021 3:25 PM
# Filename:CheckHW.py
# Toolby: PyCharm
import os
from shutil import copyfile
import support

# 开头模板信息
dictor = {
    'FailRetry': '0',
    'FailRetrytimes': '1',
    'UPLIMIT': '9999.900',
    'LOWLIMIT': '-9999.900',
    'RUNITEM': 'CheckHW',
    'instruct': 'BlueTooth.exe',
    'Errorcode': 'HT942',
    'tool_path': r'C:\WinTest\Tools',
    'result_log_name': 'bluetooth.log'
}

HWConfig = {
    'CPUES': 'AMD',
    'ODD': '',
    'CPU': 'OnBoard',
    'GPU': '',
    'RAM': 'OnBoard',
    'LCD': '',
    'LCM': '',
    'SSD': '',
    'CAM': 'YES',
    'FCAM': '',
    'RCAM': 'NO',
    'KB': '',
    'KBLT': '',
    'WLAN': 'OnBoard',
    'BT': 'OnBoard',
    'LTE': '',
    'FP': '',
    'TPFW': '',
    'PDFW': '',
    'TBTFW': '',
    'HDDC1': '1',
    'HDDC2': '2'
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
    MB_SN = support.getSN()

    # 判断是否有测试pass的log记录
    if support.passlog(dictor['RUNITEM']):
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
            # 测试内容和结果
            get_response_info_list = ('ptdcode', 'mbpn', 'oa3keyid', 'mt', 'ln', 'KB_PN')
            get_response_info_data = ('SET ToolAuthenticationCodeByPSN=', 'SET MBPN=', 'SET ProductkeyID=', 'SET Cust_PN_1=', 'SET SN=', 'SET KBPN=')

            Errorcode = '.'
            print('测试工具注册')
            ptdcode = support.get_response_info(param='ToolAuthenticationCodeByPSN')
            if ptdcode is None:
                ex = Exception('工具注册码获取失败！！！')
                # 抛出异常对象
                raise ex
            struct = 'PTDRegRun.exe %s >regist.txt' % ptdcode
            print(struct)
            ptd_res = support.test(
                tool_path=dictor['tool_path'],
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
                tool_path=dictor['tool_path'],
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
                mbpn = support.get_response_info(
                    param='MBPN'
                )
                print('mbpn', mbpn)
                cpu_info = support.get_csv_info(
                    log_name='CPU.CSV',
                    param=mbpn
                )
                print('cpu_info:', cpu_info)
                cpu_info_list = cpu_info.split(',')  # 用”,“将CPU信息分隔开
                print('cpu_info_list', cpu_info_list)
                cpu_chk_stract = 'PC_CPU.exe /set >CPU.BAT'
                check_list = ['CPU_Model', 'CPU_ID', 'CPU_Speed']
                cpu_info_uut = support.test(
                    tool_path=dictor['tool_path'],
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
                    tool_path=dictor['tool_path'],
                    result_log_name='RAM.BAT',
                    act='read',
                    checklist='NO',
                    instruct=ram_chk_stract,
                    check_item='RAMTotalSize',
                    check_data=''
                )
                ram_vender = support.test(
                    tool_path=dictor['tool_path'],
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
                        FailRetry=dictor['FailRetry'],
                        FailRetrytimes=dictor['FailRetrytimes']
                ):
                    dictor['FailRetry'] = str(int(dictor['FailRetry']) + 1)
                    print('测试循环次数：' + dictor['FailRetry'], '，测试结果：fail！！！')
                    continue

                # CreateResult
                support.creatResult(
                    Fixed=currentPath,
                    ItemName=dictor['RUNITEM'],
                    Result=-1,
                    ItemTag=0
                )
                # SetInfo
                support.setinfo(
                    RUNITEM=dictor['RUNITEM'],
                    SN=MB_SN,
                    Result='F',
                    NUM='0',
                    LOGINFO=dictor['RUNITEM'] + ' Fail',
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
                    ItemName=dictor['RUNITEM'],
                    Result=1,
                    ItemTag=0
                )
                # SetInfo
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
    print('SN匹配信息错误，请检查正则表达式！！！')

except Exception as e:
    print(e)
