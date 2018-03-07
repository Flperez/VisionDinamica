import argparse

if __name__ == "__main__":
    # paso de argumentos
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True,
                    help="ruta a la carpeta de la secuencia de imagenes")
    ap.add_argument("--size", required=False,
                    help="region size",type=int,default=3)
    ap.add_argument("--method", required=True,
                    help="Lukas-kanade: Lukas_kanade\nHorn&Schunck: Horn_Schunck")

    args = vars(ap.parse_args())
    path_video = args['video']
    method = args['method']
    size = int(args['size'])

    if method == 'Lukas_kanade':
        import Lukas_Kanade
        Lukas_Kanade.Lukas_Kanade(path_video, size)
    elif method == 'Horn_Schunk':
        import Horn_Schunk
        Horn_Schunk.Horn_Schunk(path_video, size)
    else:
        print('No method found!\nType Lukas_kanade or Horn_Schunck')

