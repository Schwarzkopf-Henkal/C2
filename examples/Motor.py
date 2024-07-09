#!/usr/bin/python3
#coding=utf8
#功能：控制左右电机以100%的速度转动，然后再以50%的速度反向转动
#原理：通过改变PWM脉冲信号的占空比来改变电机转速，占空比越大速度就越快，占空比为100%时相当于输入1（高电平），占空比为0%时相当于输入0（低电平）
#启动程序前，在命令行输入sudo pigpiod
import pigpio
import time
import os
open_io="sudo pigpiod"
os.system(open_io)
time.sleep(1)
class CarMotor(object):
    def __init__(self, in1 = 26, in2 = 18, in3 = 7, in4 = 8):
        #4个电机引脚号,采用BCM编码
        self.Pi = pigpio.pi()
        self.In1 = in1
        self.In2 = in2
        self.In3 = in3
        self.In4 = in4

        #指定要把引脚上的一个pwm周期分成100份
        self.Pi.set_PWM_range(self.In1, 100)#pwm范围
        self.Pi.set_PWM_range(self.In2, 100)
        self.Pi.set_PWM_range(self.In3, 100)
        self.Pi.set_PWM_range(self.In4, 100)
        
        ##设定引脚产生的pwm波形的频率为10Khz
        self.Pi.set_PWM_frequency(self.In1, 10000)#频率10khz
        self.Pi.set_PWM_frequency(self.In2, 10000)
        self.Pi.set_PWM_frequency(self.In3, 10000)
        self.Pi.set_PWM_frequency(self.In4, 10000)

        #指定pwm波形的占空比，这里的占空比为0/100,也就是占空比为0，这里的100是指上面分成100份
        self.Pi.set_PWM_dutycycle(self.In1, 0)#暂停pwm输出
        self.Pi.set_PWM_dutycycle(self.In2, 0)
        self.Pi.set_PWM_dutycycle(self.In3, 0)
        self.Pi.set_PWM_dutycycle(self.In4, 0)

    def SetSpeed(self, Left = 0, Right = 0):#保持电机的速度参数值在-100到100之间
        Left = -100  if Left < -100 else Left
        Left =  100  if Left >  100 else Left
        Right = 100  if Right > 100 else Right
        Right = -100 if Right < -100 else Right

        DutyIn1 = 0 if Left < 0 else Left
        DutyIn2 = 0 if Left > 0 else -Left
        DutyIn3 = 0 if Right < 0 else Right
        DutyIn4 = 0 if Right > 0 else -Right

        self.Pi.set_PWM_dutycycle(self.In1, DutyIn1)#开始pwm输出
        self.Pi.set_PWM_dutycycle(self.In2, DutyIn2)
        self.Pi.set_PWM_dutycycle(self.In3, DutyIn3)
        self.Pi.set_PWM_dutycycle(self.In4, DutyIn4)

if __name__ == "__main__":
        
    carmove = CarMotor()
    carmove.SetSpeed(0,0)#设置电机初始状态为停止
    carmove.SetSpeed(100,100)#设置电机以100%的速度转动
    time.sleep(2)
    carmove.SetSpeed(-50,-50)#设置电机以50%的速度反向转动
    time.sleep(2)
    carmove.SetSpeed(0,0)#设置电机停下

