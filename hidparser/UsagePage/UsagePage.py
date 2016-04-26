from enum import Enum as _Enum


class UsageType(_Enum):
    control_linear = ()
    control_on_off = ()
    control_momentary = ()
    control_one_shot = ()
    control_re_trigger = ()

    data_selector = ()
    data_static_value = ()
    data_static_flag = ()
    data_dynamic_value = ()
    data_dynamic_flag = ()

    collection_named_array = ()
    collection_application = ()
    collection_logical = ()
    collection_physical = ()
    collection_usage_switch = ()
    collection_usage_modifier = ()

    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    @classmethod
    def control_usage_types(cls):
        return (
            UsageType.control_linear,
            UsageType.control_on_off,
            UsageType.control_momentary,
            UsageType.control_one_shot,
            UsageType.control_re_trigger,
        )

    @classmethod
    def data_usage_types(cls):
        return (
            UsageType.data_selector,
            UsageType.data_static_value,
            UsageType.data_static_flag,
            UsageType.data_dynamic_value,
            UsageType.data_dynamic_flag,
        )

    @classmethod
    def collection_usage_types(cls):
        return (
            UsageType.collection_named_array,
            UsageType.collection_application,
            UsageType.collection_logical,
            UsageType.collection_physical,
            UsageType.collection_usage_switch,
            UsageType.collection_usage_modifier
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
    def __init__(self, usage_page: UsagePage.__class__):
        self.usage_page = usage_page
        self.minimum = None
        self.maximum = None

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
