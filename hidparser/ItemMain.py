from hidparser.Item import ItemType, Item
from hidparser.enums import CollectionType, ReportFlags, ReportType
from hidparser.DeviceBuilder import DeviceBuilder


class InputItem(Item):
    flags = None # type: ReportFlags

    def visit(self, descriptor: DeviceBuilder):
        descriptor.add_report(ReportType.input, self.flags)

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

    def visit(self, descriptor: DeviceBuilder):
        descriptor.add_report(ReportType.output, self.flags)

    @classmethod
    def _get_tag(cls):
        return 0x90

    @classmethod
    def _get_type(cls):
        return ItemType.main

    def __init__(self, **kwargs):
        super(OutputItem, self).__init__(**kwargs)

        self.flags = ReportFlags.from_bytes(self.data)

    def __repr__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, self.flags)


class FeatureItem(Item):
    flags = None

    def visit(self, descriptor: DeviceBuilder):
        descriptor.add_report(ReportType.feature, self.flags)

    @classmethod
    def _get_tag(cls):
        return 0xB0

    @classmethod
    def _get_type(cls):
        return ItemType.main

    def __init__(self, **kwargs):
        super(FeatureItem, self).__init__(**kwargs)

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

    def visit(self, descriptor: DeviceBuilder):
        if not isinstance(self.collection, CollectionType):
            raise ValueError("CollectionItem does not have a valid collection set")
        descriptor.push_collection(self.collection)

    def __init__(self, **kwargs):
        super(CollectionItem, self).__init__(**kwargs)

        if self.data is None or len(self.data) is not 1:
            raise ValueError("Collection must contain one byte of data")
        self.collection = CollectionType(self.data[0])

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.collection)


class EndCollectionItem(Item):
    def visit(self, descriptor: DeviceBuilder):
        descriptor.pop_collection()

    @classmethod
    def _get_tag(cls):
        return 0xC0

    @classmethod
    def _get_type(cls):
        return ItemType.main
