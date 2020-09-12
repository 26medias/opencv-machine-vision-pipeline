from framework import VisionFramework

from events.examples import onNewObject
from events.examples import onNewFace
from events.examples import onNewPerson
from events.examples import onDeletePerson

visionPipeline = VisionFramework(settings="settings/gender_age_objects.json")

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