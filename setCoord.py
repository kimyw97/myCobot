product_angles = [-10.45, 55.08, 7.29, 14.85, -91.75, -14.23]
error_box_angles = [-9.49, 58.31, 11.51, -1.14, -71.71, 0.17]
normal_box_angles = [-25.66, 58.96, 14.15, -11.77, -82.88, -2.98]

from pymycobot import MyCobot320
import time

mc = MyCobot320('COM4')
mc.send_angles(product_angles,20)
time.sleep(2.0)
mc.send_angles(error_box_angles,20)
time.sleep(2.0)
mc.send_angles(normal_box_angles,20)
time.sleep(2.0)
mc.send_angles([0,0,0,0,0,0],20)
time.sleep(2.0)
