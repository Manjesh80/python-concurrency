import asyncio
import aiohttp

urls = ["http://www.google.com", "http://www.yahoo.com"]
results: dict = {}


async def get_url_data(*, idx, url):
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url=url, timeout=15)
        results.update({idx: [url, resp.content.total_bytes]})


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.wait([get_url_data(idx=i, url=v) for i, v in enumerate(urls)])
    )
    loop.close()
    print(results)
