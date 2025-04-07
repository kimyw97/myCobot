from pymycobot import MyCobot320
import time
import keyboard
import threading
import cv2
from ultralytics import YOLO

stop_flag = False

mc = MyCobot320('COM8', 115200)

model = YOLO("/Users/kyw/VSCode/myCobot/obj_detect_and_pick_place/runs/detect/train9/weights/best.pt")

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
pickup_point = [33.66, -5.0, 83.05, -7.29, -77.51, -56.42]
#red 적재 위치
red_position = [-7.29, 33.92, 52.55, -6.41, -89.73, -10.1]
#yellow 적재 위치치
yellow_position = [-31.02, 37.61, 48.51, -1.23, -83.14, -32.08]
#green 적재 위치치
green_position = [-47.1, 50.71, 31.28, -2.63, -88.15, -44.47]
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



#해당 블록 위치로 이동하는 함수
def place_object_by_color(color):
    if color != err_color:
        base_position = positions[color].copy()
        z_offset= 25*stack_count[color]
        base_position[2] += z_offset
        
        print(f"{color} 블록 적재 위치로 이동중...(Z + {z_offset}mm)")
        mc.send_angles(base_position,20)
        time.sleep(2)
        
        stack_count[color] += 1
        
    elif color == err_color:
        print("불량품 감지 - 처리 위치로 이동중...")
        mc.send_angles(waste_position, 20)
        time.sleep(2)
        
    else:
        print(f"{color}는 등록되지 않은 색상. 아무 작업 수행 x")

    global detected_color
    detected_color = ''
        

def main():
    #로봇팔 원점 이동
    mc.send_angles(home_angles, 20)
    print("로봇팔 원점으로 이동")
    time.sleep(3)
    #-----------------------------반복문 시작

    # 컨베이어 위치 (for카메라 인식)로 로봇팔 이동
    mc.send_angles(cam_detecting_point,20)
    print("객체인식 준비 완료")
    time.sleep(5)
    
    # #a단계
    # #카메라로 블록 및 색상 인식
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("웹캠을 열 수 없습니다.")
        exit()
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # YOLO로 추론
        results = model(frame, verbose=False)

        # 결과 박스 그리기
        boxes = results[0].boxes
        global detected_color
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

        # 박스와 라벨 그리기
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"{label} {conf:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2)

        # 화면에 표시
        cv2.imshow("YOLOv8 Webcam Detection", frame)
        
        if detected_color != '':
            break

    cap.release()
    time.sleep(2.0)
    cv2.destroyAllWindows()

    # 그리퍼 열기
    mc.set_gripper_state(0,50,4)
    time.sleep(5)
    
    #픽업하기 위한 위치로 로봇팔 이동
    mc.send_angles(pickup_point,20)
    print("객체 pick up 위치로 이동")
    time.sleep(5)

    #그리퍼 닫기(물체 감도 인식으로)
    mc.set_gripper_state(1,50,4)
    time.sleep(2)
    print("물체 잡았습니다. 이동합니다.")
    

    #걸릴까봐 카메라basepoint로 이동
    mc.send_angles(cam_detecting_point,20)
    time.sleep(5)

    # 물체 적재 basepoint로 로봇팔 이동
    mc.send_angles(stack_base_point,20)
    time.sleep(5)
    
    place_object_by_color(detected_color)
    time.sleep(5)
    
    # 그리퍼 열기
    mc.set_gripper_state(0,50,4)
    time.sleep(5)
    print("물체 적재")


    #basepoint로 로봇팔 이동
    mc.send_angles(stack_base_point, 30)
    time.sleep(2)
    
    # 그리퍼 닫기기
    mc.set_gripper_state(1,50,4)
    time.sleep(2)
    print("물체 적재")

    #----------------------------------------------반복문끝
    
def input_keyboard():
    global stop_flag
    keyboard.wait('q')
    print("q키 눌림. 프로그램 종료중")
    stop_flag = True
    
threading.Thread(target=input_keyboard, daemon=True).start()

while not stop_flag:
    main()
    time.sleep(0.5)
    
   
mc.send_angles(home_angles, 20)
print("로봇팔 원점으로 이동 및 종료")

    