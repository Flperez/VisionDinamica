import cv2


def getfondo(path,nframe):
    cap = cv2.VideoCapture(path)
    cap.set(1, nframe)
    ret, frame = cap.read()
    return frame

def enunciado1(path):
    threshold = 75
    cap = cv2.VideoCapture(path)
    fondo = getfondo(path_in,(180*length)/448)
    fondo_gray = cv2.cvtColor(src=fondo,code=cv2.COLOR_RGB2GRAY)
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frame_gray = cv2.cvtColor(src=frame, code=cv2.COLOR_RGB2GRAY)
            result = frame_gray - fondo_gray
            mask = cv2.inRange(frame_gray, threshold, 255)
            cv2.imshow("resultado", result)
            cv2.imshow("mask", mask)
            cv2.imshow("fondo", fondo_gray)
            cv2.imshow("frame_gray", frame_gray)
            cv2.waitKey(33)


    return 1

def enunciado2(path):
    cap = cv2.VideoCapture(path)
    flag = True
    while (cap.isOpened()):
        ret, frame = cap.read()

        if ret == True:
            frame_gray = cv2.cvtColor(src=frame, code=cv2.COLOR_RGB2GRAY)
            if flag == True
                frame_ant = frame_gray

            dif = frame_gray - frame_ant
            frame_ant = frame_gray.copy()



    return 1




path_in="vid1.avi"
 #cargamos video de entrada
cap = cv2.VideoCapture(path_in)
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))




##################### Enunciado 1 ####################
#enunciado1(path_in)
##################### Enunciado 2 ####################
enunciado2(path_in)





