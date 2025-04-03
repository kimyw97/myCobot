import cv2
import numpy as np

img = cv2.imread('./myAgv/rgb.png')
img = cv2.resize(img,dsize=(300,450))

center_coord = (150,150)
radius = 100

mask = np.zeros_like(img)
cv2.circle(mask, center_coord, radius, (255,255,255),thickness=cv2.FILLED)
circular_roi = cv2.bitwise_and(img,mask)

edges = cv2.Canny(circular_roi,400,150)

cv2.imshow('test',edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
