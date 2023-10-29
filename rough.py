if len(lmList)!=0 and counterPause==0 and modeType<3:
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

                    if fingers==[0,1,0,0,0]:
                        if selections!=1:
                            counter=1
                        selections=1
                    elif fingers==[0,1,1,0,0]:
                        if selections!=2:
                            counter=1
                        selections=2
                    elif fingers==[0,1,1,1,0]:
                        if selections!=3:
                            counter=1
                        selections=3
                    else:
                        selections=-1
                        counter=0
                    if counter>0:
                        counter+=1
                        #  print(counter)
                        cv2.ellipse(ImgBackground,modePositions[selections-1],(103,103),0,0,counter*selectionSpeed,(0,156,0),15)

                        if counter*selectionSpeed>360:
                            selectionList[modeType]=selections
                            modeType+=1
                            counter=0
                            selections=-1
                            counterPause=1
                            #  print(modeType)
                #pause function  
                if counterPause>0:
                    counterPause+=1
                    if counterPause>40:
                        counterPause=0