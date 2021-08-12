"""
This script allows to collect raw points from an image.
The inputs are 2 mouse clicks one in the 0,0 position and the second in (w,h)/diagonal position of rectangle
Once a rectangle is selected the user is asked to enter the type and Name:
Type can be 'text' or 'box'
Name can be anything
"""

import cv2
import random
path = 'D:\\Year III\\FYP\\Form.png'
scale = 0.4
circles = []
counter = 0
counter2 = 0
points1 = []
points2 = []
myPoints = []
myColor = []



def mousePoints(event, x, y, flags, params):
    global counter, points1, points2, counter2, circles, myColor
    if event == cv2.EVENT_LBUTTONDOWN:
        if counter==0:
            points1 = int(x//scale), int(y//scale)
            counter +=1
            myColor = (random.randint(0,2)*200, random.randint(0,2)*200, random.randint(0,2)*200)
        elif counter ==1:
            points2 = int(x//scale), int(y//scale)
            type = input('Enter Type')
            name = input('Enter Name')
            myPoints.append([points1, points2, type, name])
            counter = 0
        circles.append([x,y,myColor])
        counter2 += 1

img = cv2.imread(path)
h,w,c = img.shape
img = cv2.resize(img,(0,0),None,scale,scale)

while True:
    #To display points
    for x, y, color in circles:
        cv2.circle(img,(x,y),3,color, cv2.FILLED)
    cv2.imshow("Original Image", img)
    cv2.setMouseCallback("Original Image", mousePoints)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        print(myPoints)
        break
