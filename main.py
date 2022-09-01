# This is main module
import urllib.request
import cv2
import numpy as np
import os 
from datetime import datetime
import time
import threading
import face_training
import multiprocessing
import firebase_admin
import firebase_working
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
names = ['Stepan', 'Vadym', 'None'] 
font = cv2.FONT_HERSHEY_SIMPLEX
VALIDATOR = 50
#iniciate id counter
id = 0


def check_connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False


# names related to ids: example ==> Marcelo: id=1,  etc

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

# Face Recocnition 

def main():
    check = 0
    while True:
        # curr = firebase_working.getAmountTrainingData()
        # if check != curr:
        #     print("Paralel Training Starts!")
        #     multiprocessing.Process(target = face_training.getImagesAndLabels, args=("dataset_f",)).start()
        #     check = curr
        checker = []    
        
        # if check_connect() == True:
            
        ret, img = cam.read()

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5, minSize = (int(minW), int(minH)),)
        
        if (len(faces) != 0):


            for i in range(VALIDATOR):
                
                ret, img = cam.read()
                gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5, minSize = (int(minW), int(minH)),)


                for(x,y,width,height) in faces:
                    

                    cv2.rectangle(img, (x,y), (x+width,y+height), (0,255,0), 2)

                    id, confidence = recognizer.predict(gray[y:y+height,x:x+width])

                    # Check if confidence is less them 100 ==> "0" is perfect match 
                    if (confidence < 75):
                        id = names[id]
                        confidence = "  {0}%".format(round(100 - confidence))
                    else:
                        id = "unknown"
                        confidence = "  {0}%".format(round(100 - confidence))
                        
                    checker.append(id)
                    cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                    cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  

                    now = datetime.now()
                    current_time = now.strftime("%H-%M-%S")
                    print(i)
                    if i == VALIDATOR-1:
                        person= max(set(checker), key = checker.count)
                        output = str(person) +"-"+ current_time + ".jpg"
                        cv2.imwrite("logs\\"+ output,img)
                        
                        # check connect

                        if check_connect() == True:
                            firebase_working.sendPhotoTofirebase(output)
                                     
                        # if person is in Users, the door will be opened for 30 seconds
                        if person != "unknown":
                            firebase_working.lightPin()
                            pass
                
                cv2.imshow('camera',img) 

                k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
                if k == 27:
                    break
            # th1.join()
        time.sleep(2)

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    jobs = []
    th1 = threading.Thread(target = main)   
    th2 = threading.Thread(target = firebase_working.sendLogs)
    jobs.append(th1)
    jobs.append(th2)
    
    for i in jobs:
        i.start()

































''' 1. If from app: 
        Light up the Pin on raspberry if the signal from open_door is 1,
        wait for 30 seconds, turn off, send file with 0 back on Firebase
       If from recognition:
        Light up the raspberry pin for 30 sec, turn off
        
        * Done
      
    2. Check in thread if there is new training data. If it is, then
       download all images from train data -> retrain cnn -> feed in main
    
    3. If error happens, while uploading Logs into Firebase, wait until
       internet connection will be again, send image to firebase.
      
'''