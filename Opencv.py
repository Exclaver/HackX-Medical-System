import cv2
from simple_facerec import SimpleFacerec
import time
import os
import OpenCVModule as htm
import gtts
import playsound


import speechrecognition as sp
#import controller as cnt
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://hackx-medical-system-default-rtdb.firebaseio.com/",
    'storageBucket':"contactlessvending.appspot.com"
})


sfr=SimpleFacerec()
sfr.load_encoding_images("images/")

file_name=""
register=0
authloop=-1
cntr=1
bucket=storage.bucket()
mainCounter=0
selectionSpeed=11
wCam,hCam=267,200
cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0
name=0
resize_img=0
modePositions=[(1136,196),(1000,384),(1136,581),(1050,384)]
counter=0
counterPause=0
selectionList=[-1,-1,-1]
AuthenticationList=[0]
ImgBackground=0
modeType=4
selections=-1
ImgStudent=[]

detector=htm.handDetector(detectionCon=0.75)
tipIds=[4,8,12,16,20]

#importing all moodes to list
folderPathModes="Resources/Modes"
listImgModesPath=os.listdir(folderPathModes)
listImgModes=[]
for imgModePath in listImgModesPath:
     listImgModes.append(cv2.imread(os.path.join(folderPathModes,imgModePath)))




def Output():
    global pTime
    global ImgBackground
    global cntr
    
    
    if authloop==1:
     if name=="Devansh":
          cv2.putText(frame,"Welcome Devansh",(200,450),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)
     elif name=="Unknown":
          cv2.putText(frame,"Unknown Face",(200,450),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)
     else:
          cv2.putText(frame,"No Face Detected",(200,450),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)
    
    if AuthenticationList==[3] or AuthenticationList==[4]:
        ImgBackground=cv2.imread("Resources\Background.jpg")
        ImgBackground[139:139+240,50:50+320 ]=frame
        ImgBackground[0:720,847:1280]=listImgModes[1]
        ImgBackground[0:720,413:846]=listImgModes[2]
        
    else:
        ImgBackground=cv2.imread("Resources\Background.jpg")
        ImgBackground[139:139+240,50:50+320]=frame
        ImgBackground[0:720,847:1280]=listImgModes[modeType]
    
   
    # if mainCounter!=0 and name!="Unknown" and authloop==1 :
    # #  cv2.putText(ImgBackground,str("Credits: "+str(studentInfo['Credits'])),(980,450),cv2.FONT_HERSHEY_COMPLEX ,1,(0,0,0),2)
    # #  cv2.putText(ImgBackground,str("Name: "+ str(studentInfo['name'])),(890,500),cv2.FONT_HERSHEY_COMPLEX ,1,(0,0,0),2)
    #  cv2.putText(ImgBackground,"Show 4 to Confirm Your Identity",(865,550),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)
    #  cv2.putText(ImgBackground,"Show 2 to register as new user",(865,620),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)


    #  ImgBackground[150:150+245,953:953+225]=ImgStudent            #student image from databse
    # if authloop==0 and selectionList[0]!=-1 and selectionList[1]!=-1 and selectionList[2]!=-1:
    #      cv2.putText(ImgBackground,str("credits: "+ str(studentInfo['Credits'])),(980,550),cv2.FONT_HERSHEY_COMPLEX ,1,(0,0,0),2)
    #      print("oolah")
     #     if cntr==1 and selectionList[0]==1 and selectionList[1]==2 and selectionList[2]==3:
     #       cntr=2                              #SERVO CODE
     #       cnt.led(selectionList[1])
     #     elif cntr==1 and selectionList[0]==2 and selectionList[1]==2 and selectionList[2]==2:
     #         cntr=2                              #SERVO CODE
     #         cnt.led1(selectionList[0]+5)     # pin 6,7,8
           
    

    ###############login page animation
    if selections==2 and authloop==1:
         cv2.ellipse(ImgBackground,(1050,650),(100,0),180,0,counter*4.6,(255,0,0),15)
    elif selections==4:
        cv2.ellipse(ImgBackground,(1050,580),(100,0),180,0,counter*4.6,(0,0,255),15)
    elif selections==-1:
        pass                          #to remove dot at position -1
    elif authloop==0:                  #elipse for selections
        cv2.ellipse(ImgBackground,modePositions[selections-1],(103,103),0,0,counter*selectionSpeed,(0,153,0),15)
    #iconlist


    if AuthenticationList[0]==4 :
         cv2.putText(ImgBackground,patentName,(995,250),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)
         cv2.putText(ImgBackground,patentStatus,(995,150),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)
         cv2.putText(ImgBackground,patentDisease,(995,350),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)
         cv2.putText(ImgBackground,patentage,(995,450),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)

         cv2.putText(ImgBackground,doctorAge,(675,480),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)
         cv2.putText(ImgBackground,doctorHospital,(675,380),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)
         cv2.putText(ImgBackground,doctorName,(675,280),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)
         cv2.putText(ImgBackground,doctorPosition,(675,180),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)
         cv2.putText(ImgBackground,doctorSpecialization,(675,80),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)

       
         text_to_speak = f"{patentName} age {patentage} has {patentDisease} and the status is {patentStatus}"
         sound=gtts.gTTS(text_to_speak,lang='en')
         sound.save("hey.mp3")
         playsound.playsound("hey.mp3")
    

    cv2.imshow("Background",ImgBackground)
    key=cv2.waitKey(1)
    if key==27:
        cap.release()
        cv2.destroyAllWindows()  
    

