import cv2
import os
import firebase_admin
import numpy as np
from PIL import Image
import pyrebase
import time
from datetime import datetime
import json
import os
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('./faceKey.json')
firebase_admin.initialize_app(cred, {'databaseURL' : "https://facelock-39a53.firebaseio.com"})

face_id = 0

cap = cv2.VideoCapture(-1)
cap.set(3,640)
cap.set(4,480)
face_detector = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

#비어있는 번호 찾기
for i in range(1,10):
	n = str(i)
	if os.path.exists("./UserData/User."+n+".30.jpg") == True:
		i+=1
	else:
		face_id = i
		break
k = str(face_id)

ref = db.reference('User/'+k)
ref.update({
        'name' : k
})


print(" [INFO] Initializing fzce capture. Look the camera and wait ..")

count = 0

#카메라에 나온 사람의 얼굴을 찾아서 프레임 씌우기 
while True:
	ret, img = cap.read()
	img = cv2.flip(img, -1)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_detector.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		count += 1
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]

		cv2.imwrite("UserData/User." + str(face_id) + '.' +str(count) + ".jpg", gray[y:y+h,x:x+w])
		cv2.imshow('image',img)

	k = cv2.waitKey(100) & 0xff
	if k == 27:
		break
	elif count >= 30:
		break

print(" [INFO] Exiting Program and cleanup stuff")

cap.release()
cv2.destroyAllWindows()


#얼굴이미지가 저장될 경로 지정하기
path = 'UserData'
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")

#이미지에 대한 정보, 얼굴 훈련시키기
def getImagesAndLabels(path):
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
        faceSamples=[]
        ids = []
        for imagePath in imagePaths:
                PIL_img = Image.open(imagePath).convert('L')
                img_numpy = np.array(PIL_img,'uint8')
                id = int(os.path.split(imagePath)[-1].split(".")[1])
                faces = detector.detectMultiScale(img_numpy)
                for (x,y,w,h) in faces:
                        faceSamples.append(img_numpy[y:y+h,x:x+w])
                        ids.append(id)
        return faceSamples,ids
print (" [INFO] Training faces. It will take a few seconds. Wait ...")
faces,ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))
# Save the model into trainer/trainer.yml
recognizer.write('trainer/trainer.yml')
# Print the number of faces trained and end program
print(" [INFO] {0} faces trained. Exiting program".format(len(np.unique(ids))))


config ={
        "apiKey":"faceKey.json",
        "authDomain":"facelock-39a53.firebaseapp.com",
        "databaseURL":"http://facelock-39a53.firebaseio.com/",
        "storageBucket":"facelock-39a53.appspot.com"
}

#Firebase에 사용자 번호 저장하기 & Firebase Storage에 얼굴 하나 뽑아서 
ID = str(face_id)
firebase = pyrebase.initialize_app(config)
uploadfile = "UserData/User."+ID+".15.jpg"
s = os.path.splitext(uploadfile)[1]
filename = ID+".jpg"

storage = firebase.storage()

storage.child("UserList/"+filename).put(uploadfile)
fileUrl = storage.child("UserList/"+filename).get_url(1)
print (fileUrl)



