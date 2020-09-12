def onNewObject(framework, object_id):
    print("New object detected!", object_id, framework.tracker.objects[object_id])

def onNewFace(framework, object_id):
    print("New face detected!", object_id, framework.tracker.objects[object_id])

def onNewPerson(framework, object_id):
    print("New person detected!", object_id, framework.tracker.objects[object_id])

def onDeletePerson(framework, object_id):
    print("Lost track of this person:", object_id, framework.tracker.objects[object_id])