def SelectUser():
    global ImgBackground
    global patentInfo
    
    ImgBackground=cv2.imread("Resources\White.jpg")
    
    if(AuthenticationList[0]==0):
        cv2.putText(ImgBackground,"Show 3 finger for doctors portal",(433,200),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(255,0,0),2)
        cv2.putText(ImgBackground,"Show 2 finger for Patients portal",(433,400),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(255,0,0),2)
    if selections==3 and AuthenticationList==[0]:
         cv2.ellipse(ImgBackground,(603,250),(100,0),180,0,counter*4.6,(255,0,0),15)
         
         
    
    ImgBackground[0:720,847:1280]=listImgModes[modeType]
    ImgBackground[0:720,0:433]=listImgModes[modeType]
    ImgBackground[439:439+240,470:470+320]=frame



#authentication
while AuthenticationList==[0]:
    global patentage
    global patentDisease
    global patentName
    global patentInfo
    global patentStatus
    success,frame=cap.read()
    cv2.imshow("Background",ImgBackground)

    key=cv2.waitKey(1)
    if key==27:
        cap.release()
        cv2.destroyAllWindows()  
        AuthenticationList=[1]
    success,frame=cap.read()
    frame=detector.findHands(frame)
    lmList=detector.findPosition(frame,draw=False)
                # print(lmList)             
    if len(lmList)!=0 and counterPause==0 and modeType<5:
        fingers=[]
        #thumb
        if lmList[tipIds[0]][1]>lmList[tipIds[0]-1][1]:
                fingers.append(1)
        else:
                fingers.append(0)
        #fingers
        for id in range(1,5):

            if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        totalFingers=fingers.count(1)
        print(fingers) 

    #  if fingers==[0,1,0,0,0]:
    #       if selections!=1:
    #          counter=1
    #       selections=1
        if fingers==[0,1,1,1,0]:
            if selections!=3:
                counter=1
            selections=3    
        elif fingers==[0,1,1,0,0]:
            if selections!=2:
                counter=1
            selections=2                                      
        else:
            selections=-1
            counter=0
        
        #print(selections)
        if counter>0:
            counter+=1
            #  print(counter)                     
            if counter*selectionSpeed>360:
                AuthenticationList[0]=selections                         
                counter=0
                selections=-1
                counterPause=1
                #  print(modeType)
    #pause function  
    if counterPause>0:
        counterPause+=1
        if counterPause>40:
            counterPause=0
    
    SelectUser()
    

