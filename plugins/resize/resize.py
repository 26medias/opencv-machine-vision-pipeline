
import cv2

def resize(img, params):
    return cv2.resize(img, (params['w'], params['h']), interpolation=cv2.INTER_AREA)
