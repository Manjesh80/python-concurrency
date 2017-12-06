import math
import csv

from collections import namedtuple


def pfactorsl(x):
    if x % 2 == 0:
        yield 2
        if x // 2 > 1:
            yield from pfactorsl(x // 2)
        return
    for i in range(3, int(math.sqrt(x) + .5) + 1, 2):
        if x % i == 0:
            yield i
            if x // i > 1:
                yield from pfactorsl(x // i)
            return
    yield x


def row_iter(source):
    return csv.reader(source, delimiter="\t")


with open("Anscombe.txt") as source:
    print(list(row_iter(source)))

namedtuple("event", [{"name": str}, {"time", int}])
