from vision_pipeline import framework

# Event handler: When a new face is detected
def onNewFace(framework, object_id):
    print("\nNew face detected!\n", framework.tracker.objects[object_id])

# Event handler: When a new person is detected
def onNewPerson(framework, object_id):
    print("\nNew person detected!\n", framework.tracker.objects[object_id])

# Event handler: When we lose track of a face
def onFaceLost(framework, object_id):
    print("\nWe lost track of this face:\n", framework.tracker.objects[object_id])


# Setup the pipeline on 
visionPipeline = framework.VisionFramework(settings="settings/person_face.json")

# Trigger an event when a new face is detected
visionPipeline.on("object.create", onNewFace, {
    "type": {
        "$eq": "face"
    },
    "score": {
        "$gt": 0.5
    }
})

# Trigger an event when a new person is detected
visionPipeline.on("object.create", onNewPerson, {
    "type": {
        "$eq": "objects"
    },
    "label": {
        "$eq": "person"
    },
    "object_score": {
        "$gt": 0.7
    }
})

# Trigger an event when we lose track of a face
visionPipeline.on("object.deactivate", onFaceLost, {
    "type": {
        "$eq": "face"
    }
})

visionPipeline.capture(src=0, fps=30)