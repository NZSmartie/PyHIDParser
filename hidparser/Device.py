from hidparser.enums import CollectionType, ReportType, ReportFlags
from hidparser.UsagePage import UsagePage, Usage, UsageType
from hidparser.helper import ValueRange

from copy import copy as _copy
from functools import partial as _partial
from bitstring import BitArray as _BitArray, Bits as _Bits


class Report:
    def __init__(
            self,
            report_type: ReportType,
            report_id: int = 0,
            usages=[],
            size: int=0,
            count: int=0,
            logical_range=None,
            physical_range=None,
            flags=None,
            parent=None
    ):
        self.report_id = report_id
        self.report_type = report_type
        self.size = size
        self.count = count
        if type(logical_range) in (list, tuple):
            logical_range = ValueRange(*logical_range)
        if type(physical_range) in (list, tuple):
            physical_range = ValueRange(*physical_range)
        self.logical_range = logical_range if logical_range is not None else ValueRange() # type: ValueRange
        self.physical_range = physical_range if physical_range is not None else _copy(self.logical_range) # type: ValueRange

        if type(usages) not in (list, tuple):
            usages = (usages,)
        self.usages = usages

        self.flags = flags

        self.parent = parent
        self._values = [0]*self.count if self.count>0 else [0]

    @property
    def bits(self):
        return self.size * self.count

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
            self._values = value
        else:
            if not self.physical_range.in_range(value):
                raise ArithmeticError("{} is not within physical range".format(value))
            self._values[0] = value

    def __getitem__(self, key):
        return self._values[key]

    def __setitem__(self, key, value):
        self._values[key] = value

    def pack(self):
        values = _BitArray(self.count*self.size)
        for i in range(self.count):
            offset = i * self.size
            try:
                values[offset:offset + self.size] = int(self.physical_range.scale_to(self.logical_range, self._values[i]))
            except ArithmeticError:
                # If the value is outside of the physical range, and NULLs are allowed, then do not modify the value
                if not self.flags & ReportFlags.NULL_STATE:
                    raise
        return values

    def unpack(self, data):
        if not isinstance(data, _Bits):
            data = _Bits(data)
        for i in range(self.count):
            offset = i*self.size
            try:
                self._values[i] = self.logical_range.scale_to(self.physical_range, data[offset:offset + self.size].int)
            except ArithmeticError:
                # If the value is outside of the logical range, and NULLs are allowed, then do not modify the value
                if not self.flags & ReportFlags.NULL_STATE:
                    raise


