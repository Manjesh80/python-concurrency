import asyncio
import aiohttp
from functools import partial
import time
import logging

successful_calls = dict()
failed_calls = dict()

logging.basicConfig(filename='report.log', level=logging.DEBUG)


async def get_web_page_len(idx, url):
    async with aiohttp.ClientSession() as session:
        call_start_time = time.time()
        try:
            response = await session.get(url=url, timeout=30)
            total_time = time.time() - call_start_time
            if response.status == 200:
                successful_calls.update(
                    {idx: [url, response.status, total_time, response.content.total_bytes or -1, '']})
                print(
                    f"SUCCESS => {idx} ==> {url} ==> {response.status} ==> {total_time} ==> {response.content.total_bytes or -1}")
            else:
                failed_calls.update({idx: [url, response.status, total_time, response.content.total_bytes or -1, '']})
                print(
                    f"FAILED => {idx} ==> {url} ==> {response.status} ==> {total_time} ==> {response.content.total_bytes or -1}")


        except Exception as e:
            total_time = time.time() - call_start_time
            failed_calls.update({idx: [url, -1, total_time, -1, repr(e)]})
            print(f"ERROR ==> {idx} ==> {url} ==> XXX ==> {total_time} ==> {repr(e)}")


get_web_page_len_with_no_index = partial(get_web_page_len, -1)


def get_url():
    with open("url.txt", "r") as fh:
        line_no = 0
        for line in fh:
            line_no += 1
            line = line.replace("\n", "")
            yield (line_no, line)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [asyncio.async(get_web_page_len(idx, url)) for idx, url in get_url()]
    start_time = time.time()
    loop.run_until_complete(asyncio.wait(tasks))
    run_time = time.time() - start_time
    loop.close()

    print(f"*********** {len(successful_calls)} -> SUCCESSFUL CALLS ***************")
    for x, y in sorted(successful_calls.items(), key=lambda x: x[0]):
        print(f" {x} \t {y} ")

    print(f"*********** {len(failed_calls)} -> FAILED CALLS ***************")
    for k, v in sorted(failed_calls.items(), key=lambda x: x[0]):
        print(f" {k} \t {v} ")
    print("**************************")

    print(f"*********** {len(successful_calls)} -> SUCCESSFUL CALLS ***************")
    print(f"*********** {len(failed_calls)} -> FAILED CALLS ***************")
    print(f"Total time taken to run is --> {run_time}")
