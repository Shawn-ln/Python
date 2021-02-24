import support

# 开头模板信息
dict = {
    'FailRetry':'0',
    'FailRetrytimes':'10',
    'UPLIMIT':'9999.900',
    'LOWLIMIT':'-9999.900',
    'RUNITEM':'UpdatePatch',
}

support.titles(dict['RUNITEM'])
for i in dict:
    print(i + ' : ' + dict[i])

# 测试正文
for n in range(1, 200):
    # 测试内容和结果
    print('\033[32;0m测试正文')
    if dict['FailRetry'] == '5':
        result = 'pass'
    else:
        result = 'fail'

    # 判断测试结果
    if result == 'fail':
        if support.judge(FailRetry=dict['FailRetry'], FailRetrytimes=dict['FailRetrytimes']):
            dict['FailRetry'] = str(int(dict['FailRetry']) + 1)
            print('测试循环次数：' + dict['FailRetry'], '，测试结果：fail！！！')
            continue
        print('测试fail')
        break

    if result == 'pass':
        print('测试循环次数:', n ,'，测试结果：pass！！！')
        break
