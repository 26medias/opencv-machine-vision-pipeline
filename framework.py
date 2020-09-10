import cv2 as cv
import json
import time

from vision.observer import Observer
from render.renderer import Renderer
from tracker.tracker import Tracker

class VisionFramework():
    __version__ = "0.0.1"
    def __init__(self, settings='settings/settings.json'):
        print("VisionFramework: ", self.__version__)
        with open(settings) as f:
            self.settings = json.load(f)
        
        self.renderer   = Renderer(self)
        self.tracker    = Tracker(self)
        self.observer   = Observer(self)
    
    # Start capturing
    def capture(self, src=0, fps=30):
        cap = cv.VideoCapture(src)
        cap.set(cv.CAP_PROP_FPS, fps);
        
        prevTime = time.time()
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            
            # Register a step with the tracker
            self.tracker.forward()
            
            # Show the observer what the camera sees
            self.observer.see(frame)
            
            # Render
            output = self.renderer.render(prevTime) # prevTime passed to calculate & display the FPS
            cv.imshow("Output", output)
            
            prevTime = time.time()
            
            if cv.waitKey(1) == ord('q'):
                break
        cap.release()
        cv.destroyAllWindows()



