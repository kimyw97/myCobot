from ultralytics import YOLO
from pymycobot import MyCobot320
import cv2
import time
import numpy as np

product_angles = [-8.45, 59.08, 7.29, 14.85, -91.75, -14.23]
box_angles= [-9.49, 58.31, 11.51, -1.14, -71.71, 0.17]
cam_angles =[-15.9, 62.57, 2.54, 0.79, -84.99, 0.08]
isError = False

model = YOLO('best.pt')
mc = MyCobot320('COM4')
# 지정위치로 캠 옮기기
mc.send_angles(cam_angles,20)
# 그리퍼 테스트
mc.set_gripper_mode(0)
mc.init_eletric_gripper()
time.sleep(1.0)
mc.set_eletric_gripper(1)
mc.set_gripper_value(100, 20)
time.sleep(1.0)
mc.set_eletric_gripper(0)
mc.set_gripper_value(0, 20)

cap = cv2.VideoCapture(1)
while True:
    ret, frame = cap.read()
    rotated_image = cv2.rotate(frame, cv2.ROTATE_180)
    # 모델로 객체 검출
    results = model(rotated_image)
    img = results[0].plot()
    for result in results:
        class_indices = result.boxes.cls.cpu().numpy()  # 클래스 인덱스 가져오기
        class_names = [result.names[int(cls)] for cls in class_indices]
        if len(class_names) == 0 or 'error' in class_names:
            isError = True
        else:
            isError = False
    cv2.imshow("Detected Image", img)
    if not isError:
        #그리퍼 열기
        mc.set_eletric_gripper(1)
        mc.set_gripper_value(100, 20)
        time.sleep(2.0)
        #물건 위치로 이동
        mc.send_angles(product_angles,20)
        time.sleep(3.0)
        #그리퍼 닫기
        mc.set_eletric_gripper(0)
        mc.set_gripper_value(0,20)
        time.sleep(2.0)
        # 바구리로 이동
        mc.send_angles(box_angles, 20)
        time.sleep(3.0)
        # 그리퍼 열기
        mc.set_eletric_gripper(1)
        mc.set_gripper_value(100, 20)
        # 캠 위치로 다시 이동 후 대기
        mc.send_angles(cam_angles,20)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

mc.send_angles([0,0,0,0,0,0],20)
mc.set_eletric_gripper(0)
mc.set_gripper_value(0, 20)

cap.release()
cv2.destroyAllWindows()


