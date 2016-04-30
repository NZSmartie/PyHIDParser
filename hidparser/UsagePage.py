from enum import Enum as _Enum


class UsageType(_Enum):
    CONTROL_LINEAR = ()
    CONTROL_ON_OFF = ()
    CONTROL_MOMENTARY = ()
    CONTROL_ONE_SHOT = ()
    CONTROL_RE_TRIGGER = ()

    DATA_SELECTOR = ()
    DATA_STATIC_VALUE = ()
    DATA_STATIC_FLAG = ()
    DATA_DYNAMIC_VALUE = ()
    DATA_DYNAMIC_FLAG = ()

    COLLECTION_NAMED_ARRAY = ()
    COLLECTION_APPLICATION = ()
    COLLECTION_LOGICAL = ()
    COLLECTION_PHYSICAL = ()
    COLLECTION_USAGE_SWITCH = ()
    COLLECTION_USAGE_MODIFIER = ()

    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    @classmethod
    def control_usage_types(cls):
        return (
            UsageType.CONTROL_LINEAR,
            UsageType.CONTROL_ON_OFF,
            UsageType.CONTROL_MOMENTARY,
            UsageType.CONTROL_ONE_SHOT,
            UsageType.CONTROL_RE_TRIGGER,
        )

    @classmethod
    def data_usage_types(cls):
        return (
            UsageType.DATA_SELECTOR,
            UsageType.DATA_STATIC_VALUE,
            UsageType.DATA_STATIC_FLAG,
            UsageType.DATA_DYNAMIC_VALUE,
            UsageType.DATA_DYNAMIC_FLAG,
        )

    @classmethod
    def collection_usage_types(cls):
        return (
            UsageType.COLLECTION_NAMED_ARRAY,
            # UsageType.collection_application, # Commented out as it is used for top level collections only
            UsageType.COLLECTION_LOGICAL,
            UsageType.COLLECTION_PHYSICAL,
            UsageType.COLLECTION_USAGE_SWITCH,
            UsageType.COLLECTION_USAGE_MODIFIER
        )

class Usage:
    def __init__(self, value, usage_types):
        if not isinstance(usage_types, list):
            usage_types = [usage_types,]
        for usage_type in usage_types:
            if not isinstance(usage_type, UsageType):
                raise ValueError("usage_type {} is not instance of {}".format(
                    usage_type.__class__.__name__,
                    UsageType.__name__)
                )
        self.value = value
        self.usage_types = usage_types


class UsagePage(_Enum):
    def __init__(self, item):
        if not isinstance(item, Usage):
            raise ValueError("{} is not a valid {}".format(item.__name__, self.__class__.__name__))
        self.index = item.value & 0xFFFF
        self.usage = item
        self.usage_types = item.usage_types

    @classmethod
    def get_usage(cls, value):
        for key, member in cls.__members__.items():
            if not isinstance(member.value, Usage):
                continue
            if member.index == value:
                return member
        raise ValueError("{} is not a valid {}".format(value, cls.__name__))

    @classmethod
    def _get_usage_page_index(cls):
        raise NotImplementedError()

    @classmethod
    def find_usage_page(cls, value):
        if not hasattr(cls, "usage_page_map"):
            cls.usage_page_map = {usage_page._get_usage_page_index(): usage_page for usage_page in cls.__subclasses__()}
        if value in cls.usage_page_map.keys():
            return cls.usage_page_map[value]
        if value not in range(0xFF00,0xFFFF):
            raise ValueError("Reserved or missing usage page 0x{:04X}".format(value))
        return None


class UsageRange:
    def __init__(self, usage_page: UsagePage.__class__ = None, minimum = None, maximum = None):
        self.usage_page = usage_page
        self.minimum = minimum
        self.maximum = maximum

    def get_range(self):
        if self.minimum is None or self.maximum is None:
            raise ValueError("Usage Minimum and Usage Maximum must be set")
        if isinstance(self.minimum, UsagePage):
            if not isinstance(self.maximum, UsagePage):
                raise ValueError("UsageRange type mismatch in minimum and maximum usages")
            self.usage_page = self.minimum.__class__
            return [self.usage_page.get_usage(value) for value in range(self.minimum.index & 0xFFFF, (self.maximum.index & 0xFFFF) + 1)]
        if self.minimum & ~0xFFFF:
            self.usage_page = UsagePage.find_usage_page((self.minimum & ~0xFFFF) >> 16)
        return [self.usage_page.get_usage(value) for value in range(self.minimum & 0xFFFF, (self.maximum & 0xFFFF) + 1)]
