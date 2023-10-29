import cv2
import speechrecognition as sp
import os
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
import time

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://contactlessvending-default-rtdb.firebaseio.com/",
    'storageBucket':"contactlessvending.appspot.com"
})

cam = cv2.VideoCapture(0)
counter=0
# If image will detected without any error, 
# show result
UserPath="user_img"
image_filename ="rinku.png"
image_path = os.path.join(UserPath, image_filename)


while True:
    ret,frame=cam.read()
    # showing result, it take frame name and image 
    # output
    cv2.putText(frame,"stand straight for pic",(200,450),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,255),2)
    cv2.imshow("frame",frame)
    key=cv2.waitKey(1)
    if key==27:
        cam.release()
        cv2.destroyAllWindows() 
        break
    counter+=1
    print(counter)
    if counter==100:
        try:
            file_name=sp.speech()                 
            resize_img = cv2.resize(frame,(225,245),interpolation = cv2.INTER_AREA)
            cv2.imshow("resized img",resize_img)
            cv2.imwrite(os.path.join(UserPath,f"{file_name}.png"), resize_img)
            ref=db.reference('Students').update({
                file_name:
                        {
                            "name":file_name,
                            "Credits":69
                        }
                                                    })
            if os.path.isfile(image_path):
            # Upload the specified image to Firebase Storage
                time.sleep(1)
                image_filename =f'{file_name}'+".png"
                print(image_filename)
                image_path = os.path.join(UserPath, image_filename)
                image_filename=f'{UserPath}/{image_filename}'
                bucket = storage.bucket()
                blob = bucket.blob(image_filename)
                blob.upload_from_filename(image_path)
                print(image_path)
                print(f"Uploaded {image_filename} to Firebase Storage")
            else:
                print(f"The specified image file '{image_filename}' does not exist.")
            counter=0           
        except:
            break
            