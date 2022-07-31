# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 17:54:35 2022

@author: gilesh.mp
"""

import cv2
import mediapipe as mp
import time
import handdemo as htm
import os
import math


cap=cv2.VideoCapture(0)

detector=htm.HandDetection(detect_min=0.4)

folderPath="finger_images"
myList=os.listdir("finger_images")
print(myList)

overlayList=[]

for i in myList:
    image=cv2.imread(f"{folderPath}\{i}")
    overlayList.append(image)

pTime=0
count=0
while True:
    ret,img=cap.read()
    
    
    img=detector.process_hands(img)
    lmList=detector.findPosition(img,draw=False)
    
    
    if len(lmList)!=0:
        t1,t2=lmList[8][2],lmList[6][2]
        if t1<t2:
            count+=1
        u1,u2=lmList[12][2],lmList[10][2]
        if u1<u2:
            count+=1
        v1,v2=lmList[16][2],lmList[14][2]
        if v1<v2:
            count+=1
        w1,w2=lmList[20][2],lmList[18][2]
        if w1<w2:
            count+=1
        x1,x2=lmList[4][1],lmList[2][1]
        if x1<x2:
            count+=1
        # z=lmList[0][1:]
        # u=lmList[12][1:]
        
        # length=math.hypot(abs(z[0]-u[0]),abs(z[1]-u[1]))
        # if length>230:
        #     count=0
        print(count)
        index=overlayList[count]
        h,w,c=index.shape
    
        img[0:h,0:w]=overlayList[count]
        
    count=0
        
    
    cTime=time.time()
    fps=int(1/(cTime-pTime))
    pTime=cTime
    
    cv2.putText(img,str(fps),(530,80),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),4)
    
    if ret:
        cv2.imshow("Video",img)
        
    if 0xFF and ord('q')==cv2.waitKey(1):
        break
    
cap.release()
cv2.destroyAllWindows()