import copy as _copy
from hidparser.enums import Collection
from hidparser.UsagePage.UsagePage import UsagePage, Usage, UsageType

from typing import Union


class Report:
    def __init__(self):
        self._usage = None
        self._usage_switches = []
        self._usage_modifiers = []


class _CollectionElement:
    def __init__(self, collection: Collection = None, parent = None):
        self.collection = collection
        self.parent = parent
        self.children = []


class DescriptorBuilder:
    def __init__(self):
        self._state_stack = []
        self._items = []
        self._reports = []
        self._usage_page = None
        self._usages = []

        self._collection = _CollectionElement()
        self._current_collection = self._collection

    @property
    def items(self):
        return self._items

    @property
    def reports(self):
        return self._reports

    def add_usage(self, usage: Union[Usage, int]):
        if isinstance(usage, Usage):
            self._usages.append(usage)
        else:
            self._usages.append(self._usage_page(usage))

    def set_usage_page(self, usage_page: UsagePage.__class__):
        self._usage_page = usage_page
        self._usages.clear()

    def push_collection(self, collection: Collection):
        collection_element = _CollectionElement(collection, self._current_collection)
        self._current_collection.children.append(collection_element)
        self._current_collection = collection_element
        return self

    def pop_collection(self):
        if self._current_collection.parent is None:
            raise RuntimeError("Can not pop collection state")
        self._current_collection = self._current_collection.parent
        if self._current_collection.parent is self._collection:
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
