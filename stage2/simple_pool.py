from concurrent.futures import ProcessPoolExecutor as Pool

pool = Pool(5)


def simple_return():
    return 100


def simple_start():
    fut = pool.submit(simple_return)
    res = fut.result(100)
    print(res)
    print("done")


if __name__ == '__main__':
    simple_start()
