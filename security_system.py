from vision_pipeline import framework
from services.devices import NetworkDevices
from services.state import State
from urllib.request import *
from urllib.parse import urlencode
import random
import threading

class SecuritySystem:
    def __init__(self):
        print("Security System starting.")
        self.identities = {}
        self.state = State()
        self.state.on('create', self.onStateCreate)
        self.state.on('update', self.onStateUpdate)
        self.state.on('remove', self.onStateRemove)
    
    def start(self):
        self.scanForDevices()
        self.state.set("LED", "loading")
        self.startMonitoring()
        
    
    def scanForDevices(self):
        devices = NetworkDevices()
        self.devices = devices.scan()
        print("devices: ", self.devices)
    
    def startMonitoring(self):
        # Setup the pipeline 
        self.visionPipeline = framework.VisionFramework(settings="settings/face_recognition.json")
        
        # Trigger an event when a new face is detected
        self.visionPipeline.on("object.create", self.onNewFace, {
            "type": {
                "$eq": "face"
            },
            "score": {
                "$gt": 0.3
            }
        })
        
        # Trigger an event when a face is identified
        self.visionPipeline.on("attribute.update", self.onFaceIdentified, {
            "type": {
                "$eq": "face"
            }
        }, attr="identity")
        
        # Trigger an event when we lose track of a face
        self.visionPipeline.on("object.reactivate", self.onFaceIdentified, {
            "type": {
                "$eq": "face"
            }
        }, attr="identity")
        
        # Trigger an event when we lose track of a face
        self.visionPipeline.on("object.deactivate", self.onFaceLost, {
            "type": {
                "$eq": "face"
            }
        })
        
        self.state.set("LED", "default")
        
        self.visionPipeline.capture(src=0, fps=30)
        
    
    
    ############ LED MODES
    
    # Talk to the remote device via HTTP
    def serviceCall(self, service_id, params={}):
        if service_id not in self.devices:
            print("Device",service_id,"Not found")
            return False
        url = "http://"+self.devices[service_id]["ip"]+"/?"+urlencode(params)
        #print("url", url)
        try:
            response = urlopen(Request(url))
            text = response.read()
            #print("text", text)
        except:
            pass
    
    def setLED(self, mode="default", rgb=(101,57,227)):
        print("setLED(",mode,")")
        params = {}
        if mode=="Camila":
            params = {
                "type": "offline"
            }
        elif mode=="Noah":
            params = {
                "type": "online"
            }
        elif mode=="Julien":
            params = {
                "type": "rgb",
                "r": 101,
                "g": 57,
                "b": 227
            }
        elif mode=="loading":
            params = {
                "type": "rgb",
                "r": 245,
                "g": 124,
                "b": 0
            }
        elif mode=="default":
            params = {
                "type": "rgb",
                "r": 194,
                "g": 24,
                "b": 91
            }
        self.serviceCall("NODEMCU-LED-001", params)
    
    def updateLighting(self):
        if "Camila" in self.state.state and self.state.state["Camila"] == True:
            self.state.set("LED", "Camila")
        elif "Noah" in self.state.state and self.state.state["Noah"] == True:
            self.state.set("LED", "Noah")
        elif "Julien" in self.state.state and self.state.state["Julien"] == True:
            self.state.set("LED", "Julien")
        else:
            self.state.set("LED", "default")
    
    ############ EVENTS
    
    # Event handler: When a face is identified
    def onFaceIdentified(self, framework, object_id):
        #print("onFaceIdentified", framework.tracker.objects[object_id])
        identity = framework.tracker.objects[object_id]["identity"]
        self.state.set(identity, True);
        #self.identities[identity] = True
        print("\nHello: ", identity)
        #self.updateLighting()
            
    # Event handler: When a new face is detected
    def onNewFace(self, framework, object_id):
        #print("\nNew face detected!\n", framework.tracker.objects[object_id])
        return True
        
    # Event handler: When we lose track of a face
    def onFaceLost(self, framework, object_id):
        #print("\nWe lost track of this face:\n", framework.tracker.objects[object_id])
        if "identity" in framework.tracker.objects[object_id]:
            self.state.remove(framework.tracker.objects[object_id]["identity"]);
        #if "identity" in framework.tracker.objects[object_id] and framework.tracker.objects[object_id]["identity"] in self.identities and self.identities[framework.tracker.objects[object_id]["identity"]]==True:
        #    print("\nBye Bye ", framework.tracker.objects[object_id]["identity"])
        #    self.identities[framework.tracker.objects[object_id]["identity"]] = False
        #self.updateLighting()
            
        return True
    
    ############ STATES
    def onStateCreate(self, data):
        print("onStateCreate", data)
        if data['key']=='LED':
            self.setLED(data['value'])
        else:
            self.updateLighting()
    
    def onStateUpdate(self, data):
        print("onStateUpdate", data)
        if data['key']=='LED':
            self.setLED(data['new_value'])
        else:
            self.updateLighting()
    
    def onStateRemove(self, data):
        print("onStateRemove", data)
        if data['key']=='LED':
            self.setLED('default')
        else:
            self.updateLighting()



security = SecuritySystem()
security.start()












































































