# Original code & models from https://github.com/Alialmanea/age-gender-detection-using-opencv-with-python
# Credits to Ali Rashad Almanea

import numpy as np
import cv2 as cv
import sys
import os

file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
prototxt_file = file_path + 'age_models/deploy_age.prototxt'
caffemodel_file = file_path + 'age_models/age_net.caffemodel'
cvNet = cv.dnn.readNetFromCaffe(prototxt_file, caffeModel=caffemodel_file)
cvNet.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
cvNet.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)

age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

def getAgeFromFace(face):
    height      = face.shape[0]
    width       = face.shape[1]
    blob        = cv.dnn.blobFromImage(face,1,(244,244),MODEL_MEAN_VALUES,swapRB=True)
    cvNet.setInput(blob)
    detections  = cvNet.forward()
    age         = age_list[detections[0].argmax()]
    return {
        "age": age
    }