from pymycobot import MyCobot320
import time

mc = MyCobot320('COM4')
mc.send_angles([20,20,0,0,0,0],20)
mc.set_gripper_mode(0)
mc.init_eletric_gripper()
print('Gripper Close')
mc.set_eletric_gripper(1)
mc.set_gripper_value(0,20)

time.sleep(2.0)
print('Gripper Open')
mc.set_eletric_gripper(0)
mc.set_gripper_value(100,20)

time.sleep(2.0)
print('Catch Object')
mc.set_eletric_gripper(1)
mc.set_gripper_value(0,20)

time.sleep(2.0)
mc.send_angles([0,0,0,0,0,0],20)

