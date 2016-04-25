import copy as _copy
from hidparser.enums import CollectionType, ReportFlags, EnumMask, ReportType
from hidparser.UsagePage.UsagePage import UsagePage, Usage, UsageType, UsageRange

from typing import Union, List


class ValueRange:
    def __init__(self, minimum=None, maximum=None):
        self.minimum = minimum
        self.maximum = maximum

    def __repr__(self):
        return "<{}: minimum: {}, maximum: {}>".format(self.__class__.__name__, self.minimum, self.maximum)


class Report:
    def __init__(self, usages: List[Usage], size: int = 0, count: int = 0, logical_range = None, physical_range = None):
        self.size = size
        self.count = count
        self.logical_range = logical_range
        self.physical_range = physical_range
        self.usages = usages
        self.usage_switches = []
        self.usage_modifiers = []


class ReportGroup:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.features = []


class _CollectionElement:
    def __init__(self, collection_type: CollectionType = None, usage: Usage = None, parent = None):
        self.collection_type = collection_type
        self.parent = parent
        self.children = [] # type: List[_CollectionElement]
        if parent is not None:
            if usage is None:
                raise ValueError("Collection item must have a usage")
            if collection_type == CollectionType.application and UsageType.collection_application not in usage.usage_types:
                raise ValueError("Usage can not be applied to application collection")
            if collection_type == CollectionType.physical and UsageType.collection_physical not in usage.usage_types:
                raise ValueError("Usage can not be applied to physical collection")
            if collection_type == CollectionType.logical and UsageType.collection_logical not in usage.usage_types:
                raise ValueError("Usage can not be applied to logical collection")
            if collection_type == CollectionType.named_array and UsageType.collection_named_array not in usage.usage_types:
                raise ValueError("Usage can not be applied to named array collection")
            if collection_type == CollectionType.usage_switch and UsageType.collection_usage_switch not in usage.usage_types:
                raise ValueError("Usage can not be applied to usage switch collection")
            if collection_type == CollectionType.usage_modifier and UsageType.collection_usage_modifier not in usage.usage_types:
                raise ValueError("Usage can not be applied to usage modifier collection")
            self.usage = usage


class DescriptorBuilder:
    def __init__(self):
        self._state_stack = []
        self._items = []
        self._reports = {0: ReportGroup()}
        self._report_group = self._reports[0]
        self._usage_page = None
        self._usages = []

        self.report_size = 0
        self.report_count = 0

        self.logical_range = ValueRange()
        self.physical_range = ValueRange()

        self._collection = _CollectionElement()
        self._current_collection = self._collection

    @property
    def items(self):
        return self._items

    @property
    def reports(self):
        return self._reports

    def add_report(self, report_type: ReportType, flags: Union[ReportFlags, EnumMask, int]):
        usages = []
        while len(usages) < self.report_count:
            usage = self._usages.pop(0) if len(self._usages) > 1 else self._usages[0]
            usages.extend(usage.get_range() if isinstance(usage, UsageRange) else [usage])

        report = Report(usages, self.report_size, self.report_count, _copy.copy(self.logical_range), _copy.copy(self.physical_range))

        if report_type is ReportType.input:
            self._report_group.inputs.append(report)
        elif report_type is ReportType.output:
            self._report_group.outputs.append(report)
        elif report_type is ReportType.feature:
            self._report_group.features.append(report)

    def set_report_id(self, report_id: int):
        if report_id in self._reports.keys():
            raise ValueError("Report ID already exists")
        self._reports[report_id] = ReportGroup()
        self._report_group = self._reports[report_id]

    def set_usage_range(self, minimum=None, maximum=None):
        usage = self._usages[len(self._usages)-1] if len(self._usages) else None
        if usage is None or not isinstance(usage, UsageRange):
            usage = UsageRange(self._usage_page)
            self._usages.append(usage)

        if minimum is not None:
            usage.minimum = minimum
        if maximum is not None:
            usage.maximum = maximum

    def set_logical_range(self, minimum = None, maximum = None):
        if minimum is not None:
            self.logical_range.minimum = minimum

        if maximum is not None:
            self.logical_range.maximum = maximum

    def set_physical_range(self, minimum=None, maximum=None):
        if minimum is not None:
            self.physical_range.minimum = minimum

        if maximum is not None:
            self.physical_range.maximum = maximum

    def add_usage(self, usage: Union[UsagePage, Usage, int]):
        if isinstance(usage, Usage):
            self._usages.append(usage)
        elif isinstance(usage, UsagePage):
            self._usages.append(usage.value)
        else:
            usage_page = self._usage_page if (usage & ~0xFFFF) == 0 else UsagePage.find_usage_page((usage & ~0xFFFF) >> 16)
            self._usages.append(usage_page.get_usage(usage & 0xFFFF))

    def set_usage_page(self, usage_page: UsagePage.__class__):
        self._usage_page = usage_page
        self._usages.clear()

    def push_collection(self, collection: CollectionType):
        collection_element = _CollectionElement(collection, self._usages.pop(0), self._current_collection)
        self._current_collection.children.append(collection_element)
        self._current_collection = collection_element

        self._usages.clear()
        return self

    def pop_collection(self):
        if self._current_collection.parent is None:
            raise RuntimeError("Can not pop collection state")
        self._current_collection = self._current_collection.parent

        self._usages.clear()
        return self

    def push(self):
        state = _copy.deepcopy(self.__dict__)
        if "_state_stack" in state.keys():
            del state["_state_stack"]
        self._state_stack.append(state)
        return self

    def pop(self):
        if len(self._state_stack) > 0:
            state = self._state_stack.pop()
            self.__dict__.update(state)
        return self
