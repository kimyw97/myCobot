import cv2

img = cv2.imread('./myAgv/rgb.png')

x,y,width,height = 350,400,500,800

roi = img[y:y+height,x:x+width]
gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

cv2.imshow('roi', gray_roi)
cv2.waitKey(0)
cv2.destroyAllWindows()