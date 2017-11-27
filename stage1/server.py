# server.py
from socket import *


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
        client, addr = sock.accept()
        print("Connection ==>", addr)


def fib_handler(client: socket):
    while True:
        req = client.recv(100)
        if not req:
            break
        n = int(req)
        result = fib(n)
        resp = str(result).encode('ascii') + b'\n'
        client.send(resp)
    print('closed')


fib_server(('', 25000))
