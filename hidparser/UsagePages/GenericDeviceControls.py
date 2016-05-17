from hidparser.UsagePage import Usage, UsagePage, UsageType


class GenericDeviceControls(UsagePage):

    BATTERY_STRENGTH = Usage(0x20,UsageType.DATA_DYNAMIC_VALUE)
    WIRELESS_CHANNEL = Usage(0x21,UsageType.DATA_DYNAMIC_VALUE)
    WIRELESS_ID = Usage(0x21,UsageType.DATA_DYNAMIC_VALUE)
    DISCOVER_WIRELESS_CONTROL = Usage(0x23,UsageType.CONTROL_ONE_SHOT)
    SECURITY_CODE_CHARACTER_ENTERED = Usage(0x24,UsageType.CONTROL_ONE_SHOT)
    SECURITY_CODE_CHARACTER_ERASED = Usage(0x25,UsageType.CONTROL_ONE_SHOT)
    SECURITY_CODE_CLEARED = Usage(0x26,UsageType.CONTROL_ONE_SHOT)

    # HID Usage Table Request 61: Version Information Usages
    SOFTWARE_VERSION = Usage(0x2A,UsageType.COLLECTION_LOGICAL)
    PROTOCOL_VERSION = Usage(0x2B,UsageType.COLLECTION_LOGICAL)
    HARDWARE_VERSION = Usage(0x2C, UsageType.COLLECTION_LOGICAL)
    MAJOR = Usage(0x2D,UsageType.DATA_STATIC_VALUE)
    MINOR = Usage(0x2E,UsageType.DATA_STATIC_VALUE)
    REVISION = Usage(0x2F,UsageType.DATA_STATIC_VALUE)

    @classmethod
    def _get_usage_page_index(cls):
        return 0x06
