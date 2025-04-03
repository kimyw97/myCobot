import cv2
import numpy as np

img = cv2.imread('./myagv/rgb.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blurred = cv2.GaussianBlur(gray,(5,5), 0)

edges = cv2.Canny(blurred, 50,150)

contours,_ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(img, contours, -1, (0,0,0),2)

cv2.imshow("Contours",img)

cv2.waitKey(0)
cv2.destroyAllWindows()