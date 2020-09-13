# Author of the model & original code unknown.
# Adapted by Julien Loutre https://github.com/26medias

import numpy as np
import cv2 as cv
import sys
import os
 

CONFIDENCE_THRESHOLD = 0.3
NMS_THRESHOLD = 0.3

file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep

class_names = []
with open(file_path+"models/coco_labels.txt", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]


cvNet = cv.dnn.readNet(file_path+"models/yolov3.weights", file_path+"models/yolov3.cfg")
cvNet.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
cvNet.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)
model   = cv.dnn_DetectionModel(cvNet)
model.setInputParams(size=(416, 416), scale=1/255)

def getObjectsFromFrame(img, params):
    
    frame = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    #frame = cv..resize(frame, )
    
    classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    
    objects = []
    for (classid, score, box) in zip(classes, scores, boxes):
        if score[0] > 0.2:
            left, top, width, height = box
            right = left+width
            bottom = top+height
            objects.append({
                "object_score": score[0],
                "label": class_names[classid[0]],
                "x1":    round(left),
                "y1":    round(top),
                "x2":    round(right),
                "y2":    round(bottom)
            })
    return objects


