'''
Created on Nov 19, 2017

@author: clopez
'''

import cv2
import CreateGafas
import CreateCorona

CROWN = 1
GLASS = 1

cap = cv2.VideoCapture(0)
cap.set(3 , 640*2)
cap.set(4 , 480*2)
faceCascPath = 'haarcascade_frontalface_default.xml'
eyeCascPath = 'haarcascade_eye.xml'
faceCascade = cv2.CascadeClassifier(faceCascPath)
eye_cascade = cv2.CascadeClassifier(eyeCascPath)

keepglasses = 0 # frames without eye detection while we keep the glasses on
oldeyes = None # just to initialize the variable

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    gray = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA) # Make pict 1/2 the size
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY) # Make pict B&W
    
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)

    print "Found {0} faces!".format(len(faces))
    
    if (CROWN==1 and type(faces) != 'tuple'): # check if we've foond any face
        if (len(faces)>0):
            for (x ,y, w, h) in faces:
                frame = CreateCorona.CreateCorona(frame, x*2, y*2, w*2)
    
    if GLASS == 1:        
        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi, 1.3, 5)
            #for (ex,ey,ew,eh) in eyes:
            #    cv2.rectangle(roi,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)
            #cv2.imshow('eyes', roi)
            if len(eyes) == 2:
                print "Eyes recognized"
                eyes = eyes[eyes[:,0].argsort()] # Arrange the "eyes" list to have the leftmost first
                for i in eyes:
                    i[0] = i[0] + x
                    i[1] = i[1] + y
                eyes = [i * 2 for i in eyes]
                oldeyes = eyes
                keepglasses = 20 # restore the counter
                frame = CreateGafas.CreateGafas(frame, eyes[0], eyes[1])
            else: # 2 eyes not recognized
                keepglasses = keepglasses -1
                if (keepglasses >0):
                    frame = CreateGafas.CreateGafas(frame, oldeyes[0], oldeyes[1])
    
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()