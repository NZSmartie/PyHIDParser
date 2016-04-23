from hidparser.Item import ItemType, Item


class InputItem(Item):
    @classmethod
    def _get_tag(cls):
        return 0x80

    @classmethod
    def _get_type(cls):
        return ItemType.main


class OutputItem(Item):
    @classmethod
    def _get_tag(cls):
        return 0x90

    @classmethod
    def _get_type(cls):
        return ItemType.main


class FeatureItem(Item):
    @classmethod
    def _get_tag(cls):
        return 0xB0

    @classmethod
    def _get_type(cls):
        return ItemType.main


class CollectionItem(Item):
    @classmethod
    def _get_tag(cls):
        return 0xA0

    @classmethod
    def _get_type(cls):
        return ItemType.main


class EndCollectionItem(Item):
    @classmethod
    def _get_tag(cls):
        return 0xC0

    @classmethod
    def _get_type(cls):
        return ItemType.main
