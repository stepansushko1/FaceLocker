import cv2
import numpy as np
from PIL import Image
import os
from firebase_working import getAmountTrainingData

# Path for face image database
path = 'dataset_f'
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");


def getImagesAndLabels(path):
    # getTrainingData()
    faceSamples=[]
    ids = []
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    counter = 0
    idDictionary = dict()
    
    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')
        
        id = (os.path.split(imagePath)[-1].split("_")[0])
        
        if id not in idDictionary:
            idDictionary[id] = counter
            counter += 1
        
        id = idDictionary[id]
        
        faces = detector.detectMultiScale(img_numpy)

        for (x,y,widht,height) in faces:
            faceSamples.append(img_numpy[y:y+height,x:x+widht])
            ids.append(id)

    return faceSamples,ids

faces, ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))

recognizer.save('trainer/trainer.yml')

print("TRAINED")