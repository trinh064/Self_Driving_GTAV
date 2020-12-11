import numpy as np
from PIL import ImageGrab,ImageOps
import cv2
import time
import pyautogui
from directkeys import PressKey,ReleaseKey, W, A, S, D
from scipy import signal
import math

th=250
nline=0
sob=0
linesP=[]
mask=np.zeros([639,800],dtype=np.uint8)
mask[40:480,200:600]=1
#mask[:,:]=1

#homography matrix
h=np.array([[-1.43194983e-01, -2.30825191e+00,  6.02821770e+02],
 [ 3.68087605e-01, -6.58908753e+00,  1.77396527e+03],
 [ 3.06823125e-04, -5.00885467e-03 , 1.00000000e+00]])

def analyze(line):
    p1=np.array([line[0],line[1]])
    p2=np.array([line[2],line[3]])
    dv=p1-p2
    length=np.sqrt(dv[0]**2+dv[1]**2)
    angle=np.arctan(dv[0]/dv[1])

    return [length,angle]
def makedecision(lines):
    list=[]
    for i in range(0, len(lines)):
        l = linesP[i][0]
        list+=[analyze(l)]
    #print(list)
    list=np.array(list)
    totallength=np.sum(list[:,0])
    vote=np.sum(list[:,0]*list[:,1])/totallength-0.012
    print(vote)
    decision=['w',None]
    if vote >0.055:
        decision=['a',A]
    if vote <0.03:
        decision=['d',D]
    return decision


def process_img(src):
    global th,nline,sob,linesP
    #convert to bird view perspective
    birdview=cv2.warpPerspective(src,h, (src.shape[1],src.shape[0] ) )
    #Gaussian blur
    birdview = signal.convolve2d(birdview,np.array([ [1,4,7,4 ,1],[4,16,26,16, 4],[7,26,41,26,7],[4,16,26,16, 4],[1,4,7,4,1] ])/115, mode='same' )
    #Sober operation
    dx = signal.convolve2d(birdview,np.array([[-1 ,-2, -1],[0 ,0, 0],[1, 2, 1]]), mode='same' ) # horizontal derivative
    dy = signal.convolve2d( birdview,np.array([[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]]), mode='same' )  # v derivative
    sum = np.sqrt(dx**2+dy**2).astype(np.uint8) # magnitude

    #cut a part of the warp
    sum=(sum*mask)


    ret,sob= cv2.threshold(sum,th,255,cv2.THRESH_BINARY)
    linesP = cv2.HoughLinesP(sob, 1, np.pi / 180, 50, None, 50, 10)
    if linesP is not None:
        nline=len(linesP)
    else:
        nline=0
    count=0;

    while(nline<20) or (nline>30):
        if (nline<20):
             th-=2
        if (nline>30):
             th+=2
        ret,sob= cv2.threshold(sum,th,255,cv2.THRESH_BINARY)
        linesP = cv2.HoughLinesP(sob, 1, np.pi / 180, 50, None, 50, 10)
        if linesP is not None:
            nline=len(linesP)
        else:
            nline=0
        count+=1
        if(count>100):
            break

    processed_img=sob

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(processed_img, (l[0], l[1]), (l[2], l[3]), (155,100,55), 3, cv2.LINE_AA)
    return processed_img,linesP

def main():

    while True:
        screen =  ImageGrab.grab(bbox=(0,1,800,640))
        screen = np.array(ImageOps.grayscale(screen))
        new_screen ,lines= process_img(screen)
        decision=makedecision(lines)
        print(decision[0])
        PressKey(W)
        if decision[1]!=None:
            PressKey(decision[1])
            time.sleep(0.12)
            ReleaseKey(decision[1])
        else:
            time.sleep(0.12)
        time.sleep(0.3)
        ReleaseKey(W)
        time.sleep(0.1)
        cv2.imshow('window', new_screen)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindoaaws()
            breakwd


main()
