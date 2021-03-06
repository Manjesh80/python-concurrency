# server.py
from socket import *
import sys
import signal
import socket as modSock
from threading import Thread


def exit_gracefully(self, signum, frame):
    print("About to be killed now")
    self.kill_now = True


signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)


def fib(n: int):
    if (n < 2):
        return n
    else:
        return fib(n - 1) + fib(n - 2)


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
        print("Started client")


def fib_handler(client: socket):
    while True:
        try:
            req = client.recv(100)
            print("Received request")
            print(req)
            if not req:
                break
            n = int(req)
            result = fib(n)
            print("Returing result %d", result)
            resp = str(result).encode('ascii') + b'\n'
            print("performing encode successful")
            client.send(resp)
            print("send successful")
        except:
            print(sys.exc_info()[0])
            break
    print('closed')


fib_server(('', 25000))
