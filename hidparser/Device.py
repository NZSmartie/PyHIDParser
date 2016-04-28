from hidparser.UsagePage import UsagePage, Usage, UsageType
from hidparser.helper import ValueRange

from typing import List, Iterator
from copy import copy as _copy
from functools import partial as _partial
from bitstring import BitArray as _BitArray


class Report:
    def __init__(self, usages: List[Usage], size: int = 0, count: int = 0, logical_range = None, physical_range = None, flags = None):
        self.size = size
        self.count = count
        self.logical_range = logical_range if logical_range is not None else ValueRange() # type: ValueRange
        self.physical_range = physical_range if physical_range is not None else _copy(self.logical_range) # type: ValueRange
        # TODO ensure usages is a list/tuple, otherwise, wrap it
        self.usages = usages
        # TODO make use of flags
        self.flags = flags
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

    def __getitem__(self, key):
        return self._values[key]

    def __setitem__(self, key, value):
        self._values[key] = value

    def pack(self):
        values = _BitArray(self.count*self.size)
        for i in range(self.count):
            values[i:i+self.size] = int(self.physical_range.scale_to(self.logical_range, self._values[i]))
        return values.tobytes()

    def unpack(self, data):
        values = _BitArray(data)
        for i in range(self.count):
            self._values[i] = self.logical_range.scale_to(self.physical_range, values[i:i + self.size])


class Collection:
    def __init__(self, usage = None, allowed_usage_types = None):
        if allowed_usage_types is None:
            allowed_usage_types = UsageType.collection_usage_types()
        if isinstance(allowed_usage_types, UsageType):
            allowed_usage_types = (allowed_usage_types,)
        elif type(allowed_usage_types) not in (list, tuple):
            raise ValueError("usage types must be a UsageType or a list or tuple of UsageType")

        self._usage_types = allowed_usage_types
        self._usage = usage
        self.items = []
        self._attrs = {}

    def append(self, item):
        if isinstance(item, UsagePage):
            if not [usage_type for usage_type in item.usage_types if usage_type in self._usage_types]:
                raise ValueError()
            collection = Collection(item)
            self.items.append(collection)
            self._attrs[item._name_] = collection
        elif isinstance(item, Report):
            if len(item.usages)>0:
                for usage in item.usages:
                    self._attrs[usage._name_] = property(
                        fget=_partial(item.__getitem__, item.usages.index(usage)),
                        fset=_partial(item.__setitem__, item.usages.index(usage))
                    )
            self.items.append(item)
        else:
            raise ValueError("usage type is not UsagePage or Report")

    def extend(self, items):
        for item in items:
            self.append(item)

    def __getitem__(self, item) -> "Collection":
        return self.items[item]

    def __getattr__(self, item) -> "Collection":
        try:
            value = self._attrs[item]
            if isinstance(value, property):
                return value.fget()
            return value
        except KeyError:
            raise AttributeError()


    def __iter__(self):
        return iter(self.items)

    def __cmp__(self, other):
        if other is None:
            return False
        if not isinstance(other, UsagePage):
            return super(Collection, self).__cmp__(other)
        return self._usage is other


class ReportGroup:
    def __init__(self):
        self._inputs = Collection(allowed_usage_types=(UsageType.collection_application,))
        self._outputs = Collection(allowed_usage_types=(UsageType.collection_application,))
        self._features = Collection(allowed_usage_types=(UsageType.collection_application,))

    @property
    def inputs(self) -> Collection:
        return self._inputs

    @property
    def outputs(self) -> Collection:
        return self._outputs

    @property
    def features(self) -> Collection:
        return self._features


class Device:
    def __init__(self):
        self._reports = {}

    def __getitem__(self, item) -> ReportGroup:
        if item not in self._reports:
            self._reports[item] = ReportGroup()
        return self._reports[item]

    def __iter__(self) -> Iterator(ReportGroup):
        return iter(self._reports)
