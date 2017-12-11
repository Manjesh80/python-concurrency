import time
from socket import *
import signal


def exit_gracefully(self, signum, frame):
    print("About to be killed now")
    self.kill_now = True


signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 25000))

while True:
    start_time = time.time()
    sock.send(b'30')
    resp = sock.recv(100)
    end_time = time.time()
    print(end_time - start_time)
    time.sleep(1)
