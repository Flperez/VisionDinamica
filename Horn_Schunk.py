import time
from tools import calculate
import cv2,math
import numpy as np
from scipy.signal import convolve2d

def HScalcUV(Ix, Iy, It, Ix_2, Iy_2, f_lambda, u, v, N_iter):
    kernel = np.array(([1/12,1/6,1/12],
                       [1/6,0,1/6],
                       [1/12,1/6,1/12]))
    f_lambda = (f_lambda ** 2)*np.ones(Ix.shape)
    for i in range(N_iter):
        # Velocidad media
        uAvg = convolve2d(u,kernel,'same')
        vAvg = convolve2d(v,kernel,'same')

        # Calculo
        u1 = np.multiply(Ix,((np.multiply(Ix,uAvg))+(np.multiply(Iy,vAvg))+It))
        v1 = np.multiply(Iy,((np.multiply(Ix,uAvg))+(np.multiply(Iy,vAvg))+It))
        u2 = f_lambda+Ix_2+Iy_2

        u = uAvg - np.divide(u1,u2)
        v = vAvg - np.divide(v1,u2)


    return u,v


def Horn_Schunk(path_in,path_out, size):
    cap = cv2.VideoCapture(path_in)

    if path_out:
        visu = False
        fourcc = cv2.VideoWriter_fourcc('X','V', 'I','D')
        out_v = cv2.VideoWriter(path_out, fourcc, 33.0, (320, 240))
    else:
        visu = True

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
                u = np.zeros(actual_frame.shape)
                v = np.zeros(actual_frame.shape)
                flag = False
            else:
                start = time.clock()
                Ix, Iy, It, Ix_2, Iy_2 = calculate.derivateXYT(previous_frame, actual_frame, 'Horn_Schunk')
                u,v = HScalcUV(Ix, Iy, It, Ix_2, Iy_2, f_lambda, u, v, 50)
                print(time.clock() - start)

                # Drawing arrows
                for ix in range( actual_frame.shape[0] ):
                    for iy in range(actual_frame.shape[1] ):
                        if ix % size == 0 and iy % size == 0:
                            if u[ix,iy] is np.nan:
                                u[ix,iy]=0
                            if v[ix,iy] is np.nan:
                                v[ix,iy]=0
                            cv2.arrowedLine(out, (iy, ix), (iy + int(u[ix,iy]), ix + int(v[ix,iy])), (255, 0, 0))


                out = cv2.resize(out, (32 * 10, 24 * 10))
                if visu:
                    cv2.imshow("out", out)
                    cv2.waitKey(2)
                else:
                    out_v.write(out)

                # Save the frame
                previous_frame = actual_frame


