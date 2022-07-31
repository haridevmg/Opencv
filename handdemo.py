# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 21:28:06 2022

@author: gilesh.mp
"""

import cv2 
import mediapipe as mp
import time

class HandDetection:
    
    def __init__(self,mode=False,max_num=2,detect_min=0.5,track_min=0.5):
        self.mode=mode
        self.max_num=max_num
        self.detect_min=detect_min
        self.track_min=track_min

        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode,self.max_num,self.detect_min,self.track_min)
        self.mpDraw=mp.solutions.drawing_utils
        
    def process_hands(self,frame):
        self.pred=self.hands.process(frame)
        if self.pred.multi_hand_landmarks:
            for i in self.pred.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(frame,i,self.mpHands.HAND_CONNECTIONS)
        return frame
    def findPosition(self,frame,hand_num=0,draw=True):
        lmList=[]
        if self.pred.multi_hand_landmarks:
            myHand=self.pred.multi_hand_landmarks[hand_num]
       
            for id , lm in enumerate(myHand.landmark):
                    
                h,w,c=frame.shape
                ax,ay=int(lm.x*w),int(lm.y*h)
                #print(id,ax,ay)
                lmList.append([id,ax,ay])
                if draw:
                    cv2.circle(frame,(ax,ay),5,(255,255,0),cv2.FILLED) 
        return lmList


def main():
    cap = cv2.VideoCapture(0)
    p_time=0
    detector=HandDetection()
    while True:
    
        ret, frame = cap.read()
        frame=detector.process_hands(frame)
        lmList=detector.findPosition(frame)
        if ret:
            cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()