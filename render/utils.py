import cv2 as cv

def resize_image(image, width, COLOUR=[0,0,0]):
    h, w, layers = image.shape
    r = width/w;
    new_w = round(float(w)*r)
    new_h = round(float(h)*r)
    return cv.resize(image, (new_w, new_h)) 