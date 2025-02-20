from pymycobot import MyCobot320
import time

mc = MyCobot320('COM4',115200)
count = 0
print('The program is running')
while count < 5:
    print('count = ', count + 1)
    print('move to root')
    mc.send_angles([0,0,0,0,0,0], 20)
    mc.send_angle(1,10,20)
    time.sleep(2.0)
    mc.send_angle(2,10,20)
    time.sleep(2.0)
    mc.send_angle(3,10,20)
    time.sleep(2.0)
    mc.send_angle(4,10,20)
    time.sleep(2.0)
    mc.send_angle(5,10,20)
    time.sleep(2.0)
    mc.send_angle(6,10,20)
    time.sleep(2.0)
    count += 1
mc.send_angles([0,0,0,0,0,0],20)