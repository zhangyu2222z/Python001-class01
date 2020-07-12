# pmap.py -n 4 -f ping -ip 192.168.0.1-192.168.0.100
# pmap.py -n 10 -f tcp -ip 192.168.0.1 -w result.json

import time
import sys
import os
import argparse
import socket
import multiprocessing
from multiprocessing.pool import Pool
from concurrent.futures import ThreadPoolExecutor
import datetime

# 调用本地系统(windows10)执行ping命令
def cmdPing(ipAddr, filePath):
    info = os.system(f'ping {ipAddr} -n 1')
    if 0 == info:
        with open(filePath, mode='a', encoding='UTF-8') as op:
            status = f'{ipAddr} 可连接\n'
            print(status)
            op.write(status)

# 执行tcp链接
def cmdTcp(portAddr, filePath):
    socket.setdefaulttimeout(5)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    info = s.connect_ex(portAddr)
    if 0 == info:
        with open(filePath, mode='a', encoding='UTF-8') as op:
            status = f'{portAddr} 可连接\n'
            print(status)
            op.write(status)
    s.close()

if __name__ == '__main__':
    try:
        start = datetime.datetime.now()
        # 构建py文件执行时的传入参数格式
        prase = argparse.ArgumentParser()
        cpuCount = multiprocessing.cpu_count()
        prase.add_argument('-n', dest='concurrentNum', default=str(cpuCount), type=str, help='并发数')
        prase.add_argument('-f', dest='commandType', default='ping', type=str, help='命令类型，ping或者tcp')
        prase.add_argument('-ip', dest='ipList', default='', type=str, help='ip列表 192.168.0.1-192.168.0.100')
        prase.add_argument('-w', dest='filePath', default='result.json', type=str, help='保存文件，如XXX.json')
        prase.add_argument('-m', dest='model', default='thread', type=str, help='并发模式，proc：多进程模式，thread：多线程模式')
        prase.add_argument('-v', default=False, dest='showTime', action='store_true')
        args = prase.parse_args()
        # 解析传入参数
        showTime = args.showTime
        if args.concurrentNum.isdigit():
            concurrentNum = int(args.concurrentNum)
        else:
            concurrentNum = 4
        commandType = args.commandType
        ipListStr = args.ipList
        ipList = ipListStr.split('-')
        ipAddrList = []
        if len(ipList) > 2:
            raise Exception('ip格式错误')
        if len(ipList) == 1:
            ipAddrList.append(ipList[0])
        else:
            prevIp = ipList[0].strip()
            nextIp = ipList[1].strip()
            minAddr = prevIp[prevIp.rfind('.')+1:].strip()
            maxAddr = nextIp[nextIp.rfind('.')+1:].strip()
            if prevIp[0:prevIp.rfind('.')] != nextIp[0:nextIp.rfind('.')]:
                raise Exception('ip格式错误')
            if int(minAddr) > int(maxAddr):
                raise Exception('起始ip和结束ip位置错误')
            mainAddr = prevIp[0:prevIp.rfind('.')+1]
            ipLength = (int(maxAddr) - int(minAddr))
            for i in range(ipLength+1):
                ipAddrList.append(mainAddr + str(int(minAddr) + i))
        filePath = args.filePath
        model = args.model
        # 多线程形式运行
        if model == 'thread':
            if concurrentNum <= 0:
                concurrentNum = 4
            if 'ping' == commandType:
                # 线程池 最大并发为传入参数值
                with ThreadPoolExecutor(max_workers=concurrentNum) as t:
                    for i in range(len(ipAddrList)):
                        t.submit(cmdPing, ipAddrList[i], filePath)
            else:
                with ThreadPoolExecutor(max_workers=concurrentNum) as t:
                    # 遍历ip地址列表
                    for i in range(len(ipAddrList)):
                        ipAddrStr = ipAddrList[i]
                        # 遍历每个ip的65535个端口
                        for i in range(65535):
                            t.submit(cmdTcp, (ipAddrStr, i), filePath)
        else:# 多进程形式运行
            if 'ping' == commandType:
                if cpuCount < concurrentNum:
                    concurrentNum = cpuCount
                # 进程池 最大并发为传入参数值
                p = Pool(concurrentNum)
                for i in range(len(ipAddrList)):
                    ipAddrStr = ipAddrList[i]
                    p.apply_async(cmdPing, args=(ipAddrStr, filePath,))
                p.close()
                p.join()
                p.terminate()
            else:
                if cpuCount < concurrentNum:
                    concurrentNum = cpuCount
                p = Pool(concurrentNum)
                for i in range(len(ipAddrList)):
                    ipAddrStr = ipAddrList[i]
                    for i in range(65535):
                        p.apply_async(cmdTcp, args=((ipAddrStr, i), filePath,))
                p.close()
                p.join()
                p.terminate()
        end = datetime.datetime.now()
        if showTime:
            runTime = end - start
            print(f'====================运行结束，消耗时间：{runTime}===================')
        print('输入exit退出：')
        while True:
            msg = input()
            if msg == 'exit':
                break
    except Exception as e:
        print(e)
        print('网络异常！')
