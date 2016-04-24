from array import array as _array
from hidparser.helper import FlagEnum, EnumMask, Enum


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
    def from_bytes(cls, data: _array):
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
