import re
from enum import Enum
import os


class ValidFilePath(object):
    def __set__(self, obj, val):
        if not os.path.exists():
            raise ValueError("Please enter a valid file path")
            self.__url = val

    def __get__(self, obj, objtype):
        return self.__url


class ValidHttpURL(object):
    def __set__(self, obj, val):
        if (val is None or re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE).search(val) is None):
            raise ValueError("Please set an valid HTTP(S) URL")
            self.__url = val

    def __get__(self, obj, objtype):
        return self.__url


class DataSourceType(Enum):
    HTTP = 100,
    LOCAL_FILE = 200,
    HDFS_FILE = 300


class ValidDataSourceType(object):
    def __set__(self, obj, val):
        if val is None or not DataSourceType.__contains__(DataSourceType[val]):
            raise ValueError("Please set a valid Data Source Type Enum, "
                             " possible values are -> ", [e.name for e in DataSourceType])
        self.__data_source_type = DataSourceType[val]

    def __get__(self, obj, objtype):
        return self.__data_source_type


class DataSource(object):
    data_source_type = ValidDataSourceType()
    data_source_path = ValidHttpURL()
