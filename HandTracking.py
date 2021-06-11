#In the hand detection we get 21 landmarks point but the position of landmarks given in ratio so we want to multiply with size of screen.
import numpy as np
import cv2
import mediapipe as mp


import time
cap=cv2.VideoCapture(0)
mphands=mp.solutions.hands
hands=mphands.Hands()
mpDraw=mp.solutions.drawing_utils

ptime=0
ctime=0

while True:
    _,img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            for id,lm in enumerate(handlms.landmark):
                #print(id,lm)
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h) 
                if id==4:
                    cv2.circle(img,(cx,cy),15,(255,255,255),cv2.FILLED)
            mpDraw.draw_landmarks(img,handlms,mphands.HAND_CONNECTIONS)
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,0),3)

    cv2.imshow("img",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()










