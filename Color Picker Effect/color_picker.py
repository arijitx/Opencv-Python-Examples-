import cv2
import numpy as np
import easygui
import sys
import math

drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1

def color_picker(rect):
	global img,img_gray2,hsv
	roi=img[rect[0][1]:rect[1][1],rect[0][0]:rect[1][0]]
	b,g,r,_=np.uint8(cv2.mean(roi))
	color=cv2.cvtColor(np.uint8([[[b,g,r]]]),cv2.COLOR_BGR2HSV)
	h= color[0][0][0]
	# define range of blue color in HSV
	lower = np.array([h-10,50,50])
	upper = np.array([h+10,255,255])

	# Threshold the HSV image to get only blue colors
	mask = cv2.inRange(hsv, lower, upper)

	# Bitwise-AND mask and original image
	res = cv2.bitwise_and(img,img, mask= mask)
	res2=cv2.bitwise_and(img_gray2,img_gray2, mask= cv2.bitwise_not(mask))
	return res+res2

def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode
    global img
    im=img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv2.rectangle(im,(ix,iy),(x,y),(0,255,0),1)
        cv2.imshow('image',im)
        cv2.imshow('res',color_picker([(ix,iy),(x,y)]))


img = cv2.imread(sys.argv[1])
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)
cv2.imshow('image',img)
img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img_gray2=cv2.cvtColor(img_gray,cv2.COLOR_GRAY2BGR)
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)


k = cv2.waitKey(0)
if k == ord('q'):         # wait for ESC key to exit
    cv2.destroyAllWindows()