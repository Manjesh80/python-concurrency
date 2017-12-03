import re


class ValidEmail(object):
    def __set__(self, obj, val):
        if not re.match(re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"), val):
            raise ValueError("Please set an valid email")
        self.__email = val

    def __get__(self, obj, objtype):
        return self.__email


class ValidHttpURL(object):
    def __set__(self, obj, val):
        if (val is None or re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE).search(val) is None):
            raise ValueError("Please set an valid URL")
            self.__url = val

    def __get__(self, obj, objtype):
        return self.__url


class ValidDataSource(object):
    def __set__(self, obj, val):
        if not re.match(re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"), val):
            raise ValueError("Please set an valid email")
        self.__url = val

    def __get__(self, obj, objtype):
        return self.__url


class DataSource(object):
    email = ValidEmail()


p1 = Person()
p1.email = "manjesh@gmai"
print(p1.email)
