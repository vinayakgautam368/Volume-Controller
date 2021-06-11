import numpy as np
import cv2
import mediapipe as mp 
import time

import handtrackingmodule as htm

ptime=0
ctime=0
cap=cv2.VideoCapture(0)
detector=htm.Hand()
    
while True:
    _,img=cap.read()
    img=detector.findhands(img)
    lmList=detector.findPosition(img)
    if len(lmList)!=0:
        print(lmList[4])
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,0),3)


    cv2.imshow("img",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
