from hidparser.Item import ItemType, Item, Collection, ReportFlags


class InputItem(Item):
    flags = None # type: ReportFlags

    @classmethod
    def _get_tag(cls):
        return 0x80

    @classmethod
    def _get_type(cls):
        return ItemType.main

    def __init__(self, **kwargs):
        super(InputItem, self).__init__(**kwargs)

        self.flags = ReportFlags.from_bytes(self.data)

    def __repr__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, self.flags)

class OutputItem(Item):
    flags = None

    @classmethod
    def _get_tag(cls):
        return 0x90

    @classmethod
    def _get_type(cls):
        return ItemType.main

    def __init__(self, **kwargs):
        super(InputItem, self).__init__(**kwargs)

        self.flags = ReportFlags.from_bytes(self.data)

    def __repr__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, self.flags)


class FeatureItem(Item):
    flags = None

    @classmethod
    def _get_tag(cls):
        return 0xB0

    @classmethod
    def _get_type(cls):
        return ItemType.main

    def __init__(self, **kwargs):
        super(InputItem, self).__init__(**kwargs)

        self.flags = ReportFlags.from_bytes(self.data)

    def __repr__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, self.flags)


class CollectionItem(Item):
    collection = None

    @classmethod
    def _get_tag(cls):
        return 0xA0

    @classmethod
    def _get_type(cls):
        return ItemType.main

    def __init__(self, **kwargs):
        super(CollectionItem, self).__init__(**kwargs)

        if self.data is None or len(self.data) is not 1:
            raise ValueError("Collection must contain one byte of data")
        self.collection = Collection(self.data[0])

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.collection)


class EndCollectionItem(Item):
    @classmethod
    def _get_tag(cls):
        return 0xC0

    @classmethod
    def _get_type(cls):
        return ItemType.main
