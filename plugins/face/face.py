# Original code & models from https://github.com/LZQthePlane/Face-detection-base-on-ResnetSSD
# Credits to Zhiqiang Lee

import numpy as np
import cv2 as cv
import sys
import os
import uuid

file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
prototxt_file = file_path + 'face_models/Resnet_SSD_deploy.prototxt'
caffemodel_file = file_path + 'face_models/Res10_300x300_SSD_iter_140000.caffemodel'
cvNet = cv.dnn.readNetFromCaffe(prototxt_file, caffeModel=caffemodel_file)
cvNet.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
cvNet.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)

def getFacesFromFrame(img, params):
    height = img.shape[0]
    width = img.shape[1]
    blob = cv.dnn.blobFromImage(cv.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    cvNet.setInput(blob)
    detections = cvNet.forward()
    
    faces = []
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.3:
            bounding_box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
            x_start, y_start, x_end, y_end = bounding_box.astype('int')
            
            label = '{0:.2f}%'.format(confidence * 100)
            
            if params is not None and "square" in params and params["square"] is True:
                # Update the coordinates to resturn a square
                h = abs(y_end-y_start)
                w = abs(x_end-x_start)
                if w > h:
                    # Resize the height
                    padding = round((w-h)/2)
                    y_start = y_start - padding
                    y_end = y_end + padding
                elif h > w:
                    # Resize the width
                    padding = round((h-w)/2)
                    x_start = x_start - padding
                    x_end = x_end + padding
            
            faces.append({
                "score": confidence,
                "label": label,
                "type": "face",
                "x1":    x_start,
                "y1":    y_start,
                "x2":    x_end,
                "y2":    y_end
            })
    return faces