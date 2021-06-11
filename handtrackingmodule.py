#In the hand detection we get 21 landmarks point but the position of landmarks given in ratio so we want to multiply with size of screen.
import numpy as np
import cv2
import mediapipe as mp

class Hand():
    def __init__(self,mode=False,MaxHands=2,detectioncon=0.5,trackcon=0.5):
        self.mode=mode
        self.MaxHands=MaxHands
        self.detectioncon=detectioncon
        self.trackcon=trackcon

        self.mphands=mp.solutions.hands
        self.hands=self.mphands.Hands(self.mode,self.MaxHands,self.detectioncon,self.trackcon)
        self.mpDraw=mp.solutions.drawing_utils

    def findhands(self,img,draw=True):
            imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            self.results=self.hands.process(imgRGB)
            # print(results.multi_hand_landmarks)
            if self.results.multi_hand_landmarks:
                for handlms in self.results.multi_hand_landmarks:
                    if draw:
                        self.mpDraw.draw_landmarks(img,handlms,self.mphands.HAND_CONNECTIONS)
            return img

    def findPosition(self,img,handNo=0,draw=True):
        lmList=[]
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):  
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h) 
                lmList.append([id,cx,cy])
                
                # if id==4:
                if draw:    
                    cv2.circle(img,(cx,cy),10,(255,255,255),cv2.FILLED)
        return lmList



        
         

import time


def main():
    ptime=0
    ctime=0
    cap=cv2.VideoCapture(0)
    detector=Hand()
    
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



if __name__ == "__main__":
    main() 






