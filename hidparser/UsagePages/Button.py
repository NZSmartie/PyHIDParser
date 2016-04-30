from hidparser.UsagePage import UsagePage, UsageType, Usage


class Button(UsagePage):

    @classmethod
    def get_usage(cls, value):
        try:
            return cls._value2member_map_[value]
        except KeyError:
            return Button(value)

    @classmethod
    def _get_usage_page_index(cls):
        return 0x09


# Because Enum overrides the __new__ method in teh metaclass, so, it's getting overridden externally
def _create_button_usage(cls, value):
    if isinstance(value, Usage):
        return super(Button, cls).__new__(cls, value)
    if (value & ~0xFFFF) > 0:
        raise ValueError()
    button = Usage(value, [
        UsageType.data_selector,
        UsageType.control_on_off,
        UsageType.control_momentary,
        UsageType.control_one_shot
    ])
    button_enum = object.__new__(cls)
    button_enum._value_ = button
    button_enum._name_ = "button{}".format(value)
    button_enum.__objclass__ = cls
    button_enum.__init__(button)
    cls._member_names_.append(button_enum._name_)
    cls._member_map_[button_enum._name_] = button_enum
    cls._value2member_map_[value] = button_enum
    return button_enum

setattr(Button, "__new__", _create_button_usage)