import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('./faceKey.json')
firebase_admin.initialize_app(cred, {'databaseURL' : "https://facelock-39a53.firebaseio.com"})

face_id = 0

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

print k
