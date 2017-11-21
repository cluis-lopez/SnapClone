'''
Created on Nov 20, 2017

@author: clopez
'''
import cv2

corona_orig = cv2.imread('corona.png', cv2.IMREAD_UNCHANGED)
corona_mask = cv2.imread('corona_mask.png', cv2.IMREAD_UNCHANGED)

def CreateCorona(imagen, x, y, w):
    
    ratio = w / 300.0
    y = y + 30 # to adjust the crown size 
    
    # la anchura de la corona en el fichero PNG son 230 pixels. ratio es la relacion de anchura entre la cara detectada y la corona
    
    corona = cv2.resize(corona_orig, None, fx=ratio, fy=ratio)
    mask = cv2.resize(corona_mask, None, fx=ratio, fy=ratio)

    cy, cx = corona.shape[0:2]
    
    if ((y-cy) < 0):
        return imagen
    
    roi = imagen[(y-cy):y, x:(x+cx)]
    mask_inv = cv2.bitwise_not(mask)
    roi = cv2.bitwise_and(roi, mask_inv)
    corona2 = cv2.bitwise_and(corona, mask)
    final = cv2.add (roi, corona2)
    imagen[(y-cy):y, x:(x+cx)] = final
    return imagen
    
if __name__ == '__main__':
    img = cv2.imread('test.jpg', cv2.IMREAD_UNCHANGED)
    main = CreateCorona(img, 300, 300 , 150)
    cv2.imshow('res', main)
    cv2.waitKey(0)
    cv2.destroyAllWindows()