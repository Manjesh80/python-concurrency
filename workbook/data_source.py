import os
import re
from enum import Enum
from weakref import WeakKeyDictionary


def valid_file_path(value):
    if not os.path.exists(value):
        raise ValueError(value, " is not present. Please make sure the file exists")
    return value

def valid_http_url(value):
    if (value is None or re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE).search(value) is None):
        raise ValueError("Please set an valid HTTP(S) URL")
    return value


class DataSourceType(Enum):
    NOT_DEFINED = (0, None)
    HTTP = (100, valid_http_url)
    LOCAL_FILE = (200, valid_file_path)

    def __init__(self, enum_id, enum_validator):
        self._id = enum_id
        self._validator = enum_validator

    @property
    def validator(self):
        return self._validator


class ValidDataSourceType(object):
    def __init__(self):
        self.default = DataSourceType.NOT_DEFINED
        self.values = WeakKeyDictionary()

    def __get__(self, instance, owner):
        return self.values.get(instance, self.default)

    def __set__(self, instance, value):
        if value is None or not DataSourceType.__contains__(DataSourceType[value]):
            raise ValueError("Please set a valid Data Source Type Enum, "
                             " possible values are -> ", [e.name for e in DataSourceType])
        self.values[instance] = DataSourceType[value]

    def __delete__(self, instance):
        del self.values[instance]


class ValidDataSourcePath(object):
    def __init__(self, default_data_source_type_field='data_source_type'):
        self._default = ''
        self._default_data_source_type_field = default_data_source_type_field
        self.values = WeakKeyDictionary()

    def __get__(self, instance, owner):
        return self.values.get(instance, self._default)

    def __set__(self, instance, *value):
        data_source_type_field = self._default_data_source_type_field
        value_to_set = None

        if value and len(value) == 1 and isinstance(value[0], str):  # user sent only the value
            value_to_set = value[0]
        if value and len(value) == 1 and isinstance(value[0], tuple):  # user sent the value , and the validation field
            value_to_set = value[0][0]
            data_source_type_field = value[0][1]

        _data_source_type = getattr(instance, data_source_type_field, None)
        if not _data_source_type:
            raise ValueError(" Valid source path depends on ValidDataSourceType , "
                             " please make sure you have an attribute named ValidDataSourceType")
        _data_source_type.validator(value_to_set)
        self.values[instance] = value_to_set


class DataSource(object):
    data_source_type = ValidDataSourceType()
    data_source_path = ValidDataSourcePath()


class SomeOtherDomainModel(object):
    data_source_type_ext = ValidDataSourceType()
    data_source_path = ValidDataSourcePath()


print(" **************** Scenario 1 - Start **************** ")
ds1 = DataSource()
ds1.data_source_type = 'HTTP'
ds1.data_source_path = "http://www.google.com"
print(ds1.data_source_path)
print(" **************** Scenario 1 - End **************** ")

print(" **************** Scenario 2 - Start **************** ")
ds2 = SomeOtherDomainModel()
ds2.data_source_type_ext = 'HTTP'
ds2.data_source_path = ("http://www.yahoo.com", 'data_source_type_ext')
print(ds2.data_source_path)
print(" **************** Scenario 2 - Start **************** ")


# # def __set__(self, instance, value, data_source_type_field='data_source_type_field'):
# def __set__(self, instance, *value, **values):
#     # _data_source_type = getattr(instance, data_source_type_field, None)
#     _data_source_type = getattr(instance, value[1], None)
#     if not _data_source_type:
#         raise ValueError(" Valid source path depends on ValidDataSourceType , "
#                          " please make sure you have an attribute named ValidDataSourceType")
#     _data_source_type.validator(value)
#     self.values[instance] = value
#     return value
