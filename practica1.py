from tools import tools
import argparse
import cv2
import numpy as np

def calcUV(Ix_y, Ix_2, Iy_2, Ix_t, Iy_t, ix, iy, size, method='pseudo'):
    if method == 'pseudo':
        A = tools.calcPinv(Ix_y, Ix_2, Iy_2, ix, iy, size)
        B = tools.calcB(Ix_t, Iy_t, ix, iy, size)
        uv = tools.calcUV(A, B)
    else:
        uv = tools.ecUV(Ix_y, Ix_2, Iy_2, Ix_t, Iy_t, size, ix, iy)
    return uv


def Lukas_Kanade(path, size):
    cap = cv2.VideoCapture(path)
    inc = int(size / 2)
    flag = True
    while (cap.isOpened()):
        ret, actual_frame = cap.read()
        # Gray
        actual_frame = cv2.cvtColor(actual_frame,cv2.COLOR_RGB2GRAY)
        out = actual_frame.copy()

        if ret == True:
            if flag == True:
                previous_frame = actual_frame.copy()
                flag = False
            else:
                Ix_y, Ix_2, Iy_2, Ix_t, Iy_t, It = tools.derivateXYT(previous_frame, actual_frame)
                for ix in range(inc, actual_frame.shape[1] - inc):
                    for iy in range(inc, actual_frame.shape[0] - inc):
                        uv = calcUV(Ix_y, Ix_2, Iy_2, Ix_t, Iy_t, ix, iy, size, method='pseudo')

                    #Drawing arrows
                    if ix%size==0 and iy%size==0:
                        cv2.arrowedLine(out,(ix,iy),(ix+uv[0],iy+uv[1]))


                #Save the frame
                previous_frame = actual_frame



if __name__ == "__main__":
    # paso de argumentos
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True,
                    help="ruta a la carpeta de la secuencia de imagenes")

    args = vars(ap.parse_args())
    path_video = args['video']
    size = 3
    Lukas_Kanade(path_video, size)
