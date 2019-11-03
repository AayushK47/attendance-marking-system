import os
import json
import cv2

def detect_faces(gray, frame):
    face_cascade = cv2.CascadeClassifier(os.path.join(os.getcwd(), 'attendance_marking_system', 'models', 'haarcascade_frontalface_default.xml'))
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)
    return frame

def extract_faces(gray, frame):
    face_cascade = cv2.CascadeClassifier(os.path.join(os.getcwd(), 'attendance_marking_system', 'models', 'haarcascade_frontalface_default.xml'))
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    extracted_faces = []
    face_dims = []
    for (x, y, w, h) in faces:
        face_dims.append((x,y,w,h))
        extracted_faces.append(frame[y:y+h,x:x+w])
    
    return face_dims, extracted_faces