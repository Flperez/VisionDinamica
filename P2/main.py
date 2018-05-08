import cv2
import numpy as np
import f_condensation
import argparse


offset = 5
Ntop = 3
bajos = np.array([49,50,50])
altos = np.array([80, 255, 255])


def condensation(mask,BB_previous,Flag_BB,N=10):
    if  Flag_BB==False: #caso de no haber encontrado nada
        #offset not constante
        # 1.- Inicializacion
        w,h = mask.shape
        y = np.random.randint(0+offset, w+offset, size=(N,1))
        x = np.random.randint(0+offset, h+offset, size=(N,1))
        BB_previous = np.concatenate((x, y), 1)
        Flag_BB = True


    # 2.- Evaluacion
    pesos = []
    for x,y in BB_previous:
        pesos.append(f_condensation.npcountMat(mask,x,y,offset))

    # pesos = [f_condensation.npcountMat(mask,x,y,offset) for x,y in BB_previous]
    if sum(pesos) != 0:
        pesos_norm = np.multiply(1/sum(pesos),pesos)
        pesos_acum = np.cumsum(pesos_norm)


        # 3.- Estimacion
        xy_best = BB_previous[np.argmax(pesos),:]

        # 4.- Seleccion
        Nselec = N
        states = []
        for i in range(Nselec):
            random_seed = np.random.rand(1)
            id = np.where(pesos_acum > random_seed)[0][0]
            states.append(id)

        BB_states = np.asarray([BB_previous[i,:] for i in states])

        # 5.- Difusion
        ratio = 10
        BB_difusion = f_condensation.difusion(BB_states,ratio,mask.shape)
        return xy_best,BB_difusion,True
    else:
        return None,None,False





def main(path):
    cap = cv2.VideoCapture(path)
    BB_difusion = None
    flag = False
    Flag_BB = False
    while (cap.isOpened()):
        ret, frame = cap.read()


        if ret == True:
            frame = cv2.resize(frame,None,fx=0.1,fy=0.1)
            if flag == False:
                flag = True
            else:
                out = frame.copy()
                mask = f_condensation.calcMask(frame,bajos,altos)
                f_condensation.drawBB(out,BB_difusion,offset,(255,0,0))

                xy_best,BB_difusion,Flag_BB = condensation(mask,BB_difusion,Flag_BB,50)
                f_condensation.drawBB(out,xy_best,offset,(0,0,255))
                #out = cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB)

                fx = 5
                cv2.imshow("video",cv2.resize(out,None,fx=fx,fy=fx))
                cv2.waitKey(100)
        else:
            break





if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True,
                    help="ruta al video de entrada",default="videos/ball.mp4")
    args = vars(ap.parse_args())
    path_video = args['video']
    main(path_video)




