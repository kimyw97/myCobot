import cv2
import numpy as np
cap = cv2.VideoCapture('./myAgv/testVideo.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_white = np.array([0,0,200], dtype=np.uint8)
    upper_white = np.array([255,30,255], dtype=np.uint8)
    white_mask = cv2.inRange(frame,lower_white, upper_white)

    white_result = cv2.bitwise_and(frame, frame, mask=white_mask)

    height, width = frame.shape[:2]
    roi_top = height*2//3
    roi_bottom = height
    roi_left = 0
    roi_right = width

    roi = white_result[roi_top:roi_bottom, roi_left:roi_right]

    cv2.imshow('roi',roi)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()