from hidparser import DeviceBuilder
from hidparser.Item import ItemType, Item, ValueItem
from hidparser.Unit import Unit as _Unit
from hidparser.UsagePage import UsagePage


class UsagePageItem(ValueItem):
    usage_page = None

    def __init__(self, *args, **kwargs):
        kwargs["signed"] = False
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
        return ItemType.GLOBAL

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
        return ItemType.GLOBAL


class LogicalMaximumItem(ValueItem):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.set_logical_range(maximum=self.value)

    @classmethod
    def _get_tag(cls):
        return 0x24

    @classmethod
    def _get_type(cls):
        return ItemType.GLOBAL


class PhysicalMinimumItem(ValueItem):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.set_physical_range(minimum=self.value)

    @classmethod
    def _get_tag(cls):
        return 0x34

    @classmethod
    def _get_type(cls):
        return ItemType.GLOBAL


class PhysicalMaximumItem(ValueItem):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.set_physical_range(maximum=self.value)

    @classmethod
    def _get_tag(cls):
        return 0x44

    @classmethod
    def _get_type(cls):
        return ItemType.GLOBAL


class UnitExponentItem(ValueItem):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.unit_exponent = self.value

    @classmethod
    def _get_tag(cls):
        return 0x54

    @classmethod
    def _get_type(cls):
        return ItemType.GLOBAL


class UnitItem(Item):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.unit = _Unit.from_bytes(self.data)

    @classmethod
    def _get_tag(cls):
        return 0x64

    @classmethod
    def _get_type(cls):
        return ItemType.GLOBAL


class ReportSizeItem(ValueItem):
    def __init__(self, *args, **kwargs):
        kwargs["signed"] = False
        super(ReportSizeItem, self).__init__(*args, **kwargs)

    def visit(self, descriptor: DeviceBuilder):
        descriptor.report_size = self.value

    @classmethod
    def _get_tag(cls):
        return 0x74

    @classmethod
    def _get_type(cls):
        return ItemType.GLOBAL


class ReportIdItem(ValueItem):
    def __init__(self, *args, **kwargs):
        kwargs["signed"] = False
        super(ReportIdItem, self).__init__(*args, **kwargs)

    def visit(self, descriptor: DeviceBuilder):
        descriptor.set_report_id(self.value)

    @classmethod
    def _get_tag(cls):
        return 0x84

    @classmethod
    def _get_type(cls):
        return ItemType.GLOBAL


class ReportCountItem(ValueItem):
    def __init__(self, *args, **kwargs):
        kwargs["signed"] = False
        super(ReportCountItem, self).__init__(*args, **kwargs)

    def visit(self, descriptor: DeviceBuilder):
        descriptor.report_count = self.value

    @classmethod
    def _get_tag(cls):
        return 0x94

    @classmethod
    def _get_type(cls):
        return ItemType.GLOBAL


class PushItem(Item):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.push()

    @classmethod
    def _get_tag(cls):
        return 0xA4

    @classmethod
    def _get_type(cls):
        return ItemType.GLOBAL


class PopItem(Item):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.pop()

    @classmethod
    def _get_tag(cls):
        return 0xB4

    @classmethod
    def _get_type(cls):
        return ItemType.GLOBAL