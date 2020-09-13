# OpenCV Machine Vision Pipeline

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

Returns the identity of a face.

Requires an `identities` folder to exist.

Each sub-folder under `identities/` must be named after the person to recognize, and contain photos of their face.

Example:

- identities/Julien/photo1.png
- identities/Julien/photo2.png
- identities/Noah/photo1.png
- identities/Noah/photo2.png
- ...

Square images work best for accurate face recognition. Make sure the faces are cropped.

When using the face recognition plugin, unknown faces will be assigned a random identity (a UUID), a folder of that name will be created and photos of their faces will be taken and saved in that folder automatically.

Rename those automatically-created folders to the name of the person.

Code & models originally from https://github.com/ageitgey/face_recognition

Credits to Adam Geitgey


