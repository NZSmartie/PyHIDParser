import copy as _copy
from hidparser.enums import Collection


class Report:
    _usage = None
    _usage_switches = []
    _usage_modifiers = []


class _CollectionElement:
    children = []
    parent = None
    usage = None
    collection = None

    def __init__(self, collection: Collection = None, parent = None):
        self.collection = collection
        self.parent = parent


class Descriptor:
    _state_stack = []
    _items = []
    _reports = []

    _collection = _CollectionElement()
    _current_collection = _collection

    @property
    def items(self):
        return self._items

    @property
    def reports(self):
        return self._reports

    def push_collection(self, collection: Collection):
        collection_element = _CollectionElement(collection, self._current_collection)
        self._current_collection.children.append(collection_element)
        self._current_collection = collection_element

    def pop_collection(self):
        if self._current_collection.parent is None:
            raise RuntimeError("Can not pop collection state")
        self._current_collection = self._current_collection.parent

    def push(self):
        state = _copy.deepcopy(self.__dict__)
        if "_state_stack" in state.keys():
            del state["_state_stack"]
        self._state_stack.append(state)

    def pop(self):
        if len(self._state_stack) == 0:
            return False
        state = self._state_stack.pop()
        self.__dict__.update(state)
        return True