import cv2
import numpy as np

def detect_color_contours(img_path, lower_color, upper_color):
    img = cv2.imread(img_path)

    if img is None:
        return
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_color, upper_color)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(img, contours, -1, (0,255,0),2)

    cv2.imshow("detect_contours", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


lower_blue = np.array([100,100,100])
upper_blue = np.array([140,255,255])
detect_color_contours('./myagv/rgb.png', lower_blue, upper_blue)