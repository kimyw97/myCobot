import cv2
from ultralytics import YOLO

model_path = './runs/detect/train2/weights/best.pt'
cap = cv2.VideoCapture(0)
model = YOLO(model_path)
while True:
    ret, img = cap.read()
    result =  model(img)
    print(result)
    annotated_frame = result[0].plot()
    cv2.imshow('webcam', annotated_frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()