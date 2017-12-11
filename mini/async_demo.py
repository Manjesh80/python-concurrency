import asyncio


async def greet_name(name):
    return f'hello {name}'


g = greet_name("Ganesh")

asyncio.get_event_loop().run_until_complete(g)


async def print_list():
    names = ["Ram", "Ganesh", "Kumar"]
    for name in names:
        print(await greet_name(name=name))


asyncio.get_event_loop().run_until_complete(print_list())
