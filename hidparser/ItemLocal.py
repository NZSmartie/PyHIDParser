from hidparser.DeviceBuilder import DeviceBuilder
from hidparser.Item import Item, ItemType, ValueItem


class UsageItem(ValueItem):

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
    @classmethod
    def _get_tag(cls):
        return 0x38

    @classmethod
    def _get_type(cls):
        return ItemType.LOCAL


class DesignatorMaximumItem(ValueItem):
    @classmethod
    def _get_tag(cls):
        return 0x48

    @classmethod
    def _get_type(cls):
        return ItemType.LOCAL


class DesignatorMinimumItem(ValueItem):
    @classmethod
    def _get_tag(cls):
        return 0x58

    @classmethod
    def _get_type(cls):
        return ItemType.LOCAL


class StringIndexItem(ValueItem):
    @classmethod
    def _get_tag(cls):
        return 0x78

    @classmethod
    def _get_type(cls):
        return ItemType.LOCAL


class StringMinimumItem(ValueItem):
    @classmethod
    def _get_tag(cls):
        return 0x88

    @classmethod
    def _get_type(cls):
        return ItemType.LOCAL


class StringMaximumItem(ValueItem):
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

