#!/usr/bin/python3
# encoding: utf-8
#在运行该程序前注意是否已经修改串口映射关系，让 ttyAMA0 映射到了引出的 GPIO Tx Rx 上
#串口舵机接扩展板上任意一个串行总线接口即可


import serial
import pigpio
import time
import os
open_io="sudo pigpiod"
os.system(open_io)
time.sleep(1)
pi = pigpio.pi()  # 初始化 pigpio库
serialHandle = serial.Serial("/dev/ttyAMA0", 115200)  # 初始化串口， 波特率为115200

def portWrite():  # 配置单线串口为输出
    pi.write(27, 1)  # 拉高TX_CON 即 GPIO27
    pi.write(17, 0)  # 拉低RX_CON 即 GPIO17
    time.sleep(0.1)
    
def checksum(buf):# 计算校验和
    sum = 0x00
    for b in buf:  # 求和
        sum += b
    sum = sum - 0x55 - 0x55  # 去掉命令开头的两个 0x55
    sum = ~sum  # 取反
    return sum & 0xff

def serial_serro_wirte_cmd(id=None, w_cmd=None, dat1=None, dat2=None):#向舵机发送指令
    '''
    写指令
    :param id:
    :param w_cmd:
    :param dat1:
    :param dat2:
    :return:
    '''
    portWrite()
    buf = bytearray(b'\x55\x55')  # 帧头
    buf.append(id)
    # 指令长度
    if dat1 is None and dat2 is None:
        buf.append(3)
    elif dat1 is not None and dat2 is None:
        buf.append(4)
    elif dat1 is not None and dat2 is not None:
        buf.append(7)

    buf.append(w_cmd)  # 指令
    # 写数据
    if dat1 is None and dat2 is None:
        pass
    elif dat1 is not None and dat2 is None:
        buf.append(dat1 & 0xff)  # 偏差
    elif dat1 is not None and dat2 is not None:
        buf.extend([(0xff & dat1), (0xff & (dat1 >> 8))])  # 分低8位 高8位 放入缓存
        buf.extend([(0xff & dat2), (0xff & (dat2 >> 8))])  # 分低8位 高8位 放入缓存
        # 校验和
    buf.append(checksum(buf))
    # for i in buf:
    #     print('%x' %i)
    serialHandle.write(buf)  # 发送
    
if __name__ == '__main__':
    ID=1#舵机ID号
    position1=700#转动到指定位置
    position2=300
    runtime=500#舵机转动的时间
    while True:
        serial_serro_wirte_cmd(ID,1,position1,runtime)
        time.sleep(1)
        serial_serro_wirte_cmd(ID,1,position2,runtime)
        time.sleep(1)
