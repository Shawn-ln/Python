# Coding by LiXiao
# Datatime:4/26/2021 4:21 PM
# Filename:FanTest.py
# Toolby: PyCharm

import os
import time
import support

"""
# 开头模板信息
dictor = {
    'FailRetry': '0',
    'FailRetrytimes': '0',
    'UPLIMIT': '9999.900',
    'LOWLIMIT': '-9999.900',
    'RUNITEM': 'FanTest',
    'Errorcode': 'MBCF4',
    'tool_path': r'C:\WinTest\FFT\Fan',
    'check_item_fan1': ['Fan1 Debug Speed Set Successful', 'Fan1 Speed Test PASS! Min:'],
    'check_item_fan2': ['Fan2 Debug Speed Set Successful', 'Fan2 Speed Test PASS! Min:'],
    'result_log_name': 'FanTest.log',
    'waittime': [20, 25, 30],
    'instruct': {
        'low': 3000,
        'mid': 4300,
        'high': 5700,
        'exit': r'FAN.EXE -E'
    }
}
support.write_json(
    data=dictor,
    path=r'C:\WinTest\JSON\data',
    filename='FanTest.json'
)
"""

dictor = support.read_json(
    path=r'C:\WinTest\JSON\data',
    filename='FanTest.json'
)
print('dictor:', dictor)

