from hidparser.Item import Item, ItemType


class UsageItem(Item):
    @classmethod
    def _get_tag(cls):
        return 0x08

    @classmethod
    def _get_type(cls):
        return ItemType.local


class UsageMinimumItem(Item):
    @classmethod
    def _get_tag(cls):
        return 0x18

    @classmethod
    def _get_type(cls):
        return ItemType.local


class UsageMaximumItem(Item):
    @classmethod
    def _get_tag(cls):
        return 0x28

    @classmethod
    def _get_type(cls):
        return ItemType.local


class DesignatorIndexItem(Item):
    @classmethod
    def _get_tag(cls):
        return 0x38

    @classmethod
    def _get_type(cls):
        return ItemType.local


class DesignatorMaximumItem(Item):
    @classmethod
    def _get_tag(cls):
        return 0x48

    @classmethod
    def _get_type(cls):
        return ItemType.local


class DesignatorMinimumItem(Item):
    @classmethod
    def _get_tag(cls):
        return 0x58

    @classmethod
    def _get_type(cls):
        return ItemType.local


class StringIndexItem(Item):
    @classmethod
    def _get_tag(cls):
        return 0x78

    @classmethod
    def _get_type(cls):
        return ItemType.local


class StringMinimumItem(Item):
    @classmethod
    def _get_tag(cls):
        return 0x88

    @classmethod
    def _get_type(cls):
        return ItemType.local


class StringMaximumItem(Item):
    @classmethod
    def _get_tag(cls):
        return 0x98

    @classmethod
    def _get_type(cls):
        return ItemType.local


class DelimiterItem(Item):
    @classmethod
    def _get_tag(cls):
        return 0xA8

    @classmethod
    def _get_type(cls):
        return ItemType.local

