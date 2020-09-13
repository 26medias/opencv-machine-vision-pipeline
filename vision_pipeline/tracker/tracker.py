import uuid
import math
import time

from vision_pipeline.tracker.lib.query import obj_query

class Tracker():
    __version__ = "0.0.1"
    def __init__(self, framework):
        print("Tracker:", self.__version__)
        self.framework          = framework
        self.objects            = {}
        self.attr_watchlist     = []
        self.dist_threshold     = 50    # If the Euclidian distance is larger than this (pixels), consider it's a new object
        self.deactivateAfter    = 30    # Mark the object as disabled if not seen for 30 frames
        self.deleteAfter        = 60    # Delete the object if not seen for 60 frames
        self.counter            = 0
    
    def registerObject(self, object_type, object_data, parent=None):
        #print("[TRACKER] registerObject("+object_type+")", object_data)
        object_id   = self.getInstance(object_type, object_data)
        if object_id is None:
            # New object
            #print("[TRACKER] New object!")
            object_id   = str(uuid.uuid4())
            self.objects[object_id]         = object_data
            self.objects[object_id]["type"] = object_type
            self.objects[object_id]["created"]    = time.time()
            self.objects[object_id]["last_seen"]  = 0
            self.objects[object_id]["active"]     = True
            self.objects[object_id]["obj_number"] = self.counter
            self.counter = self.counter + 1
            self.framework.executeEvent("object.create", object_id)
        else:
            # Known object
            #print("[TRACKER] Known object!")
            self.objects[object_id]["last_seen"]  = 0
            self.objects[object_id]["active"]     = True
            # Update the object data
            for k in object_data.keys():
                self.objects[object_id][k]  = object_data[k]
    
    def getInstance(self, object_type, object_data):
        #print("[TRACKER] getInstance("+object_type+")", object_data)
        for object_id in self.objects.keys():
            if self.objects[object_id]["type"] == object_type:
                #print(">> [TRACKER] object_id", object_id, self.objects[object_id])
                dist = self.getDistance(self.objects[object_id], object_data)
                #print(">> [TRACKER] dist", dist)
                if dist < self.dist_threshold:
                    return object_id
        return None
    
    def query(self, query, debug=False):
        return obj_query(self.objects, query, debug)
    
    def getDistance(self, obj1, obj2):
        return (self.euclidianDistance(obj1["x1"], obj1["y1"], obj2["x1"], obj2["y1"]) + self.euclidianDistance(obj1["x2"], obj1["y2"], obj2["x2"], obj2["y2"])) / 2
    
    def euclidianDistance(self, x1, y1, x2, y2):
        return math.sqrt(((x2-x1)**2)+((y2-y1)**2))
    
    def forward(self):
        deletionList = []
        for object_id in self.objects.keys():
            self.objects[object_id]["last_seen"] = self.objects[object_id]["last_seen"] + 1
            if self.objects[object_id]["last_seen"] > self.deactivateAfter and self.objects[object_id]["active"] == True:
                self.objects[object_id]["active"]   = False
                self.framework.executeEvent("object.deactivate", object_id)
            if self.objects[object_id]["last_seen"] > self.deleteAfter:
                deletionList.append(object_id)
                self.framework.executeEvent("object.delete", object_id)
        if len(deletionList)>0:
            [self.objects.pop(key) for key in deletionList] 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    