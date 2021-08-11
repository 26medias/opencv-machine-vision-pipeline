import os
import socket    
import multiprocessing
import subprocess
import os
from urllib.request import *
from socket import timeout
import threading
import json
import time

class NetworkDevices:
    def __init__(self):
        self.output = {}
        print("Network Device Scanner started")
    
    def pinger(self, job_q, results_q):
        """
        Do Ping
        :param job_q:
        :param results_q:
        :return:
        """
        DEVNULL = open(os.devnull, 'w')
        while True:
    
            ip = job_q.get()
    
            if ip is None:
                break
    
            try:
                subprocess.check_call(['ping', '-c1', ip],
                                      stdout=DEVNULL)
                results_q.put(ip)
            except:
                pass
    
    
    def get_my_ip(self):
        """
        Find my IP address
        :return:
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    
    
    def map_network(self, pool_size=255):
        """
        Maps the network
        :param pool_size: amount of parallel ping processes
        :return: list of valid ip addresses
        """
    
        ip_list = list()
    
        # get my IP and compose a base like 192.168.1.xxx
        ip_parts = self.get_my_ip().split('.')
        base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'
    
        # prepare the jobs queue
        jobs = multiprocessing.Queue()
        results = multiprocessing.Queue()
    
        pool = [multiprocessing.Process(target=self.pinger, args=(jobs, results)) for i in range(pool_size)]
    
        for p in pool:
            p.start()
    
        # cue hte ping processes
        for i in range(1, 255):
            jobs.put(base_ip + '{0}'.format(i))
    
        for p in pool:
            jobs.put(None)
    
        for p in pool:
            p.join()
    
        # collect he results
        while not results.empty():
            ip = results.get()
            ip_list.append(ip)
    
        return ip_list
    
    
    def download_index(self, ip, lock):
        text = 'Fail'
        url = "http://"+ip+"/info"
        try:
            response = urlopen(Request(url))
            text = response.read()
            r_json = json.loads(text)
            r_json["ip"] = ip
            self.output[r_json['service_id']] = r_json
        except:
            pass
    
    def scanCandidates(self, ips):
        urls = [ip for ip in ips if ip not in '192.168.0.101']
        
        n = 5 #number of parallel connections
        chunks = [urls[i * n:(i + 1) * n] for i in range((len(urls) + n - 1) // n )]
        
        lock = threading.Lock()
        
        for chunk in chunks:
            threads = []
            for url in chunk:
                thread = threading.Thread(target=self.download_index, args=(url, lock,))
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()
        
        #print("End")
        return self.output
        
    def scan(self):
        start = time.time()
        print('Mapping...')
        #lst = self.map_network()
        lst = ['192.168.0.1', '192.168.0.100', '192.168.0.103', '192.168.0.112', '192.168.0.104', '192.168.0.105']
        #print(lst)
        print("Scanning candidates...")
        output = self.scanCandidates(lst)
        end = time.time()
        duration = end-start
        d_len = len(self.output.keys())
        print("Scanned in ", duration, "sec")
        print(d_len, "services found.")
        for k in self.output.keys():
            print(self.output[k]['service_name']+" ("+self.output[k]['service_id']+")")
        return self.output
        #print(output)

#devices = NetworkDevices()
#print(devices.scan())


















