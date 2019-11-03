# Imports
import numpy as np
import cv2

# Capture video from webcam
cap = cv2.VideoCapture(0)  # Change 0 to 1 if you are using external webcam

count = 0

while True:
        # read the frame from video
	ret, frame = cap.read()

	# if noting is returned, then break
	if ret == False:
		break

        # wait for a keypress event
	wait = cv2.waitKey(10)

	# if 's' is pressed
	if wait == ord("s"):
                # save the frame
		cv2.imwrite("video_frame/frame"+str(count)+".jpg", frame)     # save frame as JPEG file
		count+=1

	# if q is pressed
	if wait == ord("q"):
                # end the process
		break

	# Text displayed on screen displaying the number of images saved
	cv2.putText(frame,"saved_frame = "+str(count),(30,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
	cv2.imshow('frame',frame)

# stop the webcam recording
cap.release()
cv2.destroyAllWindows()
