class Foo:
    def __init__(self):
        self.x = 10

    def __getattr__(self, item):
        print(f"inside __getattr__ -> {item}")
        return item

        # def __getitem__(self, item):
        #      print(f"inside __getattr__ -> {item}")
        #      return self[item]

        # def __getattribute__(self, item):
        #     print(f"inside __getattribute__ -> {item}")
        #     return self[item]


f = Foo()
print(f.x)
f.y = 8
print(f.y)
# f.x = 20
# print(vars(f))
# print(f.__dict__)
