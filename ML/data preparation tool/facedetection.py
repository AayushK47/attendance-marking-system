'''
Filename: facedetection.py
description: extracts the faces from the images and saves them in a directory
libraries used: numpy, cv2 and os
author: Kapil Nema
'''

# Imports
import numpy as np
import cv2
import os

# load the facial features
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Label for the data
label = input('Type in the label to be assigned: ')

count = 1
dir = "./video_frame"

# Iterate over all the images in the directory
for img_file in os.listdir(dir):
	# read the image as a matrix
	img = cv2.imread(os.path.join(dir, img_file))
	# convert the image to grayscale
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# Detect the face using facial features from haar-cascade
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	# extract the region of face(s)
	for (x,y,w,h) in (faces):
		img_save = img[y:y+h,x:x+w]
		img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]

                # save the image
		cv2.imwrite(f'saved_faces/{label}_' + str(count) + ".jpg",img_save)
		count += 1

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
