import hidparser
from hidparser import Device, Report, ReportFlags
from hidparser.UsagePage import GenericDesktop, Button, UsageRange

from array import array

from hidparser.helper import ValueRange

mouse = array('B', [
    0x05, 0x01,  # USAGE_PAGE (Generic Desktop)
    0x09, 0x02,  # USAGE (Mouse)
    0xa1, 0x01,  # COLLECTION (Application)
    0x09, 0x01,  #   USAGE (Pointer)
    0xa1, 0x00,  #   COLLECTION (Physical)
    0x05, 0x09,  #     USAGE_PAGE (Button)
    0x19, 0x01,  #     USAGE_MINIMUM (Button 1)
    0x29, 0x03,  #     USAGE_MAXIMUM (Button 3)
    0x15, 0x00,  #     LOGICAL_MINIMUM (0)
    0x25, 0x01,  #     LOGICAL_MAXIMUM (1)
    0x95, 0x03,  #     REPORT_COUNT (3)
    0x75, 0x01,  #     REPORT_SIZE (1)
    0x81, 0x02,  #     INPUT (Data,Var,Abs)
    0x95, 0x01,  #     REPORT_COUNT (1)
    0x75, 0x05,  #     REPORT_SIZE (5)
    0x81, 0x03,  #     INPUT (Cnst,Var,Abs)
    0x05, 0x01,  #     USAGE_PAGE (Generic Desktop)
    0x09, 0x30,  #     USAGE (X)
    0x09, 0x31,  #     USAGE (Y)
    0x15, 0x81,  #     LOGICAL_MINIMUM (-127)
    0x25, 0x7f,  #     LOGICAL_MAXIMUM (127)
    0x75, 0x08,  #     REPORT_SIZE (8)
    0x95, 0x02,  #     REPORT_COUNT (2)
    0x81, 0x06,  #     INPUT (Data,Var,Rel)
    0xc0,        #   END_COLLECTION
    0xc0         # END_COLLECTION
    ])

if __name__ is '__main__':
    # Todo return a more useful Device object instead of a "builder"
    # This returns a DescriptorBuilder
    descriptor = hidparser.parse(mouse)

    # Create a mouse device through API instead of parsing bytes
    mouse_device = Device()

    # TODO accessing the collections by Usage could be cleaned up some how
    # Index 0 is used as a fallback when no ReportID Items are used
    # otherwise, Report ID must start at 1
    mouse_device[0].inputs.append(GenericDesktop.mouse)
    mouse_device[0].inputs.mouse.append(GenericDesktop.pointer)
    mouse_device[0].inputs.mouse.pointer.extend([
        Report(
            usages=UsageRange(
                minimum=Button(1),
                maximum=Button(3)
            ).get_range(),
            size=1,
            count=3,
            logical_range=ValueRange(0, 1),
            flags=ReportFlags.variable
        ),
        Report(
            usages=[],
            size=5,
            count=1,
            flags=ReportFlags.constant | ReportFlags.variable
        ),
        Report(
            usages=[
                GenericDesktop.x,
                GenericDesktop.y
            ],
            size=8,
            count=2,
            logical_range=ValueRange(-127, 127),
            flags=ReportFlags.variable | ReportFlags.relative
        )
    ])

    # TODO Read from device and deserialize with mouse_device. Something like:
    # mouse_device.deserialize(bytes([0x00, 0x12, 0x34]))

    # Read x,y from mouse
    pointer = mouse_device[0].inputs.mouse.pointer
    print("pointer: {}, {}".format(pointer.x, pointer.y))

    # TODO Create an example device with outputs and features

    pass
