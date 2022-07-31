# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 09:17:20 2022

@author: gilesh.mp
"""
import cv2 
import mediapipe as mp
import time

class poseDetector:
    
    def __init__(self,
               mode=False,
               complexity=1,
               smooth_landmarks=True,
               enable_segmentation=False,
               smooth_segmentation=True,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5):
        
        self.mode=mode
        self.complex=complexity
        self.smooth=smooth_landmarks
        self.enable=enable_segmentation
        self.sm_seg=smooth_segmentation
        self.detectCon=min_detection_confidence
        self.trackCon=min_tracking_confidence
        
        
        

        self.mpPose=mp.solutions.pose
        self.poses=self.mpPose.Pose(self.mode,self.complex,self.smooth,
                                    self.enable,self.sm_seg,self.detectCon,self.trackCon)
        self.mpDraw=mp.solutions.drawing_utils
        self.results=[]


    def process(self,img,draw=True):
    
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.poses.process(imgRGB)
        
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return img
                
    def track(self,img,t_num=[11,12,15,16,23,24,27,28]):
        
        lmList=[]
        
        if self.results.pose_landmarks:
            for id,lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                if id in t_num:
                    cv2.circle(img,(cx,cy),15,(255,255,0),cv2.FILLED)
                    lmList.append([id,cx,cy])
        return img,lmList
   

def main():
    
    pMac=poseDetector()
    pTime=0
    cap=cv2.VideoCapture(0)
    
    while True:
        ret,img=cap.read()
        
        img = pMac.process(img)
        img,lmList = pMac.track(img,[])
        
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        
        cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_SIMPLEX,2,(25,255,100),4)
        print(str(int(fps)))
        
        
        if ret:
            cv2.imshow("Video",img)
        
            
        if 0xFF and ord('q')==cv2.waitKey(1):
            break
    print(lmList)
    cap.release()
    cv2.destroyAllWindows()
        
    

if __name__=="__main__":
    main()