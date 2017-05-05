import numpy as np
import cv2

mower_cascade = cv2.CascadeClassifier('haarcascade_mower.xml')

cap = cv2.VideoCapture('files/20170502_161726.mp4')

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mower = mower_cascade.detectMultiScale(gray, 20, 20)
    
    # add this
    for (x,y,w,h) in mower:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()