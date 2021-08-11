import time
 
class State:
    def __init__(self):
        print("States started")
        self.state = {}
        self.events = {}
    
    def set(self, k, v):
        old_value = None
        is_new = True
        if k in self.state:
            old_value = self.state[k]
            is_new = False
        
        self.state[k] = v
        if is_new:
            self.executeEvent('create', {
                "key": k,
                "value": v
            })
        else:
            self.executeEvent('update', {
                "key": k,
                "old_value": old_value,
                "new_value": v
            })
    
    def remove(self, k):
        old_value = None
        if k in self.state:
            old_value = self.state[k]
        
        if k in self.state:
            self.state.pop(k)
            self.executeEvent('remove', {
                "key": k,
                "value": old_value
            })
        
    # Register an event
    def on(self, event_name, event_fn, match=None, attr=None):
        if event_name not in self.events:
            self.events[event_name] = []
        self.events[event_name].append((event_fn, match))
    
    # Propagate an event
    def executeEvent(self, event_name, event_data):
        if event_name in self.events:
            for event in self.events[event_name]:
                event_fn, match = event
                event_fn(event_data)
 
 