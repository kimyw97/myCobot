from pymycobot import MyCobot320
import time
import  keyboard

product_angles = [-10.45, 61.08, 7.29, 14.85, -91.75, -14.23]
error_box_angles = [-9.49, 62.31, 11.51, -1.14, -71.71, 0.17]
normal_box_angles = [-25.66, 61.96, 14.15, -11.77, -82.88, -2.98]

mc = MyCobot320('COM4')
count = 0
time.sleep(2.0)
mc.release_all_servos()
while count< 10:
    print('running')
    time.sleep(1.0)
    count += 1
for i in range(1,7):
    mc.focus_servo(i)
time.sleep(2.0)
print(mc.get_angles())
time.sleep(5.0)
mc.send_angles([0,0,0,0,0,0],20)


