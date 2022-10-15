import cv2 as cv
import json
import time

from vision_pipeline.vision.observer import Observer
from vision_pipeline.render.renderer import Renderer
from vision_pipeline.tracker.tracker import Tracker
from vision_pipeline.tracker.lib.query import obj_query
from services.ThreadStack import ThreadStack

class VisionFramework():
    __version__ = "2.0.0"
    def __init__(self, settings='settings/settings.json'):
        print("VisionFramework: ", self.__version__)
        with open(settings) as f:
            self.settings = json.load(f)
        
        self.renderer   = Renderer(self)
        self.tracker    = Tracker(self)
        self.observer   = Observer(self)
        self.stack      = ThreadStack(threads=5)
        self.events     = {}
    
    # Start capturing
    def capture(self, src=0, fps=30):
        cap = cv.VideoCapture(src)
        cap.set(cv.CAP_PROP_FPS, fps)
        
        prevTime = time.time()
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            
            # Register a step with the tracker
            self.tracker.forward()
            
            # Show the observer what the camera sees
            frame = self.observer.see(frame)
            
            # Render
            output = self.renderer.render(prevTime) # prevTime passed to calculate & display the FPS
            cv.imshow("Output", output)
            
            prevTime = time.time()
            
            if cv.waitKey(1) == ord('q'):
                break
        cap.release()
        cv.destroyAllWindows()
    
    # Register an event
    def on(self, event_name, event_fn, match=None, attr=None):
        if event_name not in self.events:
            self.events[event_name] = []
        self.events[event_name].append((event_fn, match))
        if attr is not None:
            self.observer.attr_watchlist.append(attr)
        return (event_name, len(self.events[event_name])-1)
    
    # Propagate an event
    def executeEvent(self, event_name, event_data):
        if event_name in self.events:
            if event_name in ['object.create','object.deactivate','object.reactivate','object.delete','attribute.update']:
                for event in self.events[event_name]:
                    event_fn, match = event
                    if match is None:
                        #event_fn(self, event_data)
                        self.stack.add(event_fn, [self, event_data])
                    else:
                        _matching = obj_query({"obj":self.tracker.objects[event_data]}, match)
                        if "obj" in _matching:
                            #event_fn(self, event_data)
                            self.stack.add(event_fn, [self, event_data])
            elif event_name=='step':
                for event in self.events[event_name]:
                    print(">>", event)
                    event_fn, match = event
                    print(">>", event_fn, match)
                    objects = obj_query(self.tracker.objects, match)
                    for obj in objects:
                        #event_fn(self, obj)
                        self.stack.add(event_fn, [self, obj])
























