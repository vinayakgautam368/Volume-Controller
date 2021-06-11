import numpy as np
import cv2
import mediapipe as mp 
import time
import math
import pycaw
import handtrackingmodule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


wCam,hCam=640,480
ptime=0
ctime=0

cap=cv2.VideoCapture(0)
detector=htm.Hand(detectioncon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
vol_range=volume.GetVolumeRange()


vol_min=vol_range[0]
vol_max=vol_range[1]




if not cap.isOpened():
    print("cannot open camera")
    exit()

# a=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# print(a)
# a=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# print(a)

cap.set(3,wCam)
cap.set(4,hCam)

vol=400
vol_bar=400
vol_per=0
while True:
    _,img=cap.read()
    img=detector.findhands(img,draw=False)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        # print(lmList[4],lmList[8])   

        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2] 

        cx,cy=(x1+x2)//2,(y1+y2)//2

        length=math.sqrt((x2-x1)**2+(y2-y1)**2)
        # print(length)
        




        cv2.circle(img,(x1,y1),15,(255,255,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,255,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,255,255),2)
        cv2.circle(img,(cx,cy),15,(255,255,255),cv2.FILLED)

        if length<30:
            cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)

        vol=np.interp(length,[20,
        250],[vol_min,vol_max])
        vol_bar=np.interp(length,[20,250],[400,150])
        vol_per=np.interp(length,[20,250],[0,100])


        volume.SetMasterVolumeLevel(vol, None)
        print(length,vol)

    cv2.rectangle(img,(50,150),(85,400),(255,255,255),3)
    cv2.rectangle(img,(50,int(vol_bar)),(85,400),(255,0.0),cv2.FILLED)

    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime

    cv2.putText(img,f'FPS:{str(int(fps))}',(10,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
    cv2.putText(img,str(int(vol_per)),(60,450),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
    cv2.imshow("img",img)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
