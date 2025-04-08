from pymycobot import MyCobot320
import time
import cv2
from ultralytics import YOLO


mc = MyCobot320('COM8', 115200)
stop_flag = False


mc.power_on()
time.sleep(1)
mc.set_gripper_mode(0)
# mc.init_electric_gripper()
time.sleep(1)

# [위치 정의] --------------------------------
home_angles = [0,0,0,0,0,0]
#컨베이어에서 카메라 디텍팅 포인트
cam_detecting_point = [32.25, -20.3, 74.44, 7.91, -71.98, -44.73]
#적재 베이스 포인트 위치
stack_base_point = [-34.1, -0.08, 32.16, 7.82, -83.84, -26.63]
#컨베이어 물체 픽업 위치
pickup_point = [31.65, -2.0, 83.05, -4.28, -77.51, -56.42]
#red 적재 위치
red_position = [-11.29, 37.92, 52.55, -6.41, -89.73, -10.1]
#yellow 적재 위치치
yellow_position = [-35.01, 38.61, 48.51, -1.23, -83.14, -32.08]
#green 적재 위치치
green_position = [-46.1, 50.71, 31.28, -2.63, -88.15, -44.47]
#불량품 위치
waste_position = [-87.8, 11.51, 52.2, -2.02, -92.9, -3.51]
#----------------------------------------------
positions = {
    'red' : red_position,
    'yellow': yellow_position,
    'green': green_position,
    'blue':waste_position
}
#----------------------------------------------
# 블록 적재 횟수 저장용 카운터 (Z축 올리기용)
stack_count = {
    'red': 0,
    'yellow': 0,
    'green': 0,
    'blue': 0
}
#---------------------------------------------
# coords 위치좌표 -----------------------------
red_coords = [-315.6, -27.0, 300.3, -174.15, -0.73, 88.48]
yellow_coords = [-303.7, 94.1, 229.3, -172.99, 3.68, 87.82]
green_coords = [-291.1, 175.0, 230.6, -170.93, -6.45, 87.53]
waste_coords = [-92.9, 247.3, 344.7, -152.36, -4.04, 3.58]
#____________________________

double_stack_red_coords =[-315.6, -27.0, 230.3, -174.15, -0.73, 88.48]





detected_color = ''
err_color = 'blue'
is_color_detecting = False



# 색상별 기본 좌표 (Z축만 나중에 누적 보정)
# coords = {
#     'red': [200, 0, 50, 0, 0, 0],
#     'yellow': [250, 0, 50, 0, 0, 0],
#     'green': [300, 0, 50, 0, 0, 0],
# }

# 적재 카운트 (몇 개 쌓였는지)
stack_count = {
    'red': 0,
    'yellow': 0,
    'green': 0,
}


# #그리퍼 열기
# mc.set_gripper_state(1, 50, 4)
# print("그리퍼가 열렸습니다")
# time.sleep(1)

#그리퍼 열기
mc.set_gripper_state(0, 50, 4)
print("그리퍼가 열렸습니다")
time.sleep(1)

mc.set_gripper_value(30, 50, 1)
print("일부 닫힘")
time.sleep(1)

mc.set_gripper_value(60, 50, 1)
print("일부 닫힘")
time.sleep(1)

mc.set_gripper_state(1, 50, 4)
print("그리퍼가 열렸습니다")
time.sleep(1)

# mc.send_angles(waste_position, 30)
# time.sleep(15)
# coords = mc.get_coords()
# print("현재 위치 좌표:", coords)

#basepoint로 로봇팔 이동
# mc.send_angles(stack_base_point, 60)
# time.sleep(1)

# mc.sync_send_coords(red_coords, speed=10, mode=0)  # mode=0: angular
# time.sleep(15)

# coords = mc.get_coords()
# print("현재 위치 좌표:", coords)

# # mc.sync_send_coords(yellow_coords, speed=30, mode=0)  # mode=0: angular
# # time.sleep(15)


# mc.send_angles(home_angles, 40)
# print("home 이동 중...")
# time.sleep(1.5) 