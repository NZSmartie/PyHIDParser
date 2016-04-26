from hidparser.UsagePage import UsagePage, Usage, UsageType
from hidparser.helper import ValueRange

from typing import List
from copy import copy as _copy
from bitstring import BitArray as _BitArray


class Report:
    def __init__(self, usages: List[Usage], size: int = 0, count: int = 0, logical_range = None, physical_range = None):
        self.size = size
        self.count = count
        self.logical_range = logical_range if logical_range is not None else ValueRange() # type: ValueRange
        self.physical_range = physical_range if physical_range is not None else _copy(self.logical_range) # type: ValueRange
        self.usages = usages

        self._values = [0]*self.count if self.count>0 else 0

    @property
    def value(self):
        if self.count>1:
            return self._values
        return self._values[0]

    @value.setter
    def value_set(self, value):
        if self.count > 1:
            if type(value) is not list:
                raise ValueError("Can not set {} to {}".format(type(value), self.__class__.__name__))
            if len(value) != self.count:
                raise ValueError("Value must be of length {}".format(self.count))
            for v in value:
                if not self.physical_range.in_range(v):
                    raise ValueRange("{} is not within physical range".format(v))
            self._values = value
        else:
            if not self.physical_range.in_range(value):
                raise ValueRange("{} is not within physical range".format(value))
            self._values[0] = value

    def pack(self):
        values = _BitArray(self.count*self.size)
        for i in range(self.count):
            values[i:i+self.size] = int(self.physical_range.scale_to(self.logical_range, self._values[i]))
        return values.tobytes()

    def unpack(self, data):
        values = _BitArray(data)
        for i in range(self.count):
            self._values[i] = self.logical_range.scale_to(self.physical_range, values[i:i + self.size])


class ReportGroup:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.features = []


class Device:
    def __init__(self):
        self._reports = {}

    def __getitem__(self, item):
        if type(item) is not int:
            raise ValueError()
        try:
            return self._reports[item]
        except KeyError:
            self._reports[item] = ReportGroup()

    def __setitem__(self, key, value):
        if type(key) is not int or not isinstance(value, ReportGroup):
            raise ValueError()
        self._reports[key] = value

    def __iter__(self):
        return iter(self._reports)
