#!/usr/bin/env python3

 
import numpy as np
import cv2 as cv

from common import Rect

 
inWidth = 300
inHeight = 300
WHRatio = inWidth / float(inHeight)
inScaleFactor = 0.007843
meanVal = 127.5

 
classNames = ['background',
'aeroplane', 'bicycle', 'bird', 'boat',
'bottle', 'bus', 'car', 'cat', 'chair',
'cow', 'diningtable', 'dog', 'horse',
'motorbike', 'person', 'pottedplant',
'sheep', 'sofa', 'train', 'tvmonitor']

class PeopleDetector:
    def __init__(self, proto, model, confidence):
    
        self.net = cv.dnn.readNetFromCaffe(proto, model)
        
        self.confidence = confidence
     
        self.people = []
       
        self.other_objects = []

    def update(self, image):
        
        self.people = []
        self.other_objects = []
        frame = image.copy()

         blob = cv.dnn.blobFromImage(frame, inScaleFactor, (inWidth, inHeight), (meanVal, meanVal, meanVal), False, False)
       
        self.net.setInput(blob)
        detections = self.net.forward()

  
        cols = frame.shape[1]
        rows = frame.shape[0]

  
        for i in range(detections.shape[2]):
 
            confidence = detections[0, 0, i, 2]
       
            class_id = int(detections[0, 0, i, 1])
            if confidence < self.confidence:
                continue
            if class_id >= len(classNames):
           
                continue

    
            xLeftBottom = int(detections[0, 0, i, 3] * cols)
            yLeftBottom = int(detections[0, 0, i, 4] * rows)
            xRightTop   = int(detections[0, 0, i, 5] * cols)
            yRightTop   = int(detections[0, 0, i, 6] * rows)
        
            roi = Rect((xLeftBottom, yLeftBottom), (xRightTop, yRightTop))

      
            if classNames[class_id] == 'person':
                
                self.people.append(roi)
            else:
             
                self.other_objects.append(classNames[class_id])

    def visualise(self, frame):
  
    
        for roi in self.people:
            cv.rectangle(frame, roi.tl(), roi.br(), (0, 255, 0))

        cv.imshow("detections", frame)

def main():
 
    import sys
    try:
        video_src = sys.argv[1]
    except:
        video_src = 0

    print(__doc__)
    detector = PeopleDetector(sys.argv[2], sys.argv[3], 0.5)
    cam = cv.VideoCapture(video_src)
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        detector.update(frame)
        detector.visualise(frame)
        if cv.waitKey(1) >= 0:
            break
    cam.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
