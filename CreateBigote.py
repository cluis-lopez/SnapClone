'''
Created on Nov 21, 2017

@author: clopez
'''
import cv2

gafasOrig = cv2.imread('bigote.png', cv2.IMREAD_UNCHANGED)
gafasMask = cv2.imread('bigote_mask.png', cv2.IMREAD_UNCHANGED)

def CreateBigote(imagen, izq, der):

    izqx = izq[0]
    izqy = izq[1]
    derx = der[0]
    
    ratio = abs((derx - izqx)/300.0) # La anchura del bigote en el fichero original en pixels
    izqx = int(izqx - (110 * ratio))
    izqy = int(izqy + (280 * ratio))
    
    # la distancia en las gafas del fichero png son 270 pixels, asi poues hay que ampliar o reducir las gafas 
    
    bigote = cv2.resize(gafasOrig, None, fx=ratio, fy=ratio)
    mask = cv2.resize(gafasMask, None, fx=ratio, fy=ratio)

    rows, cols = bigote.shape[0:2]

    roi = imagen[izqy:(izqy+rows), izqx:(izqx+cols)]
    mask_inv = cv2.bitwise_not(mask)
    roi = cv2.bitwise_and(roi, mask_inv)
    bigote2 = cv2.bitwise_and(bigote, mask)
    final = cv2.add (roi, bigote2)
    imagen[izqy:(izqy+rows), izqx:(izqx+cols)] = final
    return imagen
    
if __name__ == '__main__':
    img = cv2.imread('test.jpg', cv2.IMREAD_UNCHANGED)
    main = CreateBigote(img, (656,256), (758,266))
    cv2.imshow('res', main)
    cv2.waitKey(0)
    cv2.destroyAllWindows()