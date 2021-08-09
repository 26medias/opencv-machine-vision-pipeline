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

def pinger(job_q, results_q):
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


def get_my_ip():
    """
    Find my IP address
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def map_network(pool_size=255):
    """
    Maps the network
    :param pool_size: amount of parallel ping processes
    :return: list of valid ip addresses
    """

    ip_list = list()

    # get my IP and compose a base like 192.168.1.xxx
    ip_parts = get_my_ip().split('.')
    base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'

    # prepare the jobs queue
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)]

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

output = {}

def download_index(url, lock):
    #print("Trying ", url)
    text = 'Fail'
    try:
        response = urlopen(Request(url))
        #response = requests.get(url, timeout=20)
        #text = response.json()
        text = response.read()
        r_json = json.loads(text)
        #print(url, "Found", r_json)
        output[url] = r_json
    #except socket.timeout:
    #    print(url, "timeout")
    except:
        pass
        #print(url, "failed")
    #indexing
    #with lock:
        #access shared resources
        #output[url] = text


def scanCandidates(ips):
    urls = ["http://"+ip+"/info" for ip in ips if ip not in '192.168.0.101']
    #print(urls)
    
    n = 5 #number of parallel connections
    chunks = [urls[i * n:(i + 1) * n] for i in range((len(urls) + n - 1) // n )]
    
    lock = threading.Lock()
    
    for chunk in chunks:
        threads = []
        for url in chunk:
            thread = threading.Thread(target=download_index, args=(url, lock,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
    
    #print("End")
    return output

if __name__ == '__main__':
    start = time.time()
    print('Mapping...')
    lst = map_network()
    #lst = ['192.168.0.1', '192.168.0.100', '192.168.0.101', '192.168.0.103', '192.168.0.112', '192.168.0.104', '192.168.0.105']
    #print(lst)
    print("Scanning candidates...")
    output = scanCandidates(lst)
    end = time.time()
    duration = end-start
    d_len = len(output.keys())
    print("Scanned in ", duration, "sec")
    print(d_len, "services found.")
    for k in output.keys():
        print(output[k]['service_name']+" ("+output[k]['service_id']+")")
    #print(output)


















