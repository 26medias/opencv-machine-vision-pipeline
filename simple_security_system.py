from vision_pipeline import framework

# Event handler: When a new face is detected
def onNewFace(framework, object_id):
    print("\nNew face detected!\n", framework.tracker.objects[object_id])

# Event handler: When a face is identified
def onFaceIdentified(framework, object_id):
    print("onFaceIdentified", framework.tracker.objects[object_id])
    identity = framework.tracker.objects[object_id]["identity"]
    print("\nFace identified: ", identity)
    if identity in ["Julien", "Noah", "Camila"]:
        print("User allowed.")
    else:
        print("Intruder alert!")
    

# Event handler: When we lose track of a face
def onFaceLost(framework, object_id):
    print("\nWe lost track of this face:\n", framework.tracker.objects[object_id])


# Setup the pipeline 
visionPipeline = framework.VisionFramework(settings="settings/face_recognition.json")

# Trigger an event when a new face is detected
visionPipeline.on("object.create", onNewFace, {
    "type": {
        "$eq": "face"
    },
    "score": {
        "$gt": 0.3
    }
})

# Trigger an event when a face is identified
visionPipeline.on("attribute.update", onFaceIdentified, {
    "type": {
        "$eq": "face"
    }
}, attr="identity")

# Trigger an event when we lose track of a face
visionPipeline.on("object.deactivate", onFaceLost, {
    "type": {
        "$eq": "face"
    }
})

visionPipeline.capture(src=0, fps=30)