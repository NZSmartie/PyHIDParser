import usb
import hidparser


"""
This example will find a Sony Dual Shock 3 controller continuously print out the button states and thumb stick values
"""

if __name__ is not "__main__":
    exit()


class MyDevice:
    def __init__(self, interface: usb.core.Interface):
        # The usb device
        self.device = interface.device # type: usb.core.Device
        # The HID interface on the usb device
        self.interface = interface

        # locate the IN and OUT endpoints for the interface (typically interrupt, none may exist!)
        self.ep_in = None  # type: usb.core.Endpoint
        self.ep_out = None  # type: usb.core.Endpoint

        for ep in interface.endpoints():  #type: usb.core.Endpoint
            if ep.bEndpointAddress & 0x80:
                self.ep_in = ep
            else:
                self.ep_out = ep

        # Detatch the kernal driver, as it prevents our script from reading and writing
        if self.device.is_kernel_driver_active(interface.bInterfaceNumber):
            self.device.detach_kernel_driver(interface.bInterfaceNumber)

        # Request the HID Report Descriptor
        bmRequest = usb.util.build_request_type(
            direction=usb.util.CTRL_IN,
            type = usb.util.CTRL_TYPE_STANDARD,
            recipient=usb.util.CTRL_RECIPIENT_INTERFACE
        )

        data = self.device.ctrl_transfer(
            bmRequestType=bmRequest,
            bRequest=0x06, # GET_DESCRIPTOR
            wValue=0x2200, # Input Report Type
            wIndex=interface.bInterfaceNumber,
            data_or_wLength=1000  # Assume it's huge. TODO get descriptor size from device first
        )

        # Create a descriptor object from the device's HID Report Descriptor
        self.desc = hidparser.parse(data)

        # Find the largest report size for the input, output and feature reports
        self.max_input_size = max(
                [report_group.input_size for report_group in self.desc.reports.values()],
                default=0
        )
        self.max_output_size = max(
                [report_group.output_size for report_group in self.desc.reports.values()],
                default=0
        )
        self.max_feature_size = max(
                [report_group.feature_size for report_group in self.desc.reports.values()],
                default=0
        )

    def read_interrupt(self):
        try:
            # add 1 to size for Report ID byte
            data = bytes(self.ep_in.read(self.max_input_size + 1))
            self.desc.deserialize(data)
        except usb.core.USBError:
            pass

# Find all Sony devices
usb_devices = usb.core.find(
    find_all=True,
    custom_match=lambda dev: dev.idVendor == 0x054C and dev.idProduct == 0x0268
)

# Find all HID interfaces in usb_devices and create a MyDevice object
my_devices = [MyDevice(interface) for device in usb_devices
              for config in device.configurations()
              for interface in config
              if interface.bInterfaceClass == 3]


running = True

while running:
    # Loop through all our found devices
    for my_device in my_devices: # type: MyDevice

        my_device.read_interrupt()

        print("---")

        # Path to the buttons report
        buttons = my_device.desc.reports[1].inputs.joystick[0][1]
        thumb_sticks = my_device.desc.reports[1].inputs.joystick[0].pointer[0]


        print("Buttons: "
              + "".join(map(
                lambda value: "-" if value is 0 else "X", # Maps 0,1 to "-" or "X" repectively
                [int(value) for value in buttons.value]))
        )

        print("Thumb sticks: {: <4}, {: <4}, {: <4}, {: <4}".format(
            thumb_sticks.x,
            thumb_sticks.y,
            thumb_sticks.z,
            thumb_sticks.r_z
        ))
