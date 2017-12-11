import time
from socket import *
import signal
from threading import Thread
import sys


def exit_gracefully(signum, frame):
    print("About to be killed now")
    global code
    code = 1
    sys.exit(0)


signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 25000))

n = 0
code = 0


def monitor_reqs():
    global n, code

    while True:
        time.sleep(1)
        print(n, ' -> reqs/sec')
        n = 0
        if code == 1:
            break


Thread(target=monitor_reqs).start()

while True:
    sock.send(b'1')
    resp = sock.recv(100)
    n += 1
    if code == 1:
        break
