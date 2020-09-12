from vision_pipeline import framework

# Some event handlers
def onNewObject(framework, object_id):
    print("New object detected!\n", framework.tracker.objects[object_id])

def onNewFace(framework, object_id):
    print("New face detected!\n", framework.tracker.objects[object_id])

def onNewPerson(framework, object_id):
    print("New person detected!\n", framework.tracker.objects[object_id])

def onDeletePerson(framework, object_id):
    print("Lost track of this person:\n", framework.tracker.objects[object_id])


# Setup the pipeline on 
visionPipeline = framework.VisionFramework(settings="settings/person_face.json")

visionPipeline.on("object.create", onNewObject)
visionPipeline.on("object.create", onNewFace, {
    "type": {
        "$eq": "face"
    }
})
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
visionPipeline.on("object.delete", onDeletePerson, {
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

visionPipeline.capture(src=0, fps=30)