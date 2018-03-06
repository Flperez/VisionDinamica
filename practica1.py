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
        if ret == True:
            if flag == True:
                previous_frame = actual_frame.copy()
                flag = False
            else:
                Ix_y, Ix_2, Iy_2, Ix_t, Iy_t, It = tools.derivateXYT(previous_frame, actual_frame)
                uv = np.zeros(actual_frame.shape)
                for ix in range(inc, actual_frame.shape[1] - inc):
                    for iy in range(inc, actual_frame.shape[0] - inc):
                        uv[ix,iy] = calcUV(Ix_y, Ix_2, Iy_2, Ix_t, Iy_t, ix, iy, size, method='pseudo')
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
