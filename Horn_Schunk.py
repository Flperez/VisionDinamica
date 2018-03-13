import time
from tools import calculate
import cv2,math
import numpy as np


def HScalcUV(Ix, Iy, It, Ix_2, Iy_2, ix, iy, size, f_lambda, previous_u, previous_v, N_iter):
    inc = int(size / 2)
    p_u = calculate.med(previous_u,ix, ix,inc)
    p_v = calculate.med(previous_v,ix, ix,inc)

    for i in range(N_iter):
        f_lambda = f_lambda ** 2

        u1 = calculate.npsumMat(Ix, ix, iy, inc) * p_u + calculate.npsumMat(Iy, ix, iy, inc) * p_v \
             + calculate.npsumMat(It, ix, iy, inc)
        u2 = f_lambda + calculate.npsumMat(Ix_2, ix, iy, inc) + calculate.npsumMat(Iy_2, ix, iy, inc)
        u = p_u - calculate.npsumMat(Ix, ix, iy, inc) * (u1 / u2)
        v = p_v - calculate.npsumMat(Iy, ix, iy, inc) * (u1 / u2)
        p_u=u
        p_v=v


    return np.vstack([u, v])


def Horn_Schunk(path_in,path_out, size):
    cap = cv2.VideoCapture(path_in)
    if path_out:
        visu = True
        fourcc = cv2.VideoWriter_fourcc('X','V', 'I','D')
        out_v = cv2.VideoWriter(path_out, fourcc, 33.0, (320, 240))
    else:
        visu = False

    inc = int(size / 2)
    flag = True
    f_lambda = 20
    threshold = 50
    while (cap.isOpened()):
        ret, actual_frame = cap.read()
        # Gray
        actual_frame = cv2.cvtColor(actual_frame, cv2.COLOR_RGB2GRAY)
        actual_frame = cv2.resize(actual_frame, (32 * 10, 24 * 10))
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

                        uv = HScalcUV(Ix, Iy, It, Ix_2, Iy_2, iy, ix, size, f_lambda, previous_u, previous_v, 50)
                        if math.isnan(uv[0]):
                            uv[0] = 0
                        if math.isnan(uv[1]):
                            uv[1] = 0
                        if uv[0] > threshold:
                            uv[0] = threshold
                        if uv[1] > threshold:
                            uv[1] = threshold

                        if uv[0] < -threshold:
                            uv[0] = -threshold
                        if uv[1] < -threshold:
                            uv[1] = -threshold

                        # Drawing arrows
                        if ix % size == 0 and iy % size == 0:
                            cv2.arrowedLine(out, (ix, iy), (ix + uv[1], iy + uv[0]), (255, 0, 0))

                        previous_u[iy,ix]=uv[0]
                        previous_v[iy,ix]=uv[1]


                print(time.clock() - start)
                out = cv2.resize(out, (32 * 10, 24 * 10))
                if visu:
                    cv2.imshow("out", out)
                    cv2.waitKey(2)
                else:
                    out_v.write(out)

                # Save the frame
                previous_frame = actual_frame

