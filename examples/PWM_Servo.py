#!/usr/bin/python3
# encoding: utf-8
import pigpio
import time
import os
open_io="sudo pigpiod"
os.system(open_io)
time.sleep(1)
#扩展板PWM接口1-8号对应扩展板IO口分别为12,16,20,21,19,13,5,6 。(树莓派扩展板7号和8号舵机接口为5V电压，所以9g舵机建议接PWM7和8号接口）
#如需更改接口请参考上方说明修改IO口号即可。
pin = 12 #要控制的IO口，这里以扩展板PWM1号接口为例。

pi = pigpio.pi()
pi.set_PWM_range(pin, 20000)#pin是要输出PWM的IO口， 20000设定PWM的调节范围，
                          #我们的舵机的控制信号是50Hz，就是20ms为一个周期。就是20000us。
                          #设为20000,就是最小调节为1us
pi.set_PWM_frequency(pin, 50) #设定PWM的频率，pin是要设定的IO口， 50 是频率
pi.set_PWM_dutycycle(pin, 1500)

while True:
    for i in range(500, 2500+1,5):
        pi.set_PWM_dutycycle(pin, i) #设定pwm的脉宽， pin为引脚，i为脉宽
        time.sleep(0.01)
    time.sleep(0.5)
    for i in range(2500, 500-1,-5):
        pi.set_PWM_dutycycle(pin, i)
        time.sleep(0.01)
    time.sleep(0.5)

