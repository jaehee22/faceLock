import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
from datetime import datetime

if (not len(firebase_admin._apps)):
	cred = credentials.Certificate('./faceKey.json')
	firebase_admin.initialize_app(cred, {'databaseURL' : "https://facelock-39a53.firebaseio.com"})


for i in range(1,10):
        n = str(i)
        if os.path.exists("./Guestdata/Guest."+n+".jpg") == True:
                i+=1
        else:
		k = str(i)
		ref = db.reference('Guest/'+k)
                Guest_id = k+".jpg"
                break

now = datetime.today().strftime("%Y%m%d %H%M%S")

ref.update({
	 'time' : now,
	 'name' : Guest_id
})
