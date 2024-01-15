#Library Initialization
import cv2               #The main library
import numpy as np       #Arthimetic operations for matrices
import face_recognition  #For photos encoding
import os               #Operating System for database (obtaining names and addresses of database)
from datetime import datetime
from datetime import date

path = 'imagesAttendance'
images = []
total = []
myList = os.listdir(path)
#print (myList)

#photo files names and student numbers collecting
for cl in myList:
  curImg = cv2.imread(f'{path}/{cl}')
  images.append(curImg)
  total.append(os.path.splitext(cl)[0])
#print (classNames)
classNames = []
for cl in total:
  classNames.append(cl.split('-'))

#Photos Encoding
def findEncodings (images):
  encodeList = []
  for img in images :
    img =  cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(img)[0]
    encodeList.append(encode)
  return encodeList

#Marking Attendance Function

def markAttendance(name,number):
  with open('Attendance.csv','r+') as f:
    myDataList = f.readlines()
    nameList = []
    for line in myDataList:
      entry = line.split((','))
      nameList.append(entry[0])
    if name not in nameList:
      now = datetime.now()
      day = date.today()
      day = day.strftime("%B %d, %Y")
      dtstring = now.strftime(' %H:%M ')
      f.writelines(f'\n{name},{number},{day},{dtstring}')


encodeListKnown = findEncodings(images)

#Initializing webcam
cap = cv2.VideoCapture(0)
while True:
  success, img = cap.read()
  imgS = cv2.resize(img,(0,0),None,0.25,0.25)
  imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

  # face detection
  facesCurFrame = face_recognition.face_locations(imgS)
  encodesCurFrame = face_recognition.face_encodings(imgS)

  #face recognition
  for encodeFace,faceLoc in zip(encodesCurFrame, facesCurFrame):
    matches = face_recognition.compare_faces(encodeListKnown,encodeFace)      # logic 1 or 0
    faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
    matchIndex = np.argmin(faceDis)

    #Draw rectangle around face
    #Write the name and student number under the rectangle
    if matches[matchIndex]:
      name = classNames[matchIndex][0].upper()
      number = ''
      if(len(classNames[matchIndex]) > 1):
        number = classNames[matchIndex][1]
      y1, x2, y2, x1 = faceLoc
      y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
      cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
      #cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0))
      cv2.putText(img, name, (x1, y2+14), cv2.FONT_HERSHEY_DUPLEX, .5, (160, 0, 195), 2)
      cv2.putText(img, number, (x1, y2 + 28), cv2.FONT_HERSHEY_DUPLEX, .5, (160, 0, 195), 2)
      markAttendance(name,number)

  cv2.imshow('Webcam',img)
  cv2.waitKey(1)
