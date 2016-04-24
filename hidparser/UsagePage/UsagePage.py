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


class UsagePage:
    def __init__(self, item):
        if isinstance(item, Usage):
            self.index = item.value & 0xFFFF
            self.value = item
        else:
            for attr in dir(self):
                member = self.__getattribute__(attr) # type: Usage
                if not isinstance(member, Usage):
                    continue
                if member.value == item:
                    self.index = member.value & 0xFFFF
                    self.value = member
                    return
        raise ValueError("{} is not a valid {}".format(item.__name__, self.__class__.__name__))

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

