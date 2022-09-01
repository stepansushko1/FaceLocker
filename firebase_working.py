import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import os
import time
# Fetch the service account key JSON file contents
cred = credentials.Certificate('tokenFaceId.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://face-detection-bc85b-default-rtdb.firebaseio.com/',
    'storageBucket' : 'face-detection-bc85b.appspot.com'
})

bucket = storage.bucket()


def sendLogs():
    logs_folder = 'logs'
    while True:
        if len(os.listdir(logs_folder)) != 0:
            for file in os.listdir(logs_folder):
                while True:
                    try:
                        blob = bucket.blob("logs/" + f'{file}')
                        blob.upload_from_filename("logs\\"+file)
                        os.remove("logs\\"+ file)
                        break
                    except Exception:
                        continue

def sendPhotoTofirebase(filename):
    try:
        blob = bucket.blob("logs/" + f'{filename}')
        blob.upload_from_filename(filename)
        os.remove("logs\\"+ filename)
        return True
    except Exception:
        return False
    


def getTrainingData():

    iterDataBase = list(bucket.list_blobs())
    for file in iterDataBase:
        file = str(file)
        if file[41:53] == "TrainingData": # checking if it is from training data
            file = file.split(',')[1].split("/")[1] # take only id of image
            try:
                blob = bucket.blob("TrainingData/" + file)
                blob.download_to_filename("dataset_f\\" + file)
            except Exception:
                pass
    return len(iterDataBase)
        

def getAmountTrainingData():
    counter = 0
    iterDataBase = list(bucket.list_blobs())
    for file in iterDataBase:
        file = str(file)
        if file[41:53] == "TrainingData":
            counter += 1
    
    return counter



def lightPin():
    time.sleep(2)
    return

def closeDoor():

    blob = bucket.blob("OPEN/" + '0.txt')
    blob.download_to_filename('0.txt')
    f = open("0.txt", "r")
    value = f.read()
    f.close()
    if value == '1':
        blob.delete()
        f = open("0.txt", "w")
        f.write(0)
        print('pin light')
        lightPin()
        time.sleep(5)
        print('end light')
        blob.upload_from_filename('0.txt')
    time.sleep(1)
            

# closeDoor()

# def openDoor():
    
#     blob = bucket.blob( "OPEN/" + '0.txt')
#     blob.delete()
#     with open("open_door.txt", 'w'):
        
#     blob = bucket.blob("OPEN/" + '1.txt')
#     blob.upload_from_filename('1.txt')
    
#     time.sleep(10)
#     closeDoor()
    
#     return

# openDoor()


# closeDoor()


