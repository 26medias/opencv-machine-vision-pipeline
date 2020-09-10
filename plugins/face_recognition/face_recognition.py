# Original code from https://github.com/ageitgey/face_recognition
# Credits to Adam Geitgey
# Adapted by Julien Loutre https://github.com/26medias

import face_recognition
import numpy as np
import cv2 as cv
import os
import uuid

known_identities = {}

# Load the known identifies from face images
def loadKnownIdentities():
    users = [ f.name for f in os.scandir("identities") if f.is_dir() ]
    for user in users:
        photos = [ f.name for f in os.scandir("identities/"+user) if f.is_file() ]
        known_identities[user] = []
        for photo in photos:
            features = face_recognition.face_encodings(face_recognition.load_image_file("identities/"+user+"/"+photo))
            if len(features) > 0:
                known_identities[user].append(features[0])
        
    print("Known Users:", users)

def getIdentity(face):
    identity = False
    
    face_encodings = face_recognition.face_encodings(face)
    if len(face_encodings) > 0:
        # Do know know that face?
        for user in known_identities.keys():
            matches = face_recognition.compare_faces(known_identities[user], face_encodings[0])
            if True in matches:
                identity = user
        if identity is False:
            # Brand new face
            # Assign an id
            identity    = str(uuid.uuid4())
            print("New identity: ", identity)
            # Create a new folder
            if not os.path.exists('identities/'+identity):
                os.makedirs('identities/'+identity)
            if identity not in known_identities:
                known_identities[identity] = []
        
        # Save a photo of the face if there are less than 20 examples of facial features for the user
        if len(known_identities[identity]) < 20:
            known_identities[identity].append(face_encodings[0])
            print(len(known_identities[identity]), "features found, saving one more")
            cv.imwrite("identities/"+identity+"/"+str(uuid.uuid4())+".png", face)
    
    
    output = {}
    if identity is not False:
        output = {
            "identity": identity
        }
    return output