import time
from tools import calculate
import cv2


def calcUV(Ix_y, Ix_2, Iy_2, Ix_t, Iy_t, ix, iy, size, method='pseudo'):
    if method == 'pseudo':

        A = calculate.calcPinv(Ix_y, Ix_2, Iy_2, ix, iy, size)
        B = calculate.calcB(Ix_t, Iy_t, ix, iy, size)
        uv = calculate.calcUV(A, B)
    else:
        uv = calculate.ecUV(Ix_y, Ix_2, Iy_2, Ix_t, Iy_t, size, ix, iy)
    return uv


def Lukas_Kanade(path, size):
    cap = cv2.VideoCapture(path)
    inc = int(size / 2)
    flag = True
    while (cap.isOpened()):
        ret, actual_frame = cap.read()
        # Gray
        actual_frame = cv2.cvtColor(actual_frame,cv2.COLOR_RGB2GRAY)
        actual_frame = cv2.resize(actual_frame,(32*5,24*5))
        out = actual_frame.copy()
        out = cv2.cvtColor(out, cv2.COLOR_GRAY2RGB)

        if ret == True:
            if flag == True:
                previous_frame = actual_frame.copy()
                flag = False
            else:
                start = time.clock()
                Ix_y, Ix_2, Iy_2, Ix_t, Iy_t, It = calculate.derivateXYT(previous_frame, actual_frame, 'Lukas_kanade')
                for ix in range(inc, actual_frame.shape[1] - inc):
                    for iy in range(inc, actual_frame.shape[0] - inc):
                        # print (ix,iy)

                        uv = calcUV(Ix_y, Ix_2, Iy_2, Ix_t, Iy_t, ix, iy, size, method='pseudo')
                        # print (uv)
                        #Drawing arrows
                        if ix%size==0 and iy%size==0:
                            cv2.arrowedLine(out,(iy,ix),(iy+uv[0],ix+uv[1]),(255,0,0))

                print (time.clock() - start)
                out = cv2.resize(out,(32*10,24*10))

                cv2.imshow("out",out)
                cv2.waitKey(2)

                #Save the frame
                previous_frame = actual_frame