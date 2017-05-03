import cv2
import sys
import time

if __name__ == '__main__' :
    # Set up tracker.
    # Instead of MIL, you can also use
    # BOOSTING, KCF, TLD, MEDIANFLOW or GOTURN
    
    resized = 0.25
    tracker = cv2.Tracker_create("MIL")
 
    # Read video
    video  = cv2.VideoCapture('files/20170502_161726.mp4')
    #fps = str(video.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    
    timestr = time.strftime('%Y%m%d-%H%M%S')
    outfilename = 'files/output-' + timestr + '.avi'
    out = cv2.VideoWriter(outfilename, fourcc, 20.0, (480,270))

    # Exit if video not opened.
    if not video.isOpened():
        print "Could not open video"
        sys.exit()
 
    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print 'Cannot read video file'
        sys.exit()
    # Define an initial bounding box
    bbox = (int(760*resized), int(295*resized), int(120*resized), int(100*resized))

    # Uncomment the line below to select a different bounding box
    # bbox = cv2.selectROI(frame, False)
    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
 
    while True:
        # Read a new frame
        ok, frame = video.read()
        frame = cv2.resize(frame,(0,0),fx=resized,fy=resized)
        height, width, channels = frame.shape 
        print height, width
        #gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        if not ok:
            break
         
        # Update tracker
        ok, bbox = tracker.update(frame)
 
        # Draw bounding box
        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            square = cv2.rectangle(frame, p1, p2, (0,0,255))
            square
            out.write(square)
            #cv2.putText(gray,fps,(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,255)
 
        # Display result
        cv2.imshow("Tracking", frame)
 
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break

out.release()
video.release()
cv2.destroyAllWindows()