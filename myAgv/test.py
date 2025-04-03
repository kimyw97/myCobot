import cv2
import numpy as np

def detect_white_contours(image):
    # 이미지 로드
    if image is None:
        print("이미지를 불러올 수 없습니다.")
        return
    
    # BGR에서 Grayscale로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 흰색 영역 감지를 위한 이진화
    _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    
    # 윤곽선 찾기
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    # 가장 큰 윤곽선 찾기
    largest_contour = max(contours, key=cv2.contourArea) if contours else None
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
    return image
   

# 테스트 실행
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    result = detect_white_contours(frame)

    # 결과 출력
    cv2.imshow("Contour Detection", result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()