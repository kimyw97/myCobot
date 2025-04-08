import cv2
from ultralytics import YOLO

# YOLO 모델 로드 (필요에 따라 yolov8n.pt, yolov8s.pt, yolov8m.pt 등 사용 가능)
model = YOLO(r"C:\Users\okpjh\Documents\vscode\myCobot\obj_detect_and_pick_place\runs\detect\train9\weights\best.pt")

# 웹캠 열기 (0번은 기본 카메라)
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
            2
        )

    # 화면에 표시
    cv2.imshow("YOLOv8 Webcam Detection", frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
