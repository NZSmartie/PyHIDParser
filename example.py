import hidparser
from hidparser import DescriptorBuilder, CollectionType, ReportType, ReportFlags
from hidparser.UsagePage import GenericDesktop, Button

from array import array

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
    # Todo return a Descriptor object instead of a builder
    # This actually returns a DescriptorBuilder
    descriptor = hidparser.parse(mouse)
    mouse_device = descriptor.build()

    # Create a mouse descriptor through API
    mouse_builder = DescriptorBuilder()
    mouse_builder.add_usage(GenericDesktop.mouse)
    mouse_builder.push_collection(CollectionType.application)
    mouse_builder.add_usage(GenericDesktop.pointer)
    mouse_builder.push_collection(CollectionType.physical)
    mouse_builder.set_usage_range(Button(1), Button(3))
    mouse_builder.set_logical_range(0,1)
    mouse_builder.report_count = 3
    mouse_builder.report_size = 1
    mouse_builder.add_report(ReportType.input, ReportFlags.variable)
    mouse_builder.report_count = 1
    mouse_builder.report_size = 5
    mouse_builder.add_report(ReportType.input, ReportFlags.constant | ReportFlags.variable)
    mouse_builder.add_usage(GenericDesktop.x)
    mouse_builder.add_usage(GenericDesktop.y)
    mouse_builder.set_logical_range(-127,127)
    mouse_builder.report_count = 2
    mouse_builder.report_size = 8
    mouse_builder.add_report(ReportType.input, ReportFlags.variable | ReportFlags.relative)
    pass
