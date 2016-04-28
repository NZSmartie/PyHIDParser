from hidparser import DeviceBuilder
from hidparser.Item import ItemType, Item, ValueItem

from hidparser.UsagePage import UsagePage


class UsagePageItem(ValueItem):
    usage_page = None

    def __init__(self, **kwargs):
        super(UsagePageItem, self).__init__(**kwargs)

        if len(self.data) not in [1,2]:
            raise ValueError("UsagePage has invalid length")

        self.usage_page = UsagePage.find_usage_page(self.value)

    def visit(self, descriptor: DeviceBuilder):
        descriptor.set_usage_page(UsagePage.find_usage_page(self.value))

    @classmethod
    def _get_tag(cls):
        return 0x04

    @classmethod
    def _get_type(cls):
        return ItemType.global_

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.usage_page.__name__)


class LogicalMinimumItem(ValueItem):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.set_logical_range(minimum=self.value)

    @classmethod
    def _get_tag(cls):
        return 0x14

    @classmethod
    def _get_type(cls):
        return ItemType.global_


class LogicalMaximumItem(ValueItem):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.set_logical_range(maximum=self.value)

    @classmethod
    def _get_tag(cls):
        return 0x24

    @classmethod
    def _get_type(cls):
        return ItemType.global_


class PhysicalMinimumItem(ValueItem):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.set_physical_range(minimum=self.value)

    @classmethod
    def _get_tag(cls):
        return 0x34

    @classmethod
    def _get_type(cls):
        return ItemType.global_


class PhysicalMaximumItem(ValueItem):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.set_physical_range(maximum=self.value)

    @classmethod
    def _get_tag(cls):
        return 0x44

    @classmethod
    def _get_type(cls):
        return ItemType.global_


class UnitExponentItem(ValueItem):

    @classmethod
    def _get_tag(cls):
        return 0x54

    @classmethod
    def _get_type(cls):
        return ItemType.global_


class UnitItem(Item):

    @classmethod
    def _get_tag(cls):
        return 0x64

    @classmethod
    def _get_type(cls):
        return ItemType.global_


class ReportSizeItem(ValueItem):

    def visit(self, descriptor: DeviceBuilder):
        descriptor.report_size = self.value

    @classmethod
    def _get_tag(cls):
        return 0x74

    @classmethod
    def _get_type(cls):
        return ItemType.global_


class ReportIdItem(ValueItem):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.set_report_id(self.value)

    @classmethod
    def _get_tag(cls):
        return 0x84

    @classmethod
    def _get_type(cls):
        return ItemType.global_


class ReportCountItem(ValueItem):

    def visit(self, descriptor: DeviceBuilder):
        descriptor.report_count = self.value

    @classmethod
    def _get_tag(cls):
        return 0x94

    @classmethod
    def _get_type(cls):
        return ItemType.global_


class PushItem(Item):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.push()

    @classmethod
    def _get_tag(cls):
        return 0xA4

    @classmethod
    def _get_type(cls):
        return ItemType.global_


class PopItem(Item):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.pop()

    @classmethod
    def _get_tag(cls):
        return 0xB4

    @classmethod
    def _get_type(cls):
        return ItemType.global_