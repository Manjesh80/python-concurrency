import asyncio

import aiohttp

websites = ['http://www.google.com', 'http://www.yahoo.com']
url_len = dict()


async def get_web_page_len(idx, url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url)
        url_len.update({idx: [url, response.content.total_bytes]})


def get_url():
    with open("url.txt", "r") as fh:
        line = fh.readline()
        yield line

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [asyncio.async(get_web_page_len(idx, url)) for idx, url in enumerate(websites)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    print(url_len)
