from hidparser.Item import ItemType, Item


class UsagePageItem(Item):
    @classmethod
    def _get_tag(cls):
        return 0x04

    @classmethod
    def _get_type(cls):
        return ItemType.global_


class LogicalMinimumItem(Item):
    @classmethod
    def _get_tag(cls):
        return 0x14

    @classmethod
    def _get_type(cls):
        return ItemType.global_


class LogicalMaximumItem(Item):

    @classmethod
    def _get_tag(cls):
        return 0x24

    @classmethod
    def _get_type(cls):
        return ItemType.global_


class PhysicalMinimumItem(Item):

    @classmethod
    def _get_tag(cls):
        return 0x34

    @classmethod
    def _get_type(cls):
        return ItemType.global_


class PhysicalMaximumItem(Item):

    @classmethod
    def _get_tag(cls):
        return 0x44

    @classmethod
    def _get_type(cls):
        return ItemType.global_


class UnitExponentItem(Item):

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


class ReportSizeItem(Item):

    @classmethod
    def _get_tag(cls):
        return 0x74

    @classmethod
    def _get_type(cls):
        return ItemType.global_


class ReportIdItem(Item):

    @classmethod
    def _get_tag(cls):
        return 0x84

    @classmethod
    def _get_type(cls):
        return ItemType.global_


class ReportCountItem(Item):

    @classmethod
    def _get_tag(cls):
        return 0x94

    @classmethod
    def _get_type(cls):
        return ItemType.global_


class PushItem(Item):

    @classmethod
    def _get_tag(cls):
        return 0xA4

    @classmethod
    def _get_type(cls):
        return ItemType.global_


class PopItem(Item):

    @classmethod
    def _get_tag(cls):
        return 0xB4

    @classmethod
    def _get_type(cls):
        return ItemType.global_