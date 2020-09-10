# OpenCV Machine Vision Pipeline

Create a machine vision pipeline easily & get started with your machine vision project without re-inventing the wheels.

The whole piepline is built in a JSON file.

You list the plugins you need to load, you list the steps in your pipelines and its rules, and finally you setup rendering rules.

Here's a pipeline for face recognition:

    {
        "vision": {
            "plugins": {
                "box": {
                    "face": {
                        "import": "plugins.face.face",
                        "method": "getFacesFromFrame",
                        "enabled": true
                    }
                },
                "attr": {
                    "face_recognition": {
                        "import": "plugins.face_recognition.face_recognition",
                        "init":  "loadKnownIdentities",
                        "method": "getIdentity",
                        "enabled": true
                    }
                }
            },
            "pipeline": [{
                "op":       "box",
                "level":    "frame",
                "plugin":   "face"
            },{
                "op":       "attr",
                "level":    "object",
                "plugin":   "face_recognition",
                "match": {
                    "type": {
                        "$eq": "face"
                    },
                    "score": {
                        "$gt": 0.5
                    },
                    "identity_inference_count": {
                        "$opt": true,
                        "$lt": 3
                    }
                }
            }]
        },
        "render": {
            "rules": [{
                "display": {
                    "color": [0,179,255],
                    "label": "([number]) [label] - [identity]",
                    "box":   true
                },
                "match": {
                    "type": {
                        "$eq": "face"
                    },
                    "score": {
                        "$gt": 0.3
                    },
                    "active": {
                        "$eq": true
                    },
                    "identity": {
                        "$exists": true
                    }
                }
            },{
                "display": {
                    "color": [0,0,255],
                    "label": "([number]) [label] - Unknown Person",
                    "box":   true
                },
                "match": {
                    "type": {
                        "$eq": "face"
                    },
                    "score": {
                        "$gt": 0.3
                    },
                    "active": {
                        "$eq": true
                    },
                    "identity": {
                        "$exists": false
                    }
                }
            }]
        }
    }

In `vision.plugins` we list the plugins we want to use. They will be imported dynamically.
Here we import the face detection plugin, which will detect faces in the frame, and we import the face recognition plugin which will recognize faces & assign them an identity.

In `vision.pipeline` we list the steps, in order.

First we will detect faces, so we call the `face` plugin & we run it on the entire frame (`level`). Every face detected will be stored in a new object with attribute `type`=`face`.

The second step in the pipeline will call the `face_recognition` plugin, and we run it on every object that match the following condition: `type`=`face`, `score` is greater than `0.5`, `identity_inference_count` either doesn't exists or is less than `3`. This means it will execute the face_recognition on a faces only 3 times, then stop. The identity will persist on the object as long as it exists.

In `render.rules` we define which objects we want to render & how. Here we'll render a green (colors on OpenCV are BGR) rectangle around faces which have an identity, and a red rectangle around faces that do not have an identity.

## Plugins

### Objects recognition

#### Face

Returns the list of faces found on an OpenCV frame

Code & models originally from https://github.com/LZQthePlane/Face-detection-base-on-ResnetSSD

Credits to Zhiqiang Lee


#### Objects

Returns detected objects found on an openCV frame using Inception V2

Original code & models from author unknown.


### Object Attributes

#### Age

Returns the estimated age range from a cropped face

Code & models originally from https://github.com/Alialmanea/age-gender-detection-using-opencv-with-python

Credits to Ali Rashad Almanea

#### Gender

Returns the estimated gender from a cropped face

Code & models originally from https://github.com/Alialmanea/age-gender-detection-using-opencv-with-python

Credits to Ali Rashad Almanea


#### Emotions

Returns the estimated emotion from a cropped face

Code & models originally from https://github.com/omar178/Emotion-recognition

Credits to Omar Ayman


#### Face Recognition

Returns the estimated emotion from a cropped face

Code & models originally from https://github.com/ageitgey/face_recognition

Credits to Adam Geitgey