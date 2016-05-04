# PyHIDParser
#### V0.0.6

A python library for interpreting a HID descriptor to provide
an application with byte structures for reading and writing to without the manual labour.

#### Pre-Alpha

At this stage, this library is still in early development and adoption is not recommended.

#### Progress

  - [x] Parse HID descriptor from byte array
  - [ ] Support for HID spec 1.11 items *(See Issue [#1](https://github.com/NZSmartie/PyHIDParser/issues/1))*
    - [x] Main items (Collections, Inputs, Outputs and Features)
    - [ ] Global items *(missing `unit` and `unit exponent`)*
    - [ ] Local items *(missing `string index/maximum/minimum` and  delimiter`)*
    - [ ] ~~Support vender defined long items~~ *(not going to happen any time soon)*
  - [x] Create an application API for handing HID items - *Don't want the application developer to deal with states, nesting or closing collections, etc*
    - [x] Access reports based on usages
    - [x] Serialize/Deserialize reports to/from the HID device
    - [x] Allow creating a HID descriptor from the API for configuring devices with

## Goals

  - Allow creating HID descriptors from byte arrays
  - Allow creating byte arrays from a HID descriptor
    - For those wanting an API approach to creating a descriptor
    - Or for anyone willing to create a new GUI tool
  - Provide a (de)serializer for reading and writing to devices
  - Support adding vendor defined usage pages through API
  - Provide meta data about reports, such as physical descriptor index, usage switches/modifiers

## Examples

More examples int the [examples/](examples/) folder:
 - [mouse.py](examples/mouse.py) - Creating the example Mouse descriptor from the HID 1.11 spec
 - [dual-shock-3.py](examples/dual-shock-3.py)  - Parse Sony's DualShock3 HID descriptor

*Note: This is a ***working*** example. But it is subject to change*
```python
import hidparser
from hidparser.UsagePages import GenericDesktop, Button

# ...

mouse_desc = array('B', [
    0x05, 0x01,  # USAGE_PAGE (Generic Desktop)
    0x09, 0x02,  # USAGE (Mouse)
    0xa1, 0x01,  # COLLECTION (Application)
    # ...
    0xc0         # END_COLLECTION
    ])

# This returns a Device object from a descriptor
mouse_from_desc = hidparser.parse(mouse)

# Alternatively, create a mouse device through API instead of parsing bytes
mouse_from_api = hidparser.Device(
    hidparser.Collection(
        usage=GenericDesktop.MOUSE,
        items=hidparser.Collection(
            usage=GenericDesktop.POINTER,
            items=[
                hidparser.Report(
                    report_type=hidparser.ReportType.INPUT,
                    usages=hidparser.UsageRange(
                        minimum=Button(1),
                        maximum=Button(3)
                    ).get_range(),
                    size=1,
                    count=3,
                    logical_range=(0, 1),
                    flags=hidparser.ReportFlags.VARIABLE
                ),
                hidparser.Report(
                    report_type=hidparser.ReportType.INPUT,
                    usages=[],
                    size=5,
                    count=1,
                    flags=hidparser.ReportFlags.CONSTANT | hidparser.ReportFlags.VARIABLE
                ),
                hidparser.Report(
                    report_type=hidparser.ReportType.INPUT,
                    usages=[
                        GenericDesktop.X,
                        GenericDesktop.Y
                    ],
                    size=8,
                    count=2,
                    logical_range=(-127, 127),
                    flags=hidparser.ReportFlags.VARIABLE | hidparser.ReportFlags.RELATIVE
                )
            ]
        )
    )
)

# Read from the physical device
data = bytes([0x00, 0x12, 0x34])
# Deserialize the data and populate the object members
mouse_from_api.deserialize(data)

# Read the x,y members from mouse after deserializing
pointer = mouse_from_api.reports[0].inputs.mouse.pointer
print("pointer: {}, {}".format(pointer.x, pointer.y))
# Example Output:
# pointer: 18, 52

```
