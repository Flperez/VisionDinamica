import numpy as np
import cv2
from numba import jit
import math
@jit
def calcPinv(Ix_y, Ix_2, Iy_2, ix, iy, size):
    A = np.matrix(((0, 0),(0,0)))
    inc = int(size / 2)
    A[0, 0] = npsumMat(Ix_2,ix,iy,inc)
    A[0, 1] =  npsumMat(Ix_y,ix,iy,inc)
    A[1, 0] = A[0, 1]
    A[1, 1] = npsumMat(Iy_2,ix,iy,inc)

    return pinv(A)


from numpy.linalg import pinv

@jit
def derivateXYT(previous_frame, actual_frame,method):
    previous_frame = cv2.GaussianBlur(previous_frame,(5,5),0.2)
    actual_frame_frame = cv2.GaussianBlur(actual_frame,(5,5),0.2)


    dx_k0 = cv2.Sobel(previous_frame, cv2.CV_64F, 1, 0, ksize=3)
    dy_k0 = cv2.Sobel(previous_frame, cv2.CV_64F, 0, 1, ksize=3)
    dx_k1 = cv2.Sobel(actual_frame, cv2.CV_64F, 1, 0, ksize=3)
    dy_k1 = cv2.Sobel(actual_frame, cv2.CV_64F, 0, 1, ksize=3)

    Ix = 0.5*(dx_k0+dx_k1)
    Iy = 0.5 *(dy_k0 + dy_k1)


    Ix_2 = np.multiply(Ix, Ix)
    Iy_2 = np.multiply(Iy, Iy)
    It = actual_frame - previous_frame
    if method == 'Lukas_kanade':

        Ix_t = np.multiply(Ix, It)
        Iy_t = np.multiply(Iy, It)
        Ix_y = np.multiply(Ix, Iy)

        return  Ix_y, Ix_2, Iy_2, Ix_t, Iy_t, It
    if method == 'Horn_Schunk':
        return Ix,Iy,It, Ix_2, Iy_2

@jit
def calcB(Ix_t, Iy_t, ix, iy, size):
    B = np.matrix(((0), (0))).T
    inc = int(size / 2)


    B[0, 0] = - npsumMat(Ix_t,ix,iy,inc)
    B[1, 0] = - npsumMat(Iy_t,ix,iy,inc)
    return B

def calcUV(A, B):
    return A*B

def npsumMat(Mat,ix,iy,inc):
    return np.sum(Mat[ix - inc:ix + inc, iy - inc:iy + inc])

def med(Mat,ix,iy,inc):
    return np.mean(Mat[ix - inc:ix + inc, iy - inc:iy + inc])

@jit
def ecUV(Ix_y, Ix_2, Iy_2, Ix_t, Iy_t, size, ix, iy):
    inc = int(size / 2)
    u1 = - npsumMat(Iy_2,ix,iy,inc) * npsumMat(Ix_t,ix,iy,inc) + npsumMat(Ix_y,ix,iy,inc) * npsumMat(Iy_t,ix,iy,inc)
    u2 = npsumMat(Ix_2,ix,iy,inc) * npsumMat(Iy_2,ix,iy,inc) - npsumMat(Ix_y,ix,iy,inc) * npsumMat(Ix_y,ix,iy,inc)

    u= u1 / u2
    v1 = npsumMat(Ix_y,ix,iy,inc) * npsumMat(Ix_t,ix,iy,inc) - npsumMat(Ix_2,ix,iy,inc) * npsumMat(Iy_t,ix,iy,inc)

    v2 = u2
    v = v1 / v2
    if math.isnan(u):
        u = 0
    if math.isnan(v):
        v = 0

    return np.vstack([u,v])




