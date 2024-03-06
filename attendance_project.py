import cv2 as cv
import numpy as np
import face_recognition
import os
from datetime import datetime
import pyttsx3



def main():
    path="imageattendance"
    images=[]
    classnames=[]
    list=os.listdir(path)
    print(list)
    for cls in list:
        curimg=cv.imread(f'{path}/{cls}')
        images.append(curimg)
        classnames.append(os.path.splitext(cls)[0])
    print(classnames)

    def talk(nomen): 
        lan=pyttsx3.init()
        voices=lan.getProperty('voices')
        lan.setProperty('voice',voices[1].id)
        lan.say(nomen)
        lan.runAndWait()

    def findencoding(images):
        encodelist=[]
        for img in images:
            img=cv.cvtColor(img,cv.COLOR_BGR2RGB)
            encode=face_recognition.face_encodings(img)[0]
            encodelist.append(encode)
        return encodelist


    def markattendance(name):
        with open('attendance.csv','r+') as f:
            mydata = f.readlines()
            namelist =[]
            for line in mydata:
                entry = line.split(',')
                namelist.append(entry[0])
            if name not in namelist:
                now = datetime.now()
                dtstring = now.strftime('%H,%M,%S')
                f.writelines(f'\n{name},{dtstring}')



    encodelistknown=findencoding(images)
    print("encoding complete")

    cap = cv.VideoCapture(0)

    while True:
        success, img= cap.read()
        imgs=cv.resize(img,(0,0),None,0.25,0.25)
        gray=cv.cvtColor(imgs,cv.COLOR_BGR2RGB)
        # cv.namedWindow("SLFC ATTENDANCE SYSTEM",cv.WINDOW_NORMAL)
        # cv.resizeWindow("SLFC ATTENDANCE SYSTEM", 1400,700)


        facecurframe= face_recognition.face_locations(gray)
        encodecurframe= face_recognition.face_encodings(gray,facecurframe)

        def call():
            for encodeface,faceloc in zip(encodecurframe,facecurframe):
                matches= face_recognition.compare_faces(encodelistknown,encodeface)
                facedis= face_recognition.face_distance(encodelistknown,encodeface)
                print(facedis)
                print(matches)
                matchindex= np.argmin(facedis)


                if facedis[11] < 0.50 and matches[matchindex]:
                    name = classnames[matchindex].upper()
                    print(name)
                    y1,x2,y2,x1 = faceloc
                    y1, x2, y2, x1 =y1*4,x2*4,y2*4,x1*4
                    cv.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv.FILLED)
                    cv.putText(img,name,(x1+6,y2-6),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    markattendance(name)
                    talk(f'{name},{",thank you,you are welcome"}')
                else:
                    # name = classnames[matchindex].upper()
                    # print(name)
                    y1,x2,y2,x1 = faceloc
                    y1, x2, y2, x1 =y1*4,x2*4,y2*4,x1*4
                    cv.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
                    cv.rectangle(img,(x1,y2-35),(x2,y2),(0,0,255),cv.FILLED)
                    cv.putText(img,'unknown user',(x1+6,y2-6),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    talk('sorry,you are not recognised. Please try again')

                
        call()
        cv.imshow("SLFC ATTENDANCE SYSTEM",img)
        cv.waitKey(1)
    

if __name__=='__main__':
    main()
