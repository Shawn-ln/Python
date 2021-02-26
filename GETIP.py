# Coding by LiXiao
# Datatime:2/26/2021 5:03 PM
# Filename:GETIP.py
# Toolby: PyCharm
import os


def getIP():
    os.chdir(r'C:\WinTest\Tools')
    instruct1 = r'net use /del * /y'
    os.system(instruct1)
    instruct2 = r'netsh wlan delete profile *'
    os.system(instruct2)
    instruct3 = r'wlanconnect.exe -disconnect'
    os.system(instruct3)