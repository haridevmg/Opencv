# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 17:59:49 2022

@author: gilesh.mp


"""

import cv2
import mediapipe as mp
import time
import numpy as np
import handdemo as htm
import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

pTime=0

cap=cv2.VideoCapture(0)
detector=htm.HandDetection()


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRan=volume.GetVolumeRange()
volume.SetMasterVolumeLevel(0.0, None)

VolMin=volRan[0]
VolMax=volRan[1]
volPer=0

while True:
    ret,img =cap.read()
    
    img=detector.process_hands(img)
    lmList=detector.findPosition(img,draw=False)
    
    if len(lmList)!=0:
        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        
        cv2.circle(img,(x1,y1),10,(255,255,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(255,255,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,255,0),3)
        
        ax,ay=(x1+x2)//2,(y1+y2)//2
        
        
        length=math.hypot(x2-x1,y2-y1)
        print(length)
        
        if length<80:
            cv2.circle(img ,(ax,ay),5,(0,0,255),cv2.FILLED)
        elif length>200:
            cv2.circle(img ,(ax,ay),5,(0,255,0),cv2.FILLED)
        else:
           cv2.circle(img ,(ax,ay),5,(255,255,0),cv2.FILLED) 
           
        vol=np.interp(length,[50,240],[-65,0])
        volume.SetMasterVolumeLevel(float(vol), None)
        level=int(np.interp(length,[50,240],[150,400]))
        cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
        cv2.rectangle(img,(50,level),(85,400),(0,255,0),cv2.FILLED)
        
    cTime=time.time()
    fps=int(1/(cTime-pTime))
    pTime=cTime
    
    cv2.putText(img,str(fps),(70,70),cv2.FONT_HERSHEY_PLAIN,5,(255,0,0),3)
    
    if ret:
        cv2.imshow("Video",img)
        
    if 0xFF and ord('q')==cv2.waitKey(1):
        break
    
cap.release()
cv2.destroyAllWindows()

