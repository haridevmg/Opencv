# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 07:10:55 2022

@author: gilesh.mp
"""

import cv2 
import mediapipe as mp
import time

mpPose=mp.solutions.pose
poses=mpPose.Pose()
mpDraw=mp.solutions.drawing_utils


pTime=0
cap=cv2.VideoCapture(0)

while True:
    ret,img=cap.read()
    
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=poses.process(imgRGB)
    
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
        for id,lm in enumerate(results.pose_landmarks.landmark):
            h,w,c=img.shape
            cx,cy=int(lm.x*w),int(lm.y*h)
            print(id,cx,cy)
            if id in [15,16,12,11,23,24,27,28]:
                cv2.circle(img,(cx,cy),15,(255,255,0),cv2.FILLED)
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    
    cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_SIMPLEX,2,(25,255,100),4)
    print(str(int(fps)))
    
    if ret:
        cv2.imshow("Video",img)
    
        
    if 0xFF and ord('q')==cv2.waitKey(1):
        break
    
cap.release()
cv2.destroyAllWindows()