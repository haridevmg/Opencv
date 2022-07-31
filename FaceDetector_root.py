# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 07:59:03 2022

@author: gilesh.mp
"""

import cv2
import mediapipe as mp
import time

cap=cv2.VideoCapture(0)
mpFace=mp.solutions.face_detection
faces=mpFace.FaceDetection()
mpDraw=mp.solutions.drawing_utils

while True:
    ret,img=cap.read()
    results=faces.process(img)
    
    if results.detections:
        for id,det in enumerate(results.detections):
            mpDraw.draw_detection(img, det,)
    if ret:
        cv2.imshow("Video",img)
    if 0xFF and ord('q')  == cv2.waitKey(1):
        break
    
cap.release()
cv2.destroyAllWindows()