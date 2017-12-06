def until(start, func, end):
    if end == start:
        return []
    if func(end):
        return [end] + until(start, func, end + 1)
    else:
        return until(start, func, end + 1)


print(until(10, lambda x: x % 3 == 0 or x % 5 == 0, 0))
