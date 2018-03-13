import time
from tools import calculate
import cv2
import numpy as np


def HScalcUV(Ix, Iy, It, Ix_2, Iy_2, ix, iy, size, f_lambda, previous_u, previous_v):
    f_lambda = f_lambda ** 2
    previous_u = previous_u[ix,iy]
    previous_v = previous_v[ix,iy]
    inc = int(size / 2)
    u1 = calculate.npsumMat(Ix, ix, iy, inc) * previous_u + calculate.npsumMat(Iy, ix, iy, inc) * previous_v \
         + calculate.npsumMat(It, ix, iy, inc)
    u2 = f_lambda + calculate.npsumMat(Ix_2, ix, iy, inc) + calculate.npsumMat(Iy_2, ix, iy, inc)
    u = previous_u - calculate.npsumMat(Ix, ix, iy, inc) * (u1 / u2)
    v = previous_v - calculate.npsumMat(Iy, ix, iy, inc) * (u1 / u2)
    return np.vstack([u, v])


def Horn_Schunk(path, size):
    cap = cv2.VideoCapture(path)
    inc = int(size / 2)
    flag = True
    f_lambda = 0.1
    while (cap.isOpened()):
        ret, actual_frame = cap.read()
        # Gray
        actual_frame = cv2.cvtColor(actual_frame, cv2.COLOR_RGB2GRAY)
        actual_frame = cv2.resize(actual_frame, (32 * 5, 24 * 5))
        out = actual_frame.copy()
        out = cv2.cvtColor(out, cv2.COLOR_GRAY2RGB)

        if ret == True:
            if flag == True:
                previous_frame = actual_frame.copy()
                previous_u = np.zeros(actual_frame.shape)
                previous_v = np.zeros(actual_frame.shape)
                flag = False
            else:
                start = time.clock()
                Ix, Iy, It, Ix_2, Iy_2 = calculate.derivateXYT(previous_frame, actual_frame, 'Horn_Schunk')
                for ix in range(inc, actual_frame.shape[1] - inc):
                    for iy in range(inc, actual_frame.shape[0] - inc):
                        # print (ix,iy)

                        uv = HScalcUV(Ix, Iy, It, Ix_2, Iy_2, ix, iy, size, f_lambda, previous_u, previous_v)
                        # Drawing arrows
                        if ix % size == 0 and iy % size == 0:
                            cv2.arrowedLine(out, (iy, ix), (iy + uv[0], ix + uv[1]), (255, 0, 0))

                        previous_u[ix,iy]=uv[0]
                        previous_v[ix,iy]=uv[1]


                print(time.clock() - start)
                out = cv2.resize(out, (32 * 10, 24 * 10))

                cv2.imshow("out", out)
                cv2.waitKey(2)

                # Save the frame
                previous_frame = actual_frame
                previous_u = uv[0]
                previous_v = uv[1]
