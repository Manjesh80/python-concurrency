def example(a, b, **kwargs):
    return a * b


print(type(example))
print(example.__code__.co_varnames)
print(example.__code__.co_argcount)

# higher order functions
year_cheese = [(2000, 29.87), (2001, 30.12), (2002, 30.6), (2003, 30.66), (2004, 31.33), (2005, 32.62), (2006, 32.73),
               (2007, 33.5), (2008, 32.84), (2009, 33.02), (2010, 32.92)]

triple_tuple = [(1, 2, 3), (7, 8, 9), (4, 10, 6)]
print(max(triple_tuple))
print(max(triple_tuple, key=lambda tpl: tpl[1]))

isinstance(triple_tuple, tuple)