try:
    fan2 = support.get_ini_info(
        param='SET FAN2'
    )
    print('fan2:', fan2)
    # 测试开始时间
    StartTime = support.titles(
        RUNITEM=dictor['RUNITEM'],
        stage='start'
    )

    # 脚本路径
    currentPath = os.getcwd()
    # currentPath = r'C:\WinTest\Work'
    # print(currentPath)

    # 读取主板写入的mbsn
    MB_SN = support.getSN()

    # 测试正文
    for n in range(1, 200):
        # 测试内容和结果

        print('FAN1低速测试')
        fan1_low = support.test(
            tool_path=dictor['tool_path'],
            act='find',
            checklist='NO',
            result_log_name=dictor['result_log_name'],
            check_item=dictor['check_item_fan1'][0],
            instruct='FAN.EXE -A %s' % dictor['instruct']['low'],
            check_data=''
        )
        print('fan1_low:', fan1_low)
        time.sleep(dictor['waittime'][0])
        fan1_speed = support.test(
            tool_path=dictor['tool_path'],
            act='find',
            checklist='NO',
            result_log_name=dictor['result_log_name'],
            check_item=dictor['check_item_fan1'][1] + '%sMax:%s' % (dictor['instruct']['low']-500, dictor['instruct']['low']+500),
            instruct='FAN.EXE -B %s %s' % (dictor['instruct']['low']-500, dictor['instruct']['low']+500),
            check_data=''
        )
        print('fan1_speed:', fan1_speed)
        if fan1_speed:
            print('FAN1低速测试pass')
            support.save_jsondata(
                save_name=r'C:\WinTest\Jsondata\JSONDATA.BAT',
                get_param=r'Fan1Speed    :',
                save_param='\nSET CPULOWACTUALSPEED=',
                get_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                splits=[':', '['],
                take_numbers=[1, 0]
            )
            support.copy_log(
                source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                act='w'
            )
        else:
            print('FAN1低速测试fail')
            support.copy_log(
                source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                target_path=r'C:\WinTest\LogFile\FAIL_%s.log' % dictor['RUNITEM'],
                act='w'
            )
            ex = Exception('FAN1低速测试fail！！！')
            # 抛出异常对象
            raise ex
        if fan2 == 'YES':
            fan2_low = support.test(
                tool_path=dictor['tool_path'],
                act='find',
                checklist='NO',
                result_log_name=dictor['result_log_name'],
                check_item=dictor['check_item_fan2'][0],
                instruct='FAN.EXE -A %s' % dictor['instruct']['low'],
                check_data=''
            )
            time.sleep(dictor['waittime'][0])
            fan2_speed = support.test(
                tool_path=dictor['tool_path'],
                act='find',
                checklist='NO',
                result_log_name=dictor['result_log_name'],
                check_item=dictor['check_item_fan2'][1] + '%sMax:%s' % (dictor['instruct']['low'] - 500, dictor['instruct']['low'] + 500),
                instruct='FAN.EXE -B %s %s' % (dictor['instruct']['low'] - 500, dictor['instruct']['low'] + 500),
                check_data=''
            )
            print('fan2_speed:', fan2_speed)
            if fan2_speed:
                support.save_jsondata(
                    save_name=r'C:\WinTest\Jsondata\JSONDATA.BAT',
                    get_param=r'Fan2Speed    :',
                    save_param='\nSET GPULOWACTUALSPEED=',
                    get_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                    splits=[':', '['],
                    take_numbers=[1, 0]
                )
                support.copy_log(
                    source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                    target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                    act='a'
                )
            else:
                print('FAN2低速测试fail')
                support.copy_log(
                    source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                    target_path=r'C:\WinTest\LogFile\FAIL_%s.log' % dictor['RUNITEM'],
                    act='a'
                )
                ex = Exception('FAN2低速测试fail！！！')
                # 抛出异常对象
                raise ex
        else:
            fan2_low = 0
            print('此配置不带FAN2，无需进行FAN2转速测试!!!')

        print('FAN1中速测试')
        fan1_mid = support.test(
            tool_path=dictor['tool_path'],
            act='find',
            checklist='NO',
            result_log_name=dictor['result_log_name'],
            check_item=dictor['check_item_fan1'][0],
            instruct='FAN.EXE -A %s' % dictor['instruct']['mid'],
            check_data=''
        )
        print('fan1_mid:', fan1_mid)
        time.sleep(dictor['waittime'][1])
        fan1_speed = support.test(
            tool_path=dictor['tool_path'],
            act='find',
            checklist='NO',
            result_log_name=dictor['result_log_name'],
            check_item=dictor['check_item_fan1'][1] + '%sMax:%s' % (
            dictor['instruct']['mid'] - 500, dictor['instruct']['mid'] + 500),
            instruct='FAN.EXE -B %s %s' % (dictor['instruct']['mid'] - 500, dictor['instruct']['mid'] + 500),
            check_data=''
        )
        print('fan1_speed:', fan1_speed)
        if fan1_speed:
            print('FAN1中速测试pass')
            support.copy_log(
                source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                act='a'
            )
        else:
            print('FAN1中速测试fail')
            support.copy_log(
                source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                target_path=r'C:\WinTest\LogFile\FAIL_%s.log' % dictor['RUNITEM'],
                act='a'
            )
            ex = Exception('FAN1中速测试fail！！！')
            # 抛出异常对象
            raise ex
        if fan2 == 'YES':
            fan2_mid = support.test(
                tool_path=dictor['tool_path'],
                act='find',
                checklist='NO',
                result_log_name=dictor['result_log_name'],
                check_item=dictor['check_item_fan2'][0],
                instruct='FAN.EXE -A %s' % dictor['instruct']['mid'],
                check_data=''
            )
            print('fan2_mid:', fan2_mid)
            time.sleep(dictor['waittime'][1])
            fan2_speed = support.test(
                tool_path=dictor['tool_path'],
                act='find',
                checklist='NO',
                result_log_name=dictor['result_log_name'],
                check_item=dictor['check_item_fan2'][1] + '%sMax:%s' % (
                dictor['instruct']['mid'] - 500, dictor['instruct']['mid'] + 500),
                instruct='FAN.EXE -B %s %s' % (dictor['instruct']['mid'] - 500, dictor['instruct']['mid'] + 500),
                check_data=''
            )
            print('fan2_speed:', fan2_speed)
            if fan2_speed:
                support.copy_log(
                    source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                    target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                    act='a'
                )
            else:
                print('FAN2中速测试fail')
                support.copy_log(
                    source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                    target_path=r'C:\WinTest\LogFile\FAIL_%s.log' % dictor['RUNITEM'],
                    act='a'
                )
                ex = Exception('FAN2中速测试fail！！！')
                # 抛出异常对象
                raise ex
        else:
            fan2_low = 0
            print('此配置不带FAN2，无需进行FAN2转速测试!!!')

        print('FAN1高速测试')
        fan1_high = support.test(
            tool_path=dictor['tool_path'],
            act='find',
            checklist='NO',
            result_log_name=dictor['result_log_name'],
            check_item=dictor['check_item_fan1'][0],
            instruct='FAN.EXE -A %s' % dictor['instruct']['high'],
            check_data=''
        )
        print('fan1_high:', fan1_high)
        time.sleep(dictor['waittime'][2])
        fan1_speed = support.test(
            tool_path=dictor['tool_path'],
            act='find',
            checklist='NO',
            result_log_name=dictor['result_log_name'],
            check_item=dictor['check_item_fan1'][1] + '%sMax:%s' % (
            dictor['instruct']['high'] - 500, dictor['instruct']['high'] + 500),
            instruct='FAN.EXE -B %s %s' % (dictor['instruct']['high'] - 500, dictor['instruct']['high'] + 500),
            check_data=''
        )
        print('fan1_speed:', fan1_speed)
        if fan1_speed:
            print('FAN1高速测试pass')
            support.save_jsondata(
                save_name=r'C:\WinTest\Jsondata\JSONDATA.BAT',
                get_param=r'Fan1Speed    :',
                save_param='\nSET CPULOWACTUALSPEED=',
                get_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                splits=[':', '['],
                take_numbers=[1, 0]
            )
            support.copy_log(
                source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                act='a'
            )
        else:
            print('FAN1高速测试fail')
            support.copy_log(
                source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                target_path=r'C:\WinTest\LogFile\FAIL_%s.log' % dictor['RUNITEM'],
                act='a'
            )
            ex = Exception('FAN1高速测试fail！！！')
            # 抛出异常对象
            raise ex
        if fan2 == 'YES':
            fan2_high = support.test(
                tool_path=dictor['tool_path'],
                act='find',
                checklist='NO',
                result_log_name=dictor['result_log_name'],
                check_item=dictor['check_item_fan2'][0],
                instruct='FAN.EXE -A %s' % dictor['instruct']['high'],
                check_data=''
            )
            print('fan2_high:', fan2_high)
            time.sleep(dictor['waittime'][2])
            fan2_speed = support.test(
                tool_path=dictor['tool_path'],
                act='find',
                checklist='NO',
                result_log_name=dictor['result_log_name'],
                check_item=dictor['check_item_fan2'][1] + '%sMax:%s' % (
                dictor['instruct']['high'] - 500, dictor['instruct']['high'] + 500),
                instruct='FAN.EXE -B %s %s' % (dictor['instruct']['high'] - 500, dictor['instruct']['high'] + 500),
                check_data=''
            )
            print('fan2_speed:', fan2_speed)
            if fan2_speed:
                support.save_jsondata(
                    save_name=r'C:\WinTest\Jsondata\JSONDATA.BAT',
                    get_param=r'Fan2Speed    :',
                    save_param='\nSET GPULOWACTUALSPEED=',
                    get_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                    splits=[':', '['],
                    take_numbers=[1, 0]
                )
                support.copy_log(
                    source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                    target_path=r'C:\WinTest\LogFile\%s.log' % dictor['RUNITEM'],
                    act='a'
                )
            else:
                print('FAN2高速测试fail')
                support.copy_log(
                    source_path=r'%s\%s' % (dictor['tool_path'], dictor['result_log_name']),
                    target_path=r'C:\WinTest\LogFile\FAIL_%s.log' % dictor['RUNITEM'],
                    act='a'
                )
                ex = Exception('FAN2高速测试fail！！！')
                # 抛出异常对象
                raise ex
        else:
            fan2_low = 0
            print('此配置不带FAN2，无需进行FAN2转速测试!!!')

        if support.test(
            tool_path=dictor['tool_path'],
            act='find',
            checklist='NO',
            result_log_name=dictor['result_log_name'],
            check_item=r'Exit FAN Test Mode Successful',
            instruct=dictor['instruct']['exit'],
            check_data=''
        ):
            result = 'pass'
        else:
            result = 'fail'

        os.system(r'%s\%s' % (dictor['tool_path'], dictor['instruct']['exit']))

        # 判断测试结果
        if result == 'fail':
            os.system(r'%s\%s' % (dictor['tool_path'], dictor['instruct']['exit']))
            if support.judge(FailRetry=dictor['FailRetry'], FailRetrytimes=dictor['FailRetrytimes']):
                dictor['FailRetry'] = str(int(dictor['FailRetry']) + 1)
                print('测试循环次数：' + dictor['FailRetry'], '，测试结果：fail！！！')
                continue

            # creatResult
            support.creatResult(
                Fixed=r'%~dp0',
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
            # support.message(
            #     Code=dictor['Errorcode']
            # )
            break

        elif result == 'pass':
            os.system(r'%s\%s' % (dictor['tool_path'], dictor['instruct']['exit']))
            # os.system(r'call \WinTest\tools\FileLog.cmd \WinTest\LogFile\%s.log' % dictor['RUNITEM'])
            support.FileLog(item=dictor['RUNITEM'])
            print('测试循环次数:', n, '，测试结果：pass！！！')
            print('测试SN:', MB_SN)
            # creatResult
            support.creatResult(
                Fixed=r'%~dp0',
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
    os.system(r'%s\%s' % (dictor['tool_path'], dictor['instruct']['exit']))
    print("SN匹配信息错误，请检查正则表达式！！！")
    print(e)
    support.message_showinfo('ERROR', e)

except Exception as e:
    os.system(r'%s\%s' % (dictor['tool_path'], dictor['instruct']['exit']))
    print(e)
    support.message_showinfo('ERROR', e)
