import tensorflow as tf
import os
import sys
import cv2

print(sys.argv[1])
print(sys.argv[2])
model = tf.keras.models.load_model(os.path.join(os.getcwd(), 'attendance_marking_system', 'models', 'model.h5'), custom_objects={"tf": tf})

img1 = cv2.imread(sys.argv[1])
img2 = cv2.imread(sys.argv[2])

img1 = cv2.resize(img1, (160,160))
img2 = cv2.resize(img2, (160,160))

img1 = img1.astype('float')/255
img2 = img2.astype('float')/255

img1 = [img1]
img2 = [img2]
pred = model.predict([img1, img2])

print(pred)
label = 1 if pred > 0.5 else 0

with open('results.txt', 'w') as f:
    f.write(str(label))