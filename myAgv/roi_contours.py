import cv2
import numpy as np

def find_contours_in_white(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(gray_img, 200,200,cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img,contours,-1,(0,255,0),2)
    return img


cap = cv2.VideoCapture('./myAgv/testVideo.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width, _ = frame.shape
    roi_height = height // 3
    roi = frame[2*roi_height:,:]
    
    result_frame = find_contours_in_white(roi)

    frame[2*roi_height:,:] = result_frame

    cv2.imshow('roi',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()