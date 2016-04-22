from enum import IntEnum
from array import array

# Toddo create a Enum like class that happily converts subclasses into byte arrays

class TagType(IntEnum):
    main = 0x00
    global_ = 0x04
    local = 0x08


class TagMain(IntEnum):
    input = 0x80
    output = 0x90
    feature = 0xB0
    collection = 0xA0
    end_collection = 0xC0


class TagGlobal(IntEnum):
    usage_page = 0x04
    logical_minimum = 0x14
    logical_maximum = 0x24
    physical_minimum = 0x34
    physical_maximum = 0x44
    unit_exponent = 0x54
    unit = 0x64
    report_size = 0x74
    report_id = 84
    report_count = 0x94
    push = 0xA4
    pop = 0xB4


class TagLocal(IntEnum):
    usage = 0x08
    usage_minimum = 0x18
    usage_maximum = 0x28
    designator_index = 0x38
    designator_maximum = 0x48
    designator_minimum = 0x58
    string_index = 0x78
    string_minimum = 0x88
    string_maximum = 0x98
    delimiter = 0xA8

class Collection(IntEnum):
    physical = 0
    application = 1
    logical = 2
    report = 3
    named_array = 4
    usage_switch = 5
    usage_modifier = 6

class Item:
    data = None # type: bytearray
    tag = None # type: TagMain | TagGlobal | TagLocal

    def __init__(self, tag: IntEnum, data: array, long: bool = False):
        if not long and not isinstance(tag, TagMain) and not isinstance(tag, TagGlobal) and not isinstance(tag, TagLocal):
            raise TypeError("tag is not an instance of <TagMain>, <TagGlobal> or <TagLocal>")
        self.tag = tag
        self.data = data

    def __repr__(self):
        return "<Item: {0}, {1}>".format(repr(self.tag),repr(self.data))
