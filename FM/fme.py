
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
import json
import time
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from threading import Thread

def identify_face(facearray):
    model = joblib.load('static/face_recognition_model.pkl')
    recognized_name = model.predict(facearray)
    known_faces = os.listdir('static/faces')
    if recognized_name in known_faces:
        return recognized_name
    else:
        return ["Unknown"]

def get_email(person):
    with open('email_data.json', 'r') as f:
        data = json.load(f)
    return data[person]

def check_notify(person,face):
    try:
        with open('time_data.json', 'r') as f:
            data = json.load(f)
        if time.time() - data[person] > 30:
                thread = Thread(target=notify, args=(get_email(person),face))
                thread.start()
                with open('time_data.json', 'w') as f:
                    data[person]=time.time()
                    json.dump(data,f)
                    
    except:
        with open('time_data.json', 'w') as f:
            data = {
                person: time.time(),
                "Unknown": time.time()
            }
            json.dump(data,f)

def notify(email,face):
    try:
        password='komfrjekvkotukqd'
        subject = 'Face Mask Detection Alert'
        if email == '20N31A05F8@gmail.com':
            body='An unknown person has been detected without mask. Please take necessary action.'
        else:
            body = 'You were detected without a mask. Please wear a mask for safety.'
        message = MIMEMultipart()
        message['From'] = '20N31A05F8@gmail.com'
        message['To'] = email
        message['Subject'] = subject
        text = MIMEText(body)
        message.attach(text)
        image_part = MIMEImage(cv2.imencode('.jpg', face)[1].tobytes(), name="realtime_face.jpg")
        message.attach(image_part)
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login('20N31A05F8@gmail.com', password)
        smtp_server.sendmail('20N31A05F8@gmail.com', email, message.as_string())
        smtp_server.quit()
        print(f"Email sent to {email}")
    except Exception as e:
        print(f"Email not sent to {email}: {e}")
        

cap=cv2.VideoCapture(0)
mymodel=load_model('mymodel.h5')
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
            check_notify(person,face_img)
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
