import numpy as np
import cv2

def limit(num, maximum,minimum=0):
  return max(min(num, maximum), minimum)

def nplimit(num,shape):
    return np.array([np.max([np.min([num[0],shape[0]]),0]),
                     np.max([np.min([num[1],shape[1]]),0])],dtype=np.int)

def npcountMat(Mat,ix,iy,inc):
    y_begin = iy-inc
    if iy-inc<0:
        y_begin = 0
    y_end = iy+inc
    if iy+inc>Mat.shape[0]:
        y_end = Mat.shape[0]

    x_begin = ix-inc
    if ix-inc<0:
        x_begin= 0
    x_end =ix+inc
    if iy+inc>Mat.shape[1]:
        x_end = Mat.shape[1]


    return np.count_nonzero(Mat[y_begin:y_end, x_begin:x_end])


def drawBB(image,xys,offset,color):
    if type(xys) == np.ndarray:
        xys = np.reshape(xys, (-1, 2))
        for xy in xys:
            x = xy[0]
            y = xy[1]
            cv2.rectangle(image,(x-offset,y-offset),(x+offset,y+offset),color)

def calcMask(image,lowerb,upperb):
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    return  cv2.inRange(hsv,lowerb,upperb)

def difusion(BB_states,ratio,shape):
    BB_difusion = np.zeros(BB_states.shape,dtype=np.int)
    for idx,BB in enumerate(BB_states):
        BB_difusion[idx,:]=nplimit(BB+np.random.randint(-ratio,ratio,(2,)),shape)
    return BB_difusion
