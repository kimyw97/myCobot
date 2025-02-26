from ultralytics import YOLO
from pymycobot import MyCobot320
import cv2
import time
import numpy as np

product_angles = [-8.45, 57.08, 7.29, 14.85, -91.75, -14.23]
red_box= [-9.49, 58.31, 11.51, -1.14, -71.71, 0.17]
purple_box= [-25.66, 58.96, 14.15, -11.77, -82.88, -2.98]
cam_angles = [-14.94, -4.83, 16.25, 20.21, -98.26, 0.0]
model = YOLO('best.pt')
mc = MyCobot320('COM4')
mc.send_angles(cam_angles,20)
isError = False
cap = cv2.VideoCapture(1)
mc.set_gripper_mode(0)
mc.init_eletric_gripper()
time.sleep(1.0)
mc.set_eletric_gripper(1)
mc.set_gripper_value(100, 20)
time.sleep(1.0)
mc.set_eletric_gripper(0)
mc.set_gripper_value(0, 20)

while True:
    ret, frame = cap.read()
    rotated_image = cv2.rotate(frame, cv2.ROTATE_180)
    # cv2.imshow('Webcam', rotated_image)
    # 모델로 객체 검출
    results = model(rotated_image)
    hsv = cv2.cvtColor(rotated_image , cv2.COLOR_BGR2HSV)
    color = "Unknown"
    # 빨간색 범위 정의 (두 개의 범위 필요)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # 보라색 범위 정의
    lower_purple = np.array([120, 50, 50])
    upper_purple = np.array([150, 255, 255])

    for result in results:
        class_indices = result.boxes.cls.cpu().numpy()  # 클래스 인덱스 가져오기
        class_names = [result.names[int(cls)] for cls in class_indices]
        print(class_names)
        if len(class_names) == 0 or 'error' in class_names:
            isError = True
        for box in result.boxes.xyxy:  # Bounding Box 좌표
            x1, y1, x2, y2 = map(int, box)  # 정수 변환

            # 객체 검출 영역 자르기
            roi = hsv[y1:y2, x1:x2]

            # 빨간색 & 보라색 마스크 생성
            mask_red1 = cv2.inRange(roi, lower_red1, upper_red1)
            mask_red2 = cv2.inRange(roi, lower_red2, upper_red2)
            mask_red = mask_red1 + mask_red2

            mask_purple = cv2.inRange(roi, lower_purple, upper_purple)

            # 색상 픽셀 개수 계산
            red_count = np.sum(mask_red > 0)
            purple_count = np.sum(mask_purple > 0)

            # 색상 판별
            if red_count > purple_count:
                color = "Red"
            elif purple_count > red_count:
                color = "Purple"
    cv2.imshow("Detected Image", rotated_image)
    print('=======')
    print(color)

    #객체에 맞게 움직
    if not isError:
        #그리퍼 열기
        mc.set_eletric_gripper(1)
        mc.set_gripper_value(100, 20)
        time.sleep(1.0)
        #물건 위치로 이동
        mc.send_angles(product_angles,20)
        time.sleep(5.0)
        #그리퍼 닫기
        mc.set_eletric_gripper(0)
        mc.set_gripper_value(0,20)
        time.sleep(1.0)
        # 색상 판별
        if color == 'Red':
            mc.send_angle(red_box,20)
        elif color =='Purple':
            mc.send_angle(purple_box,20)
        else: 
            print('df')
        
        #색깔에 맞는 위치로 이동
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

mc.send_angles([0,0,0,0,0,0],20)
# cap.release()
cv2.destroyAllWindows()

