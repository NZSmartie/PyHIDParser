# PyHIDParser

A python library for interpreting a HID descriptor to provide
an application with byte structures for reading and writing to without the manual labour.

## Pre-Alpha

At this stage, this library is still in early development and adoption is not recommended.

#### Progress

  - [x] Parse HID descriptor from byte array
  - [ ] Support for HID spec 1.11 items
    - [x] Main items (Collections, Inputs, Outputs and Features)
    - [ ] Global items
    - [ ] Local items
    - [ ] Support vender defined long items - ***low priority***
  - [ ] Create an application API for handing HID items - *Don't want the application developer to deal with states, nesting or closing collections, etc*
    - [ ] Find reports based on usages
    - [ ] Serialise/Deserialise reports to/from the HID device
    - [ ] Allow creating a HID descriptor from the API for configuring devices with

## Goals

  - Allow creating HID descriptors from byte arrays
  - Allow creating byte arrays from a HID descriptor
    - For those wanting an API approach to creating a descriptor
    - Or for anyone willing to create a new GUI tool
  - Provide a (de)serialiser for reading and writing to devices
  - Support adding vendor defined usage pages through API
  - Provide meta data about reports, such as physical descriptor index, usage switches/modifiers

## Example
***Node: this is a mockup example, not implemented yet***
```python
import hidparser

# ...

mouse = hidparser.parse(mouse_descriptor)
pointer = None

for report in mouse.reports:
    if hidparser.Usages.GenericDesktop.Pointer in report.usages:
        pointer = report
        break
if pointer is None:
    raise ValueError("mouse descriptor does not have a pointer report")

# ...

pointer.deserialise(report_data)
print("Mouse pointer: {}".format((pointer.x, pointer.y))
```
