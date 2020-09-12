# Author of the model & original code unknown.
# Adapted by Julien Loutre https://github.com/26medias

import numpy as np
import cv2 as cv
import sys
import os
from plugins.objects.objects_models.coco_labels import LABEL_MAP
 
file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep

FROZEN_GRAPH = file_path+"objects_models/ssd_inception_v2_coco.pb"
PB_TXT = file_path+"objects_models/ssd_inception_v2_coco.pbtxt"
SIZE = 300

cvNet = cv.dnn.readNetFromTensorflow(FROZEN_GRAPH, PB_TXT)
cvNet.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
cvNet.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)

def getObjectsFromFrame(img, params):
    height = img.shape[0]
    width = img.shape[1]
    cvNet.setInput(cv.dnn.blobFromImage(img, 1.0/127.5, (SIZE, SIZE), (127.5, 127.5, 127.5), swapRB=True, crop=False))
    cvOut = cvNet.forward()
    faces = []
    for detection in cvOut[0,0,:,:]:
        score = float(detection[2])
        if score > 0.3:
            left = detection[3] * width
            top = detection[4] * height
            right = detection[5] * width
            bottom = detection[6] * height
            faces.append({
                "score": score,
                "type":  LABEL_MAP[int(detection[1])],
                "label": LABEL_MAP[int(detection[1])],
                "x1":    round(left),
                "y1":    round(top),
                "x2":    round(right),
                "y2":    round(bottom)
            })
    return faces