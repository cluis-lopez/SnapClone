'''
Created on Nov 19, 2017

@author: clopez
'''
import cv2

gafasOrig = cv2.imread('gafas.png', cv2.IMREAD_UNCHANGED)
gafasMask = cv2.imread('gafas_mask.png', cv2.IMREAD_UNCHANGED)

def CreateGafas(imagen, izq, der):

    izqx = izq[0]
    izqy = izq[1]
    derx = der[0]
    
    ratio = abs((derx - izqx)/270.0) # La anchura de las gafas en el fichero original en pixels
    izqx = int(izqx - (60 * ratio))
    izqy = int(izqy - (30 * ratio))
    
    # la distancia en las gafas del fichero png son 270 pixels, asi poues hay que ampliar o reducir las gafas 
    
    gafas = cv2.resize(gafasOrig, None, fx=ratio, fy=ratio)
    mask = cv2.resize(gafasMask, None, fx=ratio, fy=ratio)

    rows, cols = gafas.shape[0:2]

    roi = imagen[izqy:(izqy+rows), izqx:(izqx+cols)]
    mask_inv = cv2.bitwise_not(mask)
    roi = cv2.bitwise_and(roi, mask_inv)
    gafas2 = cv2.bitwise_and(gafas, mask)
    final = cv2.add (roi, gafas2)
    imagen[izqy:(izqy+rows), izqx:(izqx+cols)] = final
    return imagen
    
if __name__ == '__main__':
    img = cv2.imread('test.jpg', cv2.IMREAD_UNCHANGED)
    main = CreateGafas(img, (656,256), (758,266))
    cv2.imshow('res', main)
    cv2.waitKey(0)
    cv2.destroyAllWindows()