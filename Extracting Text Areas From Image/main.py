import cv2
import numpy as np;

im = cv2.imread("im.png")

im_gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(im_gray,127,255,cv2.THRESH_BINARY_INV)

edges = cv2.Canny(im_gray,50,150,apertureSize = 3)
minLineLength = 100
maxLineGap = 100
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
for line in lines:
	for x1,y1,x2,y2 in line:
		cv2.line(thresh,(x1,y1),(x2,y2),(0),5)


kernel = np.ones((3,3),np.uint8)

thresh = cv2.dilate(thresh,kernel,iterations = 10)





_,contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
minArea=5000 #nothing 
for cnt in contours:
	area=cv2.contourArea(cnt)
	if(area>minArea):
		rect = cv2.minAreaRect(cnt)
    	box = cv2.boxPoints(rect)
    	box = np.int0(box)
    	cv2.drawContours(im,[box],0,(0,0,255),2)

cv2.imshow("thresh", im)
cv2.imwrite('so_result.jpg',im)
cv2.waitKey(0)