from hidparser.Item import Item, ItemType
from hidparser.ItemMain import *
from hidparser.ItemGlobal import *
from hidparser.ItemLocal import *

from hidparser.DeviceBuilder import DeviceBuilder
from hidparser.Device import Device, Collection, ReportGroup, Report

from hidparser.UsagePage import UsagePage, Usage, UsageRange, UsageType
import hidparser.UsagePages as UsagePages

def parse(data):
    items = get_items(data)

    descriptor_builder = DeviceBuilder()
    for item in items:
        print(item)
        item.visit(descriptor_builder)

    return Device(reports=descriptor_builder.reports)


def get_items(data):
    import array

    if isinstance(data, bytes):
        data = array.array('B', data)

    # grab the next len bytes and return an array from the iterator
    get_bytes = lambda it, len: [next(it) for x in range(len)]

    byte_iter = iter(data)
    while True:
        try:
            item = next(byte_iter)
            # Check if the item is "Long"
            if item is 0xFE:
                size = next(byte_iter)
                tag = next(byte_iter)
                if tag not in range(0xF0, 0xFF):
                    raise ValueError("Long Items are only supported by Vender defined tags as of Version 1.11")
                # Yield a long item, There are no tags defined in HID as of Version 1.11
                yield Item(tag=tag, data=get_bytes(byte_iter, size), long=True)

            # Short item's size is the first two bits (eitehr 0,1,2 or 4)
            size = item & 0x03
            if size is 3:
                size = 4

            # Get the item tag type from bits 3 - 2
            item_type = ItemType(item & 0x0C)
            if item_type is ItemType.reserved:
                raise ValueError("Invalid bType in short item")

            yield Item.create(tag=item & 0xFC, data=get_bytes(byte_iter, size))

        except StopIteration:
            break
    pass
