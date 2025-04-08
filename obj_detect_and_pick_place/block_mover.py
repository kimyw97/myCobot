from pymycobot import MyCobot320
import time
import cv2
from ultralytics import YOLO

stop_flag = False

mc = MyCobot320('COM8', 115200)

model = YOLO(r"C:\Users\okpjh\Documents\vscode\myCobot\obj_detect_and_pick_place\runs\detect\train9\weights\best.pt")

mc.power_on()
time.sleep(1)
mc.set_gripper_mode(0)
mc.init_electric_gripper()
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
yellow_position = [-34.01, 37.61, 48.51, -1.23, -83.14, -32.08]
#green 적재 위치치
green_position = [-40.1, 50.71, 31.28, -2.63, -88.15, -44.47]
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

detected_color = ''
err_color = 'blue'
is_color_detecting = False



#해당 블록 위치로 이동하는 함수
def place_object_by_color(color):
    if color != err_color:
        base_position = positions[color].copy()
        z_offset= 7*stack_count[color]
        base_position[1] -= z_offset
        
        print(f"{color} 블록 적재 위치로 이동중...(Z + {z_offset}mm)")
        mc.send_angles(base_position,60)
        time.sleep(2)
        
        stack_count[color] += 1
        
    elif color == err_color:
        print("불량품 감지 - 처리 위치로 이동중...")
        mc.send_angles(waste_position, 60)
        time.sleep(2)
        
    else:
        print(f"{color}는 등록되지 않은 색상. 아무 작업 수행 x")

    global detected_color
    detected_color = ''

def detect_block_color():
    global is_color_detecting
    is_color_detecting = True
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("웹캠 열기 실패")
        return ''
    start_time = time.time()
    label = ''
    while time.time() - start_time < 3:  # 최대 3초 대기
        ret, frame = cap.read()
        if not ret:
            continue
        results = model(frame, verbose=False)
        boxes = results[0].boxes
        
        for box in boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            if conf > 0.6:  # 신뢰도 필터링
                label = model.names[cls_id]
    cap.release()
    is_color_detecting = False
    return label
        

def main():
    print('종료하려면 q를 입력하세요')
    cmd = input()
    global stop_flag
    if cmd == 'q':
        stop_flag = True
    
    time.sleep(1.5)
    mc.send_angles(cam_detecting_point, 60)
    print("객체 인식 위치 이동 중...")
    time.sleep(1.5) 
    global detected_color
    detected_color = detect_block_color()
    global is_color_detecting
    while is_color_detecting:
        print('색깔 감지중')
    if detected_color == '':
        print("객체 인식 실패. 다시 시도합니다.")
        return
    print(f"감지된 색상: {detected_color}")

    # 그리퍼 열기
    mc.set_gripper_state(0,50,4)
    print("그리퍼가 열렸습니다")
    time.sleep(1)
    
    #픽업하기 위한 위치로 로봇팔 이동
    mc.send_angles(pickup_point,60)
    print("객체 pick up 위치로 이동")
    time.sleep(5)

    #그리퍼 닫기(물체 감도 인식으로)
    mc.set_gripper_state(1,50,4)
    time.sleep(1)
    print("물체 잡았습니다. 이동합니다.")
    

    #걸릴까봐 카메라basepoint로 이동
    mc.send_angles(cam_detecting_point,60)
    time.sleep(1.5)

    # 물체 적재 basepoint로 로봇팔 이동
    mc.send_angles(stack_base_point,60)
    time.sleep(1.5)
    
    place_object_by_color(detected_color)
    time.sleep(1)
    
    # 그리퍼 열기
    mc.set_gripper_state(0,50,4)
    time.sleep(1)
    print("물체 적재")


    #basepoint로 로봇팔 이동
    mc.send_angles(stack_base_point, 60)
    time.sleep(1)
    
    # 그리퍼 닫기
    mc.set_gripper_state(1,50,4)
    time.sleep(1)
    print("물체 적재")
    
    mc.send_angles(home_angles, 60)
    print("원점 이동 중...")
    time.sleep(5)

    #----------------------------------------------반복문끝
    
mc.send_angles(home_angles, 60)
print("원점 이동 중...")
time.sleep(5)

while not stop_flag:
    main()
    time.sleep(0.5)
    
   
mc.send_angles(home_angles, 60)
print("로봇팔 원점으로 이동 및 종료")

    