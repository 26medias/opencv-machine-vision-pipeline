def onNewObject(framework, object_id):
    print("New object detected!\n", framework.tracker.objects[object_id])

def onNewFace(framework, object_id):
    print("New face detected!\n", framework.tracker.objects[object_id])

def onNewPerson(framework, object_id):
    print("New person detected!\n", framework.tracker.objects[object_id])

def onDeletePerson(framework, object_id):
    print("Lost track of this person:\n", framework.tracker.objects[object_id])
