import cv2
import numpy as np
import time
import threading
from pymycobot import MyAgv
from queue import Queue

# AGV 객체 생성
agv = MyAgv('/dev/ttyAMA2')

# 프레임을 저장할 큐 (최대 5개까지 저장)
frame_queue = Queue(maxsize=5)

# AGV 제어 함수 (별도 쓰레드에서 실행)
def control_agv(direction):
    if direction == "Left":
        print("Turning counterclockwise at speed 10 for 2 seconds")
        agv.counterclockwise_rotation(10)
    else:
        print("Turning clockwise at speed 10 for 2 seconds")
        agv.clockwise_rotation(10)
    time.sleep(2)
    agv.stop()

# 영상 처리 쓰레드 함수
def process_frames():
    while True:
        if not frame_queue.empty():
            image = frame_queue.get()
            if image is None:
                break

            # BGR에서 Grayscale로 변환
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # 흰색 영역 감지를 위한 이진화
            _, mask = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

            # 윤곽선 찾기
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 가장 큰 윤곽선 찾기
            largest_contour = max(contours, key=cv2.contourArea) if contours else None

            # 윤곽선을 원본 이미지에 초록색으로 그림
            cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

            # 모멘트 계산 및 중심점 구하기
            if largest_contour is not None:
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])  # 중심 x 좌표
                    cy = int(M["m01"] / M["m00"])  # 중심 y 좌표
                    cv2.circle(image, (cx, cy), 5, (255, 0, 0), -1)  # 중심점 표시

                    # 이미지 중앙과 비교하여 방향 결정
                    img_center = image.shape[1] // 2
                    direction = "Left" if cx < img_center else "Right"
                    print(f"Current Position: {direction}")

                    # AGV 제어를 별도 쓰레드에서 실행
                    threading.Thread(target=control_agv, args=(direction,)).start()

            # 결과 출력
            cv2.imshow("Contour Detection", image)

# 영상 처리 쓰레드 시작
processing_thread = threading.Thread(target=process_frames, daemon=True)
processing_thread.start()

# 카메라 열기
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 최신 프레임만 유지하도록 큐 관리
    if frame_queue.full():
        frame_queue.get()
    frame_queue.put(frame)

    # 종료 조건
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
