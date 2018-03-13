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
    ap.add_argument("--method", required=True,
                    help="Lukas-kanade: Lukas_kanade\nHorn&Schunck: Horn_Schunck")

    args = vars(ap.parse_args())
    path_video = args['video']
    method = args['method']
    path_out = args['out']
    size = int(args['size'])

    if method == 'Lukas_Kanade':
        import Lukas_Kanade
        Lukas_Kanade.Lukas_Kanade(path_video, path_out,size)
    elif method == 'Horn_Schunk':
        import Horn_Schunk
        Horn_Schunk.Horn_Schunk(path_video,path_out, size)
    else:
        print('No method found!\nType Lukas_kanade or Horn_Schunck')