class Collection:
    def __init__(self, items=None, usage=None, allowed_usage_types=None, collection_type: CollectionType=None, parent: "Collection"=None):
        if allowed_usage_types is None:
            allowed_usage_types = UsageType.collection_usage_types()
        if isinstance(allowed_usage_types, UsageType):
            allowed_usage_types = (allowed_usage_types,)
        elif type(allowed_usage_types) not in (list, tuple):
            raise ValueError("usage types must be a UsageType or a list or tuple of UsageType")

        self.collection_type = collection_type
        self._usage_types = allowed_usage_types
        self._usage = usage
        self.items = []  # type: _List[_Union[Collection, Report]]
        self._attrs = {}

        # _parent either refers to the collection it's nested in, or the collection it's derrived from
        # i.e. collections in ReportGroup.input are derrived from the collections in the Device object
        self.parent = parent

        if items is not None:
            if type(items) not in (list, tuple):
                items = [items]
            for item in items:
                self.append(item)

    @property
    def bits(self):
        # TODO Cache the total bit size, and invalidate when a child Collection or Report is added somewhere in the tree
        return sum([item.bits for item in self.items])

    def get_bit_size(self, report_type: ReportType):
        return sum([item.bits for item in self.items if item.report_type == report_type])

    def deserialize(self, data):
        offset = 0
        if not isinstance(data, _Bits):
            data = _Bits(data)
        for item in self.items:
            if isinstance(item, Report):
                if item.report_type not in (ReportType.INPUT, ReportType.FEATURE):
                    continue
                item.unpack(data[offset:offset + item.bits])
            else:
                item.deserialize(data[offset:offset + item.bits])
            offset += item.bits

    def serialize(self) -> bytes:
        data = _BitArray()
        for item in self.items:
            if isinstance(item, Report):
                if item.report_type is not ReportType.OUTPUT:
                    continue
                data.append(item.pack())
            else:
                data.append(item.serialize())
        return data

    def append(self, item):
        if isinstance(item, Collection):
            self.items.append(item)
            if item._usage is not None:
                self._attrs[item._usage._name_.lower()] = item
        elif isinstance(item, UsagePage):
            if not [usage_type for usage_type in item.usage_types if usage_type in self._usage_types]:
                raise ValueError()
            collection = Collection(usage=item)
            self.items.append(collection)
            self._attrs[item._name_.lower()] = collection
        elif isinstance(item, Report):
            if len(item.usages)>0:
                for usage in item.usages:
                    self._attrs[usage._name_.lower()] = property(
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
        if isinstance(other, UsagePage):
            return self._usage is other
        return super(Collection, self).__cmp__(other)


class ReportGroup:
    def __init__(self):
        self._inputs = Collection(allowed_usage_types=(UsageType.COLLECTION_APPLICATION,))
        self._outputs = Collection(allowed_usage_types=(UsageType.COLLECTION_APPLICATION,))
        self._features = Collection(allowed_usage_types=(UsageType.COLLECTION_APPLICATION,))

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
    def deserialize(self, data: bytes, report_type: ReportType=None):
        report = 0
        if len(self._reports) == 0:
            raise ValueError("No reports have been created for {}".format(self.__class__.__name__))

        if report_type is None:
            report_type = ReportType.INPUT
        if 0 not in self._reports.keys():
            report = data[0]
            data = data[1:]

        if report_type is ReportType.INPUT:
            return self._reports[report].inputs.deserialize(data)
        if report_type is ReportType.OUTPUT:
            return self._reports[report].outputs.deserialize(data)
        if report_type is ReportType.FEATURE:
            return self._reports[report].features.deserialize(data)

    def serialize(self, report: int = 0, report_type: ReportType=None) -> bytes:
        if report_type is None:
            report_type = ReportType.OUTPUT
        if len(self._reports) == 0:
            raise ValueError("No reports have been created for {}".format(self.__class__.__name__))
        if report_type is ReportType.INPUT:
            return self._reports[report].inputs.serialize()
        if report_type is ReportType.OUTPUT:
            return self._reports[report].outputs.serialize()
        if report_type is ReportType.FEATURE:
            return self._reports[report].features.serialize()

    def __init__(self, collection=None):
        self._reports = {}  # type: _Dict[int, ReportGroup]
        self._collection = Collection(items=collection, allowed_usage_types=UsageType.COLLECTION_APPLICATION)
        self._populate_report_types(self._collection)

    @property
    def reports(self):
        return self._reports

    def _populate_report_types(self, collection: Collection, path=None):
        if path is None:
            path = []

        for item in collection.items:
            if isinstance(item, Collection):
                path.append(item)
                self._populate_report_types(item, path.copy())
                path.pop()
                continue
            # assume the item is a Report
            if item.report_id not in self._reports.keys():
                self._reports[item.report_id] = ReportGroup()
            if item.report_type is ReportType.INPUT:
                self._collection_add_report(
                    self._reports[item.report_id].inputs,
                    path.copy(),
                    item
                )
            elif item.report_type is ReportType.OUTPUT:
                self._collection_add_report(
                    self._reports[item.report_id].outputs,
                    path.copy(),
                    item
                )
            elif item.report_type is ReportType.FEATURE:
                self._collection_add_report(
                    self._reports[item.report_id].features,
                    path.copy(),
                    item
                )

    def _collection_add_report(self, collection: Collection, path, report: Report):
        while len(path)>0:
            target = path.pop(0)
            try:
                collection = [item for item in collection.items if item.parent == target][0]
                continue
            except IndexError:
                break
        while len(path) >= 0 and collection.parent != target:
            # Create a derrived Collection
            new_collection = Collection(
                usage=target._usage,
                allowed_usage_types=target._usage_types,
                collection_type=target.collection_type,
                parent=target
            )
            collection.append(new_collection)
            collection = new_collection
            if len(path)>0:
                target = path.pop(0)

        collection.append(report)
