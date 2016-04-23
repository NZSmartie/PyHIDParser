from enum import IntEnum
from array import array

# Toddo create a Enum like class that happily converts subclasses into byte arrays

from abc import ABCMeta as _ABCMeta


class ItemType(IntEnum):
    main = 0x00
    global_ = 0x04
    local = 0x08
    reserved = 0x0C


class Item(metaclass=_ABCMeta):
    import array
    from abc import abstractmethod
    _item_map = None

    data = None  # type: array.array

    def __init__(self, data: array.array = None, long: bool = False):
        self.data = data

    def __repr__(self):
        return "<{0}: {1}, {2}>".format(self.__class__.__name__, repr(self.tag), repr(self.data))

    @classmethod
    @abstractmethod
    def _get_tag(cls):
        pass

    @classmethod
    @abstractmethod
    def _get_type(cls):
        pass

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
    def create(cls, tag: int, item_type: ItemType = None, data: array.array = [], long: bool = False):
        if cls._item_map is None:
            cls._item_map = {}
            for c in cls.__subclasses__():
                key = c._get_tag()
                cls._item_map[key] = c
        if long:
            raise NotImplementedError("Log items are not supported by this parser yet")

        if item_type is not None:
            if (tag & ~0x0F) > 0:
                raise ValueError("tag is not valid")
            tag = (tag << 4) | item_type.value

        if tag not in cls._item_map:
            raise ValueError("Unknown tag {0} ({1})".format(tag, hex(tag)))

        return cls._item_map[tag](data=data, long=long)


class Collection(IntEnum):
    physical = 0
    application = 1
    logical = 2
    report = 3
    named_array = 4
    usage_switch = 5
    usage_modifier = 6
