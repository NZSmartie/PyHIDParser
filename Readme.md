# PyHIDParser
#### V0.0.3

A python library for interpreting a HID descriptor to provide
an application with byte structures for reading and writing to without the manual labour.

#### Pre-Alpha

At this stage, this library is still in early development and adoption is not recommended.

#### Progress

  - [x] Parse HID descriptor from byte array
  - [ ] Support for HID spec 1.11 items
    - [x] Main items (Collections, Inputs, Outputs and Features)
    - [ ] Global items *(missing `unit` and `unit exponent`)*
    - [ ] Local items *(missing `designator index/maximum/minimum`, `string index/maximum/minimum` and  delimiter`)*
    - [ ] ~~Support vender defined long items~~ *(not going to happen any time soon)*
  - [x] Create an application API for handing HID items - *Don't want the application developer to deal with states, nesting or closing collections, etc*
    - [x] Access reports based on usages
    - [ ] Serialize/Deserialize reports to/from the HID device
    - [x] Allow creating a HID descriptor from the API for configuring devices with

## Goals

  - Allow creating HID descriptors from byte arrays
  - Allow creating byte arrays from a HID descriptor
    - For those wanting an API approach to creating a descriptor
    - Or for anyone willing to create a new GUI tool
  - Provide a (de)serializer for reading and writing to devices
  - Support adding vendor defined usage pages through API
  - Provide meta data about reports, such as physical descriptor index, usage switches/modifiers

## Example
***Note: this is mostly a mockup example. It is subject to change***
```python
import hidparser
from hidparser import Device, Report, ReportFlags
from hidparser.UsagePage import GenericDesktop, Button, UsageRange
from hidparser.helper import ValueRange

# ...

mouse_desc = array('B', [
    0x05, 0x01,  # USAGE_PAGE (Generic Desktop)
    0x09, 0x02,  # USAGE (Mouse)
    0xa1, 0x01,  # COLLECTION (Application)
    # ...
    0xc0         # END_COLLECTION
    ])

# This returns a Device
mouse_from_desc = hidparser.parse(mouse_desc)

# Alternatively, create a mouse device through API instead of parsing bytes
mouse_from_api = Device()

# Index 0 is used as a fallback when no ReportID Items are used
# otherwise, Report ID must start at 1
mouse_from_api[0].inputs.append(GenericDesktop.mouse)
mouse_from_api[0].inputs.mouse.append(GenericDesktop.pointer)
mouse_from_api[0].inputs.mouse.pointer.extend([
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

mouse_from_api.deserialize(bytes([0x00, 0x12, 0x34]))

# Read x,y from mouse
pointer = mouse_from_api[0].inputs.mouse.pointer
print("pointer: {}, {}".format(pointer.x, pointer.y))
# pointer: 18, 52

```
