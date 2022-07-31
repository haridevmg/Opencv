# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 09:39:56 2022

@author: gilesh.mp
"""

import cv2
import mediapipe as mp
import time
import handdemo as htm
import autopy
import numpy as np
import math

wCam=640
hCam=480



cap=cv2.VideoCapture(0)

cap.set(3,wCam)
cap.set(4,hCam)

detector=htm.HandDetection()

wScr,hScr=autopy.screen.size()

print(wScr,hScr)

pTime=0

while True:
    ret,img=cap.read()
    
    img=detector.process_hands(img)
    
    lmList=detector.findPosition(img)
    
    if len(lmList)!=0:
    
        ix,iy,i2=lmList[8][1],lmList[8][2],lmList[6][2]
        mx,my,m2=lmList[12][1],lmList[12][2],lmList[10][2]
        
        jx,jy=0,0
        
        if iy<i2 and my<m2:
            # Click Mode
            #print('Click Mode')
            
            cv2.circle(img,(mx,my),3,(255,255,0),cv2.FILLED)
            cv2.circle(img,(ix,iy),3,(255,255,0),cv2.FILLED)
            length=math.hypot(abs(mx-ix),abs(my-iy))
            cv2.line(img,(mx,my),(ix,iy),(255,255,0),3)
            
            if length<50:
                autopy.mouse.click()
            
        elif iy<i2:
            # Mouse mode
            # print('Mouse mode')
            jx=np.interp(ix,(0,wCam),(0,wScr))
            jy=np.interp(iy,(0,hCam),(0,hScr))
            
            print(jx,jy)
            autopy.mouse.move(jx, jy)
            
    
    
    
    cTime=time.time()
    fps=int(1/(cTime-pTime))
    pTime=cTime
    
    cv2.putText(img,str(fps),(40,70),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),3)
    
    if ret:
        cv2.imshow("Video",img)
    if 0xFF and ord('q')==cv2.waitKey(1):
        break

cap.release()
cv2.destroyAllWindows()
