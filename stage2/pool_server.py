# server.py
from socket import *
import sys
import signal
from threading import Thread
sys.path.insert(0, "C:\\workspace\\python\\concurrency-from-scratch\\fibonacci")
from fibonacci import *

from concurrent.futures import ProcessPoolExecutor as Pool

print("************* Called again *************")


def exit_gracefully(self, signum, frame):
    print("About to be killed now")
    self.kill_now = True


signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)

pool = Pool(1)


# def fib(n):
#     if (n < 2):
#         return n
#     else:
#         return fib(n - 1) + fib(n - 2)


def fib_server(address):
    sock = socket()

    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        print("Ready to receive connection")
        client, addr = sock.accept()
        print("Received connection")
        print("Connection ==>", addr)
        Thread(target=fib_handler, args=(client,)).start()
        # fib_handler(client)
        print("Started client")


def simple_return():
    return 1


def fib_handler(client: socket):
    while True:
        try:
            req = client.recv(100)
            print("Received request")
            print(req)
            if not req:
                break
            n = int(req)

            print(" Doing submit to pool")
            future = pool.submit(fib, n)
            result = future.result()
            # result = fib(n)
            print("Returning result %d", result)
            resp = str(result).encode('ascii') + b'\n'
            print("performing encode successful")
            client.send(resp)
            print("send successful")
        except:
            print("************* Received Error ***********")
            print(sys.exc_info()[0])
            break
    print('closed')


fib_server(('', 25000))

if __name__ == '__main__':
    print("********* calling main *******")
