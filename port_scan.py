# ========================================================
#               Simple Port Scanner
# ========================================================
"""Tries to connect to certain ports at a host or a whole network, in order
to find weaknesses for future attacks. Open ports = security breach.
More advanced threading with this port scanner for faster results,"""
import socket
from queue import Queue
import threading
import multiprocessing
import time

def scan():
    target = input('Enter target IP > ')
    q = Queue()

    # Loading the queue up with numbers 1-5000 (port numbers)
    for i in range(1, 502):
        q.put(i)

    def portscan(port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn = s.connect((target, port))
            return True
        except:
            return False

    def worker():
        while True:
            try:
                # grab each value from the queue
                port = q.get()
                if port > 500:
                    print('\nScan Complete.\nPress Ctrl C to quit')

                if portscan(port):
                    # we only print the open ports in this one
                    print(f'Port {port} is open!')
            except KeyboardInterrupt:
                print('Shutting Down...')

    print('Results'.center(18, '='))

    # Create 30 threads to handle the worker function MUCH faster for us
    for i in range(30):
        t = threading.Thread(target=worker)
        t.start()

scan()