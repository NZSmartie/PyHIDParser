from hidparser.DeviceBuilder import DeviceBuilder
from hidparser.Item import Item, ItemType, ValueItem


class UsageItem(ValueItem):
    def __init__(self, *args, **kwargs):
        kwargs["signed"] = False
        super(UsageItem, self).__init__(*args, **kwargs)

    def visit(self, descriptor: DeviceBuilder):
        descriptor.add_usage(self.value)

    @classmethod
    def _get_tag(cls):
        return 0x08

    @classmethod
    def _get_type(cls):
        return ItemType.LOCAL


class UsageMinimumItem(ValueItem):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.set_usage_range(minimum=self.value)

    @classmethod
    def _get_tag(cls):
        return 0x18

    @classmethod
    def _get_type(cls):
        return ItemType.LOCAL


class UsageMaximumItem(ValueItem):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.set_usage_range(maximum=self.value)

    @classmethod
    def _get_tag(cls):
        return 0x28

    @classmethod
    def _get_type(cls):
        return ItemType.LOCAL


class DesignatorIndexItem(ValueItem):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.set_designator_range(minimum=self.value, maximum=self.value)

    @classmethod
    def _get_tag(cls):
        return 0x38

    @classmethod
    def _get_type(cls):
        return ItemType.LOCAL


class DesignatorMaximumItem(ValueItem):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.set_designator_range(maximum=self.value)

    @classmethod
    def _get_tag(cls):
        return 0x48

    @classmethod
    def _get_type(cls):
        return ItemType.LOCAL


class DesignatorMinimumItem(ValueItem):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.set_designator_range(minimum=self.value)

    @classmethod
    def _get_tag(cls):
        return 0x58

    @classmethod
    def _get_type(cls):
        return ItemType.LOCAL


class StringIndexItem(ValueItem):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.set_string_range(minimum=self.value, maximum=self.value)

    @classmethod
    def _get_tag(cls):
        return 0x78

    @classmethod
    def _get_type(cls):
        return ItemType.LOCAL


class StringMinimumItem(ValueItem):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.set_string_range(minimum=self.value)

    @classmethod
    def _get_tag(cls):
        return 0x88

    @classmethod
    def _get_type(cls):
        return ItemType.LOCAL


class StringMaximumItem(ValueItem):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.set_string_range(maximum=self.value)

    @classmethod
    def _get_tag(cls):
        return 0x98

    @classmethod
    def _get_type(cls):
        return ItemType.LOCAL


class DelimiterItem(Item):
    @classmethod
    def _get_tag(cls):
        return 0xA8

    @classmethod
    def _get_type(cls):
        return ItemType.LOCAL

