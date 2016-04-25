from hidparser.UsagePage.UsagePage import UsagePage, UsageType, Usage


class Button(UsagePage):

    def __init__(self, value):
        self.value = Usage(value, [
            UsageType.data_selector,
            UsageType.control_on_off,
            UsageType.control_momentary,
            UsageType.control_one_shot
        ])
        self.index = self.value.value

    @classmethod
    def get_usage(cls, value):
        return Usage(value, [
            UsageType.data_selector,
            UsageType.control_on_off,
            UsageType.control_momentary,
            UsageType.control_one_shot
        ])

    @classmethod
    def _get_usage_page_index(cls):
        return 0x09
