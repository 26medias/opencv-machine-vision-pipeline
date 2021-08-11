import threading
import time
 
class ThreadStack:
    def __init__(self, threads=5):
        print("States started")
        self.stack = []
        self.threads = []
        self.length = 0
        for i in range(0,threads):
            t = threading.Thread(target=self.processor)
            self.threads.append(t)
            t.start()
        #for t in self.threads:
        #    t.join()
    
    def processor(self):
        while True:
            #if len(self.stack)>0:
            if self.length>0:
                item = self.stack.pop(0)
                self.length = self.length - 1
                item[0](*item[1])
            time.sleep(0.5)
    
    def add(self, fn, args):
        self.stack.append([fn, args])
        self.length = self.length + 1
        return len(self.stack)
 
 