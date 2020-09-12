import cv2 as cv
import json
import time

from vision.observer import Observer
from render.renderer import Renderer
from tracker.tracker import Tracker
from tracker.lib.query import obj_query

class VisionFramework():
    __version__ = "0.0.1"
    def __init__(self, settings='settings/settings.json'):
        print("VisionFramework: ", self.__version__)
        with open(settings) as f:
            self.settings = json.load(f)
        
        self.renderer   = Renderer(self)
        self.tracker    = Tracker(self)
        self.observer   = Observer(self)
        self.events     = {}
    
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
        
    def on(self, event_name, event_fn, match=None):
        if event_name not in self.events:
            self.events[event_name] = []
        self.events[event_name].append((event_fn, match))
        print('On', event_name)
    
    def executeEvent(self, event_name, event_data):
        if event_name in self.events:
            if event_name in ['object.create','object.deactivate','object.delete']:
                for event in self.events[event_name]:
                    event_fn, match = event
                    if match is None:
                        event_fn(self, event_data)
                    else:
                        _matching = obj_query({"obj":self.tracker.objects[event_data]}, match)
                        if "obj" in _matching:
                            event_fn(self, event_data)
            elif event_name=='step':
                for event in self.events[event_name]:
                    print(">>", event)
                    event_fn, match = event
                    print(">>", event_fn, match)
                    objects = obj_query(self.tracker.objects, match)
                    for obj in objects:
                        event_fn(self, obj)