while True:
    while AuthenticationList[0]==3  :
        Output()
        authloop=1
        ret,frame=cap.read()
        face_location,face_names=sfr.detect_known_faces(frame)
        for face_loc,name in zip(face_location,face_names):              
            print(name)
            name1=name    
            if mainCounter==0:
                    mainCounter=1
        if mainCounter!=0 and name!="Unknown":
            if mainCounter==1:
                # #Data from Database
                # studentInfo=db.reference(f'Students/{name}').get()
                # print(studentInfo) 
                # #Image from database
                # blob=bucket.get_blob(f'images/{name}.jpg')
                # array=np.frombuffer(blob.download_as_string(),np.uint8)
                # ImgStudent1=cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
                # ImgStudent=cv2.resize(ImgStudent1,(225,245),interpolation = cv2.INTER_AREA)
                AuthenticationList=[4]               
               #update credits
            #    if selectionList==[]
            #    ref=db.reference(f'Students/{name}')
            #    studentInfo['Credits']+=10  
            #    ref.child('Credits').set(studentInfo['Credits'])
        
        
        if name=="Unknown":
            print("Unknown face")
        while name=="Devansh" and AuthenticationList[0]!=4 and AuthenticationList[0]!=2 :
                
                
                success,frame=cap.read()
                frame=detector.findHands(frame)
                lmList=detector.findPosition(frame,draw=False)
                            # print(lmList)             
                if len(lmList)!=0 and counterPause==0 and modeType<5:
                    fingers=[]
                    #thumb
                    if lmList[tipIds[0]][1]>lmList[tipIds[0]-1][1]:
                            fingers.append(1)
                    else:
                            fingers.append(0)
                    #fingers
                    for id in range(1,5):

                        if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    # print(fingers)
                    totalFingers=fingers.count(1)
                    print(fingers) 

                #  if fingers==[0,1,0,0,0]:
                #       if selections!=1:
                #          counter=1
                #       selections=1
                    if fingers==[0,1,1,1,1]:
                        if selections!=4:
                            counter=1
                        selections=4      
                    elif fingers==[0,1,1,0,0]:
                        if selections!=2:
                            counter=1
                        selections=2                                      
                    else:
                        selections=-1
                        counter=0
                    
                    #print(selections)
                    if counter>0:
                        counter+=1
                        #  print(counter)                     
                        if counter*selectionSpeed>360:
                            AuthenticationList[0]=selections                         
                            counter=0
                            selections=-1
                            counterPause=1
                            #  print(modeType)
                #pause function  
                if counterPause>0:
                    counterPause+=1
                    if counterPause>40:
                        counterPause=0
                print(AuthenticationList)
                
            
                Output()
        if name!="Devansh" and name!="Unknown":
            print("No Face Detected")




        ###########################################


        

    # while AuthenticationList[0]==2:
    #     authloop=2
    #     cam = cv2.VideoCapture(0)
    #     counter=0
    #     # If image will detected without any error, 
    #     # show result
    #     UserPath="user_img"
    #     image_filename ="devansh.png"
    #     image_path = os.path.join(UserPath, image_filename)


    #     while AuthenticationList[0]==2 :
    #         ret,frame=cam.read()
    #         # showing result, it take frame name and image 
    #         # output
    #         cv2.putText(frame,"stand straight for pic",(200,450),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,255),2)
            
    #         key=cv2.waitKey(1)
    #         if key==27:
    #             cam.release()
    #             cv2.destroyAllWindows() 
    #             break
    #         counter+=1
    #         print(counter)
    #         Output()
    #         if counter==100:
    #             try:
    #                 file_name=sp.speech()                 
    #                 resize_img = cv2.resize(frame,(225,245),interpolation = cv2.INTER_AREA)
                    
    #                 cv2.imwrite(os.path.join(UserPath,f"{file_name}.png"), resize_img)
    #                 ref=db.reference('Students').update({
    #                     file_name:
    #                             {
    #                                 "name":file_name,
    #                                 "Credits":69
    #                             }
    #                                                         })
    #                 if os.path.isfile(image_path):
    #                 # Upload the specified image to Firebase Storage
    #                     time.sleep(1)
    #                     image_filename =f'{file_name}'+".png"
    #                     print(image_filename)
    #                     image_path = os.path.join(UserPath, image_filename)
    #                     image_filename=f'{UserPath}/{image_filename}'
    #                     bucket = storage.bucket()
    #                     blob = bucket.blob(image_filename)
    #                     blob.upload_from_filename(image_path)
    #                     print(image_path)
    #                     print(f"Uploaded {image_filename} to Firebase Storage")
    #                     time.sleep(1)
    #                     AuthenticationList[0]=-1
                        
                        
    #                 else:
    #                     print(f"The specified image file '{image_filename}' does not exist.")
    #                 counter=0       
    #             except:
    #                 break
                



    #################################################






            
                    
    #maincode
    mainCounter=0
    counter=0
    counterPause=0
    ImgBackground=0
    modeType=0
    selections=-1
    mainCounter=0
    creditCounter=0
    speak=1

    while AuthenticationList[0]==4:
        global Uid
        
        authloop=0
        ret,frame=cap.read()
        face_location,face_names=sfr.detect_known_faces(frame)
        for face_loc,name in zip(face_location,face_names):              
            print(name)
            name1=name     
           
        if speak==1:
            text="Speak Unique Identification of the patient"
            sounds=gtts.gTTS(text,lang='en')
            sounds.save("ask.mp3")
            playsound.playsound("ask.mp3")
            speak=2

        
        try:
            Uid = sp.speech()
            first_run = False  # Set the flag to False to exit the loop
        except Exception as e:
            print("An error occurred:", e)
        
        
        patentInfo=db.reference(f'Medical/patent/{Uid}').get()
        patentDisease=db.reference(f'Medical/patent/{Uid}/Disease').get()
        patentName=db.reference(f'Medical/patent/{Uid}/name').get()
        patentStatus=db.reference(f'Medical/patent/{Uid}/Status').get()
        patentage=db.reference(f'Medical/patent/{Uid}/age').get()

        doctorInfo=db.reference(f'Medical/Doctors/{Uid}').get()
        doctorName=db.reference(f'Medical/Doctors/{Uid}/name').get()
        doctorPosition=db.reference(f'Medical/Doctors/{Uid}/Position').get()
        doctorSpecialization=db.reference(f'Medical/Doctors/{Uid}/specialization').get()
        doctorAge=db.reference(f'Medical/Doctors/{Uid}/Age').get()
        doctorHospital=db.reference(f'Medical/Doctors/{Uid}/Hospital').get()
        print(patentName)
        if Uid == "update":
            text2 = "Speak updated patient name"
            sounds2 = gtts.gTTS(text2, lang='en')
            sounds2.save("askpat.mp3")
            playsound.playsound("askpat.mp3")

            name3 = sp.speech()
            
            # Initialize patentInfo as an empty dictionary
            patentInfo = {}
            
            ref = db.reference(f'Medical/patent/{Uid}')
            patentInfo['patentName'] = name3
            ref.child('patentName').set(patentInfo['patentName'])
            break
            

        
        Output()
       

        
        # if name=="Unknown":
        #     print("Unknown face")

        # while name=="Devansh":            
        #         if selectionList[0]!=-1 and selectionList[1]!=-1 and selectionList[2]!=-1 and creditCounter<1:
        #             ref=db.reference(f'Students/{name}')
        #             studentInfo['Credits']-=10  
        #             ref.child('Credits').set(studentInfo['Credits'])
        #             creditCounter=1
        #         success,frame=cap.read()
        #         frame=detector.findHands(frame)
        #         lmList=detector.findPosition(frame,draw=False)
                                
        #         if len(lmList)!=0 and counterPause==0 and modeType<3:
        #             fingers=[]

        #             #thumb
        #             if lmList[tipIds[0]][1]>lmList[tipIds[0]-1][1]:
        #                     fingers.append(1)
        #             else:
        #                     fingers.append(0)


        #             #fingers
        #             for id in range(1,5):

        #                 if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
        #                     fingers.append(1)
        #                 else:
        #                     fingers.append(0)
        #             # print(fingers)
        #             totalFingers=fingers.count(1)
        #             print(fingers) 

        #             if fingers==[0,1,0,0,0]:
        #                 if selections!=1:
        #                     counter=1
        #                 selections=1
        #             elif fingers==[0,1,1,0,0]:
        #                 if selections!=2:
        #                     counter=1
        #                 selections=2
        #             elif fingers==[0,1,1,1,0]:
        #                 if selections!=3:
        #                     counter=1
        #                 selections=3
        #             else:
        #                 selections=-1
        #                 counter=0
        #             if counter>0:
        #                 counter+=1
        #                 #  print(counter)
        #                 cv2.ellipse(ImgBackground,modePositions[selections-1],(103,103),0,0,counter*selectionSpeed,(0,156,0),15)

        #                 if counter*selectionSpeed>360:
        #                     selectionList[modeType]=selections
        #                     modeType+=1
        #                     counter=0
        #                     selections=-1
        #                     counterPause=1
        #                     #  print(modeType)
        #         #pause function  
        #         if counterPause>0:
        #             counterPause+=1
        #             if counterPause>40:
        #                 counterPause=0
                
                
        #         print(selectionList)
        #         Output()

                
        # if name!="Devansh" and name!="Unknown":
        #     print("No Face Detected")
    
    file_name=""
    register=0
    authloop=-1
    cntr=1
    mainCounter=0
    cap=cv2.VideoCapture(0)
    name=0
    resize_img=0
    counter=0
    counterPause=0
    selectionList=[-1,-1,-1]
    AuthenticationList=[-1]
    ImgBackground=0
    modeType=4
    selections=-1
    ImgStudent=[]