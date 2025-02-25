from pymycobot import MyCobot320
import time

mc = MyCobot320('COM4',115200)
mc.send_angles([0,0,0,0,0,0],20)
time.sleep(2.0)
mc.send_angle(1,20,20)