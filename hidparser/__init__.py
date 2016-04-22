from hidparser.Item import Item, TagType, TagMain, TagGlobal, TagLocal

def parse(data):
    import array

    if isinstance(data, bytes):
        data = array.array('B', data)

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
                yield Item(tag, get_bytes(byte_iter, size), True)

            # Short item's size is the first two bits (eitehr 0,1,2 or 4)
            size = item & 0x03
            if size is 3:
                size = 4

            # Get the item tag type from bits 3 - 2
            tag = item & 0x0C
            if tag is TagType.main.value:
                tag = TagMain(item & 0xFC)
            elif tag is TagType.global_.value:
                tag = TagGlobal(item & 0xFC)
            elif tag is TagType.local.value:
                tag = TagLocal(item & 0xFC)
            else:
                raise ValueError("Invalid bType in short item")

            # Yield a short item
            yield Item(tag, get_bytes(byte_iter, size))

        except StopIteration:
            break
    pass
        