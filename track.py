import cv2
import sys
import time
import os
import random
import math

#screensize = 1080 1920
scaling = 1

# MIL, BOOSTING, KCF, TLD, MEDIANFLOW or GOTURN
tracker = cv2.Tracker_create("BOOSTING")
video  = cv2.VideoCapture('files/20170502_161726.mp4')
frameRate = video.get(5)

timestr = time.strftime('%Y%m%d-%H%M%S')
outfilename = 'files/output-' + timestr + '.avi'
outfoldername = 'files/' + timestr
os.mkdir(outfoldername)
cwd = os.getcwd()

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter(outfilename, fourcc, 20.0, (480,270))
postxtfilename = outfoldername + '/' + timestr + '.lst'
negtxtfilename = outfoldername + '/neg' + timestr + '.lst'
postxt = open(postxtfilename, 'w+')
negtxt = open(negtxtfilename, 'w+')
# Exit if video not opened.
if not video.isOpened():
    print "Could not open video"
    sys.exit()
 
# Read first frame.
ok, frame = video.read()
if not ok:
    print 'Cannot read video file'
    sys.exit()

#bbox = (int(760*scaling), int(295*scaling), int(100*scaling), int(100*scaling))
bbox = (765, 300, 100, 100)
#bbox = cv2.selectROI(frame, False)

ok = tracker.init(frame, bbox)
 
imagecount = 1

while True:
    while (video.isOpened()):
        frameId = video.get(1)
        # Read a new frame
        ok, frame = video.read()
        if (ok != True):
            break
        if (frameId % math.floor(frameRate) == 0):
            frame = cv2.resize(frame,(0,0),fx=scaling,fy=scaling)
            height, width, channels = frame.shape 
            #gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
            if not ok:
                break

            # Update tracker
            ok, bbox = tracker.update(frame)
        
            # Draw bounding box
            if ok:
        
                imagename = str(imagecount) + '.jpg'
                imagepath = cwd + '/' + outfoldername + '/' + imagename
                cv2.imwrite(imagepath, frame)
                postxt.write(imagepath + ' 1 ' + str(int(bbox[0])) + ' ' + str(int(bbox[1])) + ' ' + str(int(bbox[2])) + ' ' + str(int(bbox[3])) + '\n')
                font = cv2.FONT_HERSHEY_COMPLEX
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                square = cv2.rectangle(frame, p1, p2, (0,0,255))
                square
                #out.write(square)
                imagecount += 1
 
            # Display result
            cv2.imshow("Tracking", frame)
 
            # Exit if ESC pressed
            k = cv2.waitKey(1) & 0xff
            if k == 27 : break   

#out.release()
postxt.release()
negtxt.release()
video.release()
cv2.destroyAllWindows()