# Original code & models from https://github.com/omar178/Emotion-recognition
# Credits to Omar Ayman
# Adapted by Julien Loutre https://github.com/26medias


from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np
import sys
import os
import uuid

file_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
emotion_model_path = file_path + 'models/_mini_XCEPTION.102-0.66.hdf5'

emotion_classifier = load_model(emotion_model_path, compile=True)
EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised", "neutral"]

def getEmotionsFromFace(face):
    height      = face.shape[0]
    width       = face.shape[1]
    
    _face = cv2.resize(face, (64, 64))
    _face = cv2.cvtColor(_face, cv2.COLOR_BGR2GRAY)
    _face = _face.astype("float") / 255.0
    _face = img_to_array(_face)
    _face = np.expand_dims(_face, axis=0)
    
    preds = emotion_classifier.predict(_face)[0]
    emotion_probability = np.max(preds)
    emotion = EMOTIONS[preds.argmax()]
    
    output = {
        "emotion": emotion,
        "emotion_label": "{}: {:.2f}%".format(emotion, emotion_probability * 100),
        "emotion_probability": emotion_probability
    }
    
    for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
        output["emotion_"+str(i)] = "{}: {:.2f}%".format(emotion, prob * 100),
        
    return output