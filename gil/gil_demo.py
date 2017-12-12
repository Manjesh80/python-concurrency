import time
from threading import Thread
import argparse

parser = argparse.ArgumentParser(description='Demo thread gotcha in Python')
parser.add_argument('mode', type=str, help='Enter mode of processing. Allowed values sequential or parallel')
args = parser.parse_args()


def count_down(n):
    while n > 0:
        n -= 1


def sequential_execution(big_number):
    count_down(big_number)


def parallel_execution(big_number):
    # break the countdown job in to 2 parts ( big_number // 2)
    # and execute in 2 threads and you would expect the program
    # to complete in half the time sequential execution
    t1 = Thread(target=count_down, args=(big_number // 2,))
    t2 = Thread(target=count_down, args=(big_number // 2,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == "__main__":
    start_time = time.time()

    print(f"Executing task in *** {args.mode.split('=')[1]} *** fashion")
    if args.mode == "sequential":
        sequential_execution(100000000)
    else:
        parallel_execution(100000000)
    print(f"Total time taken { time.time() - start_time}")
