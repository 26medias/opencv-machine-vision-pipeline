import cv2 as cv
import numpy as np
import time
import re

import render.utils

class Renderer():
    __version__ = "0.0.1"
    def __init__(self, framework):
        print("Renderer:", self.__version__)
        self.framework  = framework
        self._fps       = []
    
    def setFrame(self, frame):
        self.current_frame  = frame
    
    def render(self, prevTime=0):
        self.renderObjects(self.current_frame)
        current_fps = round(1.0/ (time.time() - prevTime))
        # Average the FPS over the past 10 frames and display that
        self._fps.append(current_fps)
        self._fps = self._fps[-10:]
        fps = np.mean(np.asarray(self._fps))
        cv.putText(self.current_frame, str(fps)+"fps", (20, 20), cv.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (229,155,3))
        return self.current_frame
    
    # Render the objects
    def renderObjects(self, frame):
        for rule in self.framework.settings["render"]["rules"]:
            targets = self.framework.tracker.query(rule["match"])
            for obj_id in targets:
                obj = self.framework.tracker.objects[obj_id]
                if "box" in rule["display"] and rule["display"]["box"] is True:
                    cv.rectangle(frame, (int(obj["x1"]), int(obj["y1"])), (int(obj["x2"]), int(obj["y2"])), self.RGB2BGR(rule["display"]["color"]), thickness=2)
                # If there's a label to show for that object type
                if "label" in rule["display"]:
                    # Extract the variables to replace ("[varname]")
                    variables = re.findall(r"\[([a-zA-Z0-9_]+)\]", rule["display"]["label"])
                    label = rule["display"]["label"]
                    for v in variables:
                        if v in obj:
                            label    = re.sub('\['+v+'\]', str(obj[v]), label)
                    cv.putText(frame, label, (int(obj["x1"]), int(obj["y1"])-10), cv.FONT_HERSHEY_COMPLEX_SMALL, 0.5, self.RGB2BGR(rule["display"]["color"]))
    
    def RGB2BGR(self, color):
        return (color[2],color[1],color[0])