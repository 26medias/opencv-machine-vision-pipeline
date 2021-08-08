import threading
from queue import Queue
import time
import socket
import requests

# a print_lock is what is used to prevent "double" modification of shared variables.
# this is used so while one thread is using a variable, others cannot access
# it. Once done, the thread releases the print_lock.
# to use it, you want to specify a print_lock per thing you wish to print_lock.
print_lock = threading.Lock()



target = '127.0.0.1'
#ip = socket.gethostbyname(target)

class Scanner1:
    def __init__(self):
        print("Network Scanner")

    def portscan(self, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            con = self.s.connect((target,port))
            with print_lock:
                print('port', port)
            con.close()
        except:
            pass


    # The threader thread pulls an worker from the queue and processes it
    def threader(self):
        while True:
            # gets an worker from the queue
            worker = self.q.get()

            # Run the example job with the avail worker in queue (thread)
            self.portscan(worker)

            # completed with the job
            self.q.task_done()


    def scan(self):

        # Create the queue and threader 
        self.q = Queue()

        # how many threads are we going to allow for
        for x in range(30):
            self.t = threading.Thread(target=self.threader)

            # classifying as a daemon, so they will die when the main dies
            self.t.daemon = True

            # begins, must come after daemon definition
            self.t.start()


        self.start = time.time()

        # 100 jobs assigned.
        for worker in range(1,100):
            self.q.put(worker)

        # wait until the thread terminates.
        self.q.join()

#scanner = Scanner()
#scanner.scan()



class Scanner2:
    def __init__(self):
        print("Network Scanner")

    def portscan(self, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(20)
        try:
            ip = '192.168.0.'+str(port)
            #print("ip", ip)
            con = self.s.connect((ip,80))
            with print_lock:
                print('Server found: ', ip)
            con.close()
        except:
            pass


    # The threader thread pulls an worker from the queue and processes it
    def threader(self):
        while True:
            # gets an worker from the queue
            worker = self.q.get()

            # Run the example job with the avail worker in queue (thread)
            self.portscan(worker)

            # completed with the job
            self.q.task_done()


    def scan(self):

        # Create the queue and threader 
        self.q = Queue()

        # how many threads are we going to allow for
        for x in range(30):
            self.t = threading.Thread(target=self.threader)

            # classifying as a daemon, so they will die when the main dies
            self.t.daemon = True

            # begins, must come after daemon definition
            self.t.start()


        self.start = time.time()

        # 100 jobs assigned.
        for worker in range(1,255):
            self.q.put(worker)

        # wait until the thread terminates.
        self.q.join()

#scanner = Scanner()
#scanner.scan()




class Scanner:
    def __init__(self):
        print("Network Service Scanner")

    def portscan(self, port):
        ip = "192.168.0."+str(port)
        info_url = "http://"+ip+"/info"

        try:
            response = requests.get(info_url).json()
            print(ip, response['service_id'])
            return response
        except:
            return False
            #print("Failed: ", ip, info_url)


    # The threader thread pulls an worker from the queue and processes it
    def threader(self):
        while True:
            # gets an worker from the queue
            worker = self.q.get()

            # Run the example job with the avail worker in queue (thread)
            self.portscan(worker)

            # completed with the job
            self.q.task_done()


    def scan(self):

        # Create the queue and threader 
        self.q = Queue()

        # how many threads are we going to allow for
        for x in range(5):
            self.t = threading.Thread(target=self.threader)

            # classifying as a daemon, so they will die when the main dies
            self.t.daemon = True

            # begins, must come after daemon definition
            self.t.start()


        self.start = time.time()

        # 100 jobs assigned.
        for worker in range(100,110):
            self.q.put(worker)

        # wait until the thread terminates.
        self.q.join()

        print("Done");

scanner = Scanner()
scanner.scan()
print("End");

#try:
#    response = requests.get("http://192.168.0.105/info").json()
#    print(response['service_id'])
#except:
#    print("Failed")