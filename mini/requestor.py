from threading import *
from urllib.request import *
from collections import deque
from concurrent.futures import Future
import asyncio
from asyncio import wait_for, wrap_future


class Queuey:
    def __init__(self, maxsize):
        self.mutex = Lock()
        self.maxsize = maxsize
        self.items = deque()
        self.getters = deque()
        self.putters = deque()

    def get_no_block(self):
        with self.mutex:
            if self.items:
                # Wake a putter
                if self.putters:
                    self.putters.popleft().set_result(True)
                return self.items.popleft(), None
            else:
                fut = Future()
                self.getters.append(fut)
                return None, fut

    def put_no_block(self, url):
        if len(self.items) < self.maxsize:
            self.items.append(url)
            # Wake a getter
            if self.getters:
                self.getters.popleft().set_result(self.items.popleft())
        else:
            fut = Future()
            self.putters.append(fut)
            return fut

    async def get_async(self):
        item, fut = self.get_no_block()
        if fut:
            item = await wait_for(wrap_future(fut), None)
        return item

    def get_sync(self):
        item, fut = self.get_no_block()
        if fut:
            item = fut.result()
        return item

    def put_sync(self, url):
        fut = self.put_no_block(url)
        if fut is None:
            return
        return fut.result()

    async def put_async(self, url):
        while True:
            fut = self.put_no_block(url)
            if fut is None:
                return
            await wait_for(wrap_future(fut), None)


def make_request(url):
    response = urlopen(url)
    return response.header


def main():
    print("Invoked main")
    make_request("www.google.com")
    print("Ganesh bye")


def test_basic_queue_non_blocking():
    q = Queuey(2)
    q.put_no_block("www.google.com")
    q.put_no_block("www.yahoo.com")
    url, fut = q.get_no_block()
    print(url)
    print(fut)
    url, fut = q.get_no_block()
    print(url)
    print(fut)
    url, fut = q.get_no_block()
    print(url)
    print(fut)
    print("Done")


def test_basic_queue_blocking():
    q = Queuey(2)
    q.put_sync("www.google.com")
    q.put_sync("www.yahoo.com")

    url = q.get_sync()
    print(url)
    url = q.get_sync()
    print(url)
    url = q.get_sync()
    print(url)
    print("Done")


async def test_basic_queue_async():
    q = Queuey(2)
    await q.put_async("www.google.com")
    await q.put_async("www.yahoo.com")
    url = await q.get_async()
    print(url)
    url = await q.get_async()
    print(url)
    url = await q.get_async()
    print(url)
    print("Done")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(test_basic_queue_async())
