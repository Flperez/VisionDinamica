import argparse

if __name__ == "__main__":
    # paso de argumentos
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True,
                    help="ruta al video de entrada")
    ap.add_argument("--out", required=False,
                    help="ruta al video de salida")
    ap.add_argument("--size", required=False,
                    help="region size",type=int,default=3)
    ap.add_argument("--N_iter", required=False,
                    help="numero de iteraciones", type=int, default=10)
    ap.add_argument("--lambda", required=False,
                    help="lambda de Horn&Schunk", type=int, default=25)
    ap.add_argument("--method", required=True,
                    help="Lukas-kanade: Lukas_kanade\nHorn&Schunck: Horn_Schunck")
    ap.add_argument("--operation", required=False,default='pseudo',
                    help="pseudo or ecuation")


    args = vars(ap.parse_args())
    path_video = args['video']
    method = args['method']
    operation = args['operation']
    path_out = args['out']
    size = int(args['size'])
    N_iter = int(args['N_iter'])
    f_lambda = int(args['lambda'])

    if method == 'Lukas_Kanade':
        import Lukas_Kanade
        Lukas_Kanade.Lukas_Kanade(path_video, path_out,size,operation)
    elif method == 'Horn_Schunk':
        import Horn_Schunk
        Horn_Schunk.Horn_Schunk(path_video,path_out, size,N_iter,f_lambda)
    else:
        print('No method found!\nType Lukas_kanade or Horn_Schunck')

