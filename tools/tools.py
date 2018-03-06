import numpy as np
import cv2
def calcPinv(Ix_y, Ix_2, Iy_2, ix, iy, size):
    A = np.zeros((2, 2))
    inc = int(size / 2)
    A[0, 0] = np.sum(Ix_2[ix - inc:ix + inc, iy - inc:iy + inc])
    A[0, 1], A[1, 0] = np.sum(Ix_y[ix - inc:ix + inc, iy - inc:iy + inc])
    A[1, 1] = np.sum(Iy_2[ix - inc:ix + inc, iy - inc:iy + inc])

    return pinv(A)


from numpy.linalg import pinv


def derivateXYT(previous_frame, actual_frame):
    Ix = cv2.Sobel(actual_frame, cv2.CV_64F, 1, 0, ksize=5)
    Iy = cv2.Sobel(actual_frame, cv2.CV_64F, 0, 1, ksize=5)
    Ix_y = np.multiply(Ix, Iy)
    Ix_2 = np.multiply(Ix, Ix)
    Iy_2 = np.multiply(Iy, Iy)
    It = actual_frame - previous_frame
    Ix_t = np.multiply(Ix, It)
    Iy_t = np.multiply(Iy, It)

    return  Ix_y, Ix_2, Iy_2, Ix_t, Iy_t, It


def calcB(Ix_t, Iy_t, ix, iy, size):
    B = np.zeros([2, 1])
    inc = int(size / 2)
    B[0, 0] = - np.sum(Ix_t[ix - inc:ix + inc, iy - inc:iy + inc])
    B[1, 0] = - np.sum(Iy_t[ix - inc:ix + inc, iy - inc:iy + inc])
    return B


def calcUV(A, B):
    return np.multiply(A, B)


def ecUV(Ix_y, Ix_2, Iy_2, Ix_t, Iy_t, size, ix, iy):
    inc = int(size / 2)
    u1 = - np.sum(Iy_2[ix - inc:ix + inc, iy - inc:iy + inc]) * np.sum(Ix_t[ix - inc:ix + inc, iy - inc:iy + inc]) \
         + np.sum(Ix_y[ix - inc:ix + inc, iy - inc:iy + inc]) * np.sum(Iy_t[ix - inc:ix + inc, iy - inc:iy + inc])
    u2 = np.sum(Ix_2[ix - inc:ix + inc, iy - inc:iy + inc]) * np.sum(Iy_2[ix - inc:ix + inc, iy - inc:iy + inc]) \
         - np.sum(Ix_y[ix - inc:ix + inc, iy - inc:iy + inc]) * np.sum(Ix_y[ix - inc:ix + inc, iy - inc:iy + inc])
    u = u1 / u2
    v1 = np.sum(Ix_y[ix - inc:ix + inc, iy - inc:iy + inc]) * np.sum(Ix_t[ix - inc:ix + inc, iy - inc:iy + inc]) \
         - np.sum(Ix_2[ix - inc:ix + inc, iy - inc:iy + inc]) * np.sum(Iy_t[ix - inc:ix + inc, iy - inc:iy + inc])
    v2 = u2
    v = v1 / v2
    return np.vstack([u,v])




