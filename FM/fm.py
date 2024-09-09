
import numpy as np
import keras
import keras.backend as k
from tensorflow.keras.layers import Conv2D,MaxPooling2D,SpatialDropout2D,Flatten,Dropout,Dense
from tensorflow.keras.models import Sequential,load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import cv2
import datetime
import os
import joblib

mymodel=load_model('mymodel.h5')
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
def identify_face(facearray):
    model = joblib.load('static/face_recognition_model.pkl')
    recognized_name = model.predict(facearray)
    known_faces = os.listdir('static/faces')
    if recognized_name in known_faces:
        return recognized_name
    else:
        return ["Unknown"]

cap=cv2.VideoCapture(0)
face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
while cap.isOpened():
    _,img=cap.read()
    face=face_cascade.detectMultiScale(img,scaleFactor=1.1,minNeighbors=4)
    for(x,y,w,h) in face:
        face_img = img[y:y+h, x:x+w]
        cv2.imwrite('temp.jpg',face_img)
        test_image=load_img('temp.jpg',target_size=(150,150,3))
        test_image=img_to_array(test_image)
        test_image=np.expand_dims(test_image,axis=0)
        pred=mymodel.predict(test_image)[0][0]
        if pred==1:
            face_img = cv2.resize(face_img, (50, 50))
            person = identify_face(face_img.reshape(1,-1))[0]
            cv2.rectangle(img,(x, y), (x+w, y+h), (255, 0, 20), 2)
            cv2.putText(img,f'No Mask - {person}',(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 20),2,cv2.LINE_AA)
        else:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
            cv2.putText(img,'MASK',((x+w)//2,y+h+20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)

        datet=str(datetime.datetime.now())
        cv2.putText(img,datet,(400,450),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
          
    cv2.imshow('img',img)
    
    if cv2.waitKey(1)==ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
