from pymycobot import MyCobot320
import time
import keyboard

mc = MyCobot320("COM8", 115200)

# 수정 전 위치 정의 ---------------------
home_angles = [0,0,0,0,0,0]
#컨베이어에서 카메라 디텍팅 포인트
cam_detecting_point = [32.25, -20.3, 74.44, 7.91, -71.98, -44.73]
#적재 베이스 포인트 위치
stack_base_point = [-34.1, -0.08, 32.1, 7.82, -83.84, -26.63]
#컨베이어 물체 픽업 위치
pickup_point = [31.65, -2.0, 83.05, -4.28, -77.51, -56.42]
#red 적재 위치
red_position = [-11.29, 37.92, 52.55, -6.41, -89.73, -10.1]
#yellow 적재 위치치
yellow_position = [-34.01, 37.61, 48.51, -1.23, -83.14, -32.08]
#green 적재 위치치
green_position = [-40.1, 50.71, 31.28, -2.63, -88.15, -44.47]
#불량품 위치
waste_position = [-87.8, 11.51, 52.2, -2.02, -92.9, -3.51]
#----------------------------------
snd_red_pos = [-14.29, 34.92, 52.55, -6.41, -89.73, -10.1]
trd_red_pos = [-18.29, 30.92, 52.55, -6.41, -89.73, -10.1]
#---------------------------------
positions = {
    'red' : red_position,
    'yellow': yellow_position,
    'green': green_position,
    'blue':waste_position
}
#-------------------------------


# 초기 설정 각도
current_point = red_position
base_point = [0, 0, 0, 0, 0, 0]

#---------------------------------
print("""
--- 키보드 제어 안내 ---
Joint 1: z / x
Joint 2: q / a
Joint 3: w / s
Joint 4: e / d
Joint 5: r / f
Joint 6: t / g
ESC: 종료
""")
#--------------------------------
prev_keys = set()
#----------------
mc.send_angles(base_point, 20)
print("초기 설정 각도로 이동")
time.sleep(2)

mc.set_gripper_mode(0)
# mc.init_electric_gripper()
time.sleep(1)

mc.set_gripper_state(0, 50, 4)
time.sleep(1)
print("물체 집기준비비")


# 해당 설정 각도로 이동
mc.send_angles(current_point, 20)
print("초기 설정 각도로 이동동")
time.sleep(2)


while True:
    current_keys = set()
    
    # 조인트 1
    if keyboard.is_pressed('z'):
        current_point[0] += 1
        mc.send_angles(current_point, 20)
        print("joint 1+1 ->", current_point)
        time.sleep(0.1)
    elif keyboard.is_pressed('x'):
        current_point[0] -= 1
        mc.send_angles(current_point, 20)
        print("joint 1-1 ->", current_point)
        time.sleep(0.1)
        
    # 조인트 2
    if keyboard.is_pressed('q'):
        current_point[1] += 1
        mc.send_angles(current_point, 20)
        print("joint 1+1 ->", current_point)
        time.sleep(0.1)
    elif keyboard.is_pressed('a'):
        current_point[1] -= 1
        current_point[0] -= 1
        mc.send_angles(current_point, 20)
        print("joint 1-1 ->", current_point)
        time.sleep(0.1)

    # 조인트 3
    if keyboard.is_pressed('w'):
        current_point[2] += 1
        mc.send_angles(current_point, 20)
        print("joint 1+1 ->", current_point)
        time.sleep(0.1)
    elif keyboard.is_pressed('s'):
        current_point[2] -= 1
        current_point[0] -= 1
        mc.send_angles(current_point, 20)
        print("joint 1-1 ->", current_point)
        time.sleep(0.1)

    # 조인트 4
    if keyboard.is_pressed('e'):
        current_point[3] += 1
        mc.send_angles(current_point, 20)
        print("joint 1+1 ->", current_point)
        time.sleep(0.1)
    elif keyboard.is_pressed('d'):
        current_point[3] -= 1
        current_point[0] -= 1
        mc.send_angles(current_point, 20)
        print("joint 1-1 ->", current_point)
        time.sleep(0.1)

    # 조인트 5
    if keyboard.is_pressed('r'):
        current_point[4] += 1
        mc.send_angles(current_point, 20)
        print("joint 1+1 ->", current_point)
        time.sleep(0.1)
    elif keyboard.is_pressed('f'):
        current_point[4] -= 1
        current_point[0] -= 1
        mc.send_angles(current_point, 20)
        print("joint 1-1 ->", current_point)
        time.sleep(0.1)

    # 조인트 6
    if keyboard.is_pressed('t'):
        current_point[5] += 1
        mc.send_angles(current_point, 20)
        print("joint 1+1 ->", current_point)
        time.sleep(0.1)
    elif keyboard.is_pressed('g'):
        current_point[5] -= 1
        current_point[0] -= 1
        mc.send_angles(current_point, 20)
        print("joint 1-1 ->", current_point)
        time.sleep(0.1)

    # ESC 키로 종료
    if keyboard.is_pressed('esc'):
        print("종료합니다.")
        break
    
    if current_keys - prev_keys:
        
        # 현재 각도 전송
        mc.send_angles(current_point, 20)
        print("현재 각도:", current_point)
    
    prev_keys = current_keys

    time.sleep(0.2)  # 입력 너무 빠르게 처리되지 않도록 조절
    

mc.set_gripper_state(1, 50, 4)
time.sleep(1)
print("물체 집기준비")

# 원점 0 각도로 이동
mc.send_angles(base_point, 20)
print("초기 설정 각도로 이동")
time.sleep(2)
