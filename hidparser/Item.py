from enum import Enum, IntEnum
from array import array
from hidparser.helper import FlagEnum,EnumMask

# Toddo create a Enum like class that happily converts subclasses into byte arrays

from abc import ABCMeta as _ABCMeta
import struct as _struct


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
        return "<{}: {}>".format(self.__class__.__name__, repr(self.data))

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
    def create(cls, tag: int, item_type: ItemType = None, data: array.array = [], long: bool = False):
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


class ReportFlags(FlagEnum):
    constant = 0x01
    variable = 0x02
    relative = 0x04
    wrap = 0x08
    non_linear = 0x10
    no_preferred = 0x20
    null_state = 0x40
    # reserved = 0x80
    buffered_bytes = 0x100

    @classmethod
    def from_bytes(cls, data: array):
        result = 0
        if data is None:
            return EnumMask(cls,result)
        if len(data)>0:
            result |= data[0]
        if len(data)>1:
            result |= data[1] << 8

        return EnumMask(cls, result)

    @classmethod
    def __repr_members__(cls, value):
        return [
            "Data" if not value & ReportFlags.constant.value else "Constant",
            "Array" if not value & ReportFlags.variable.value else "Variable",
            "Absolute" if not value & ReportFlags.relative.value else "Relative",
            "No Wrap" if not value & ReportFlags.wrap.value else "Wrap",
            "Linear" if not value & ReportFlags.non_linear.value else "Non Linear",
            "Prefered State" if not value & ReportFlags.no_preferred.value else "No Prefered",
            "No Null position" if not value & ReportFlags.null_state.value else "Null state",
            "Bit Field" if not value & ReportFlags.buffered_bytes.value else "Buffered Bytes",
            ]


# TODO Support vendor defined functions
class Collection(Enum):
    physical = 0
    application = 1
    logical = 2
    report = 3
    named_array = 4
    usage_switch = 5
    usage_modifier = 6
