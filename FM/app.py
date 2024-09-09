import cv2
import os
from flask import Flask,request,render_template
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import joblib
import json

#### Defining Flask App
app = Flask(__name__)

#### Initializing VideoCapture object to access WebCam
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


#### If these directories don't exist, create them
if not os.path.isdir('static'):
    os.makedirs('static')
if not os.path.isdir('static/faces'):
    os.makedirs('static/faces')

#### get a number of total registered users
def totalreg():
    return len(os.listdir('static/faces'))

#### extract the face from an image
def extract_faces(img):
    try:
        if img.shape!=(0,0,0):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face_points = face_detector.detectMultiScale(gray, 1.3, 5)
            return face_points
        else:
            return []
    except:
        return []
    
#### Identify face using ML model
def identify_face(facearray):
    model = joblib.load('static/face_recognition_model.pkl')
    recognized_name = model.predict(facearray)
    known_faces = os.listdir('static/faces')
    if recognized_name in known_faces:
        return recognized_name
    else:
        return ["Unknown"]


#### A function which trains the model on all the faces available in faces folder
def train_model():
    faces = []
    labels = []
    userlist = os.listdir('static/faces')
    for user in userlist:
        for imgname in os.listdir(f'static/faces/{user}'):
            img = cv2.imread(f'static/faces/{user}/{imgname}')
            resized_face = cv2.resize(img, (50, 50))
            faces.append(resized_face.ravel())
            labels.append(user)
    faces = np.array(faces)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(faces,labels)
    joblib.dump(knn,'static/face_recognition_model.pkl')


def deletefolder(duser):
    pics = os.listdir(duser)
    
    for i in pics:
        os.remove(duser+'/'+i)

    os.rmdir(duser)

def addemail(newusername,newuserid,newemail):
    try:
        with open('email_data.json', 'r') as f:
            data = json.load(f)
        data[newusername+'_'+str(newuserid)]=newemail
        json_filename = "email_data.json"
        with open(json_filename, "w") as json_file:
            json.dump(data, json_file)
    except:
        data = {
            newusername+'_'+str(newuserid): newemail,
            'Unknown': '20N31A05F8@gmail.com'
        }
        json_filename = "email_data.json"
        with open(json_filename, "w") as json_file:
            json.dump(data, json_file)


################## ROUTING FUNCTIONS #########################

#### Our main page
@app.route('/')
def home():  
    return render_template('home.html',totalreg=totalreg())  


#### This function will run when we click on Take Attendance Button
@app.route('/start',methods=['GET'])
def start():
    if 'face_recognition_model.pkl' not in os.listdir('static'):
        return render_template('home.html',totalreg=totalreg(),mess='There is no trained model in the static folder. Please add a new face to continue.') 

    ret = True
    cap = cv2.VideoCapture(0)
    while ret:
        ret,frame = cap.read()
        if len(extract_faces(frame))>0:
            (x,y,w,h) = extract_faces(frame)[0]
            cv2.rectangle(frame,(x, y), (x+w, y+h), (255, 0, 20), 2)
            face = cv2.resize(frame[y:y+h,x:x+w], (50, 50))
            identified_person = identify_face(face.reshape(1,-1))[0]
            cv2.putText(frame,f'{identified_person}',(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 20),2,cv2.LINE_AA)
        cv2.imshow('Face',frame)
        if cv2.waitKey(1)==27:
            break
    cap.release()
    cv2.destroyAllWindows() 
    return render_template('home.html',totalreg=totalreg()) 


#### This function will run when we add a new user
@app.route('/add',methods=['GET','POST'])
def add():
    newusername = request.form['newusername']
    newuserid = request.form['newuserid']
    newemail = request.form['newemail']
    addemail(newusername,newuserid,newemail)
    userimagefolder = 'static/faces/'+newusername+'_'+str(newuserid)
    if not os.path.isdir(userimagefolder):
        os.makedirs(userimagefolder)
    i,j = 0,0
    cap = cv2.VideoCapture(0)
    while 1:
        _,frame = cap.read()
        faces = extract_faces(frame)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x, y), (x+w, y+h), (255, 0, 20), 2)
            cv2.putText(frame,f'Images Captured: {i}/50',(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 20),2,cv2.LINE_AA)
            if j%10==0:
                name = newusername+'_'+str(i)+'.jpg'
                cv2.imwrite(userimagefolder+'/'+name,frame[y:y+h,x:x+w])
                i+=1
            j+=1
        if j==500:
            break
        cv2.imshow('Adding new User',frame)
        if cv2.waitKey(1)==27:
            break
    cap.release()
    cv2.destroyAllWindows()
    print('Training Model')
    train_model()
    return render_template('home.html',totalreg=totalreg()) 


#### Our main function which runs the Flask App
if __name__ == '__main__':
    app.run(debug=True)
