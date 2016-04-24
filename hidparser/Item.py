from enum import Enum, IntEnum
from hidparser.DescriptorBuilder import DescriptorBuilder

# Toddo create a Enum like class that happily converts subclasses into byte arrays

from abc import ABCMeta as _ABCMeta
import struct as _struct
import copy as _copy
from array import array as _array


class ItemType(IntEnum):
    main = 0x00
    global_ = 0x04
    local = 0x08
    reserved = 0x0C


class Item(metaclass=_ABCMeta):
    from abc import abstractmethod
    _item_map = None

    data = None  # type: _array

    # Abstract methods

    # @abstractmethod
    def visit(self, descriptor: DescriptorBuilder):
        pass

    @classmethod
    @abstractmethod
    def _get_tag(cls):
        pass

    @classmethod
    @abstractmethod
    def _get_type(cls):
        pass

    # Concrete methods

    def __init__(self, data: _array = None, long: bool = False):
        self.data = data

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, repr(self.data))

    @property
    def tag(self) -> int:
        """
        Gets the item tag number including the item type (bTag | bType)
        :return int:
        """
        return self._get_tag()

    @property
    def type(self) -> ItemType:
        """
        Gets the tag type of the item
        :return TagType:
        """
        return self._get_type()

    @classmethod
    def _map_subclasses(cls, parent_class):
        for c in parent_class.__subclasses__():
            if not issubclass(c, cls):
                continue
            try:
                key = c._get_tag()
                cls._item_map[key] = c
            except NotImplementedError:
                cls._map_subclasses(c)

    @classmethod
    def create(cls, tag: int, item_type: ItemType = None, data: _array = [], long: bool = False):
        if cls._item_map is None:
            cls._item_map = {}
            cls._map_subclasses(cls)
        if long:
            raise NotImplementedError("Log items are not supported by this parser yet")

        if item_type is not None:
            if (tag & ~0x0F) > 0:
                raise ValueError("tag is not valid")
            tag = (tag << 4) | item_type.value

        if tag not in cls._item_map:
            raise ValueError("Unknown tag {0} ({1})".format(tag, hex(tag)))

        return cls._item_map[tag](data=data, long=long)


class ValueItem(Item):
    value = None

    def __init__(self, **kwargs):
        super(ValueItem, self).__init__(**kwargs)

        if len(self.data) == 1:
            self.value = _struct.unpack("b", bytes(self.data))[0]
        if len(self.data) == 2:
            self.value = _struct.unpack("h", bytes(self.data))[0]
        if len(self.data) == 4:
            self.value = _struct.unpack("i", bytes(self.data))[0]

    @classmethod
    def _get_tag(cls):
        raise NotImplementedError()

    @classmethod
    def _get_type(cls):
        raise NotImplementedError()

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, repr(self.value))
