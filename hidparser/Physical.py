from enum import Enum as _Enum
import struct as _struct


class Bias(_Enum):
    NOT_APPLICABLE = 0
    RIGHT_HAND = 1
    LEFT_HAND = 2
    BOTH_HANDS = 3
    EITHER_HAND = 4


class Qualifier(_Enum):
    NOT_APPLICABLE = 0
    RIGHT = 1
    LEFT = 2
    BOTH = 3
    EITHER = 4
    CENTER = 5


class Designator(_Enum):
    NONE = 0x00
    HAND = 0x01
    EYEBALL = 0x02
    EYEBROW = 0x03
    EYELID = 0x04
    EAR = 0x05
    NOSE = 0x06
    MOUTH = 0x07
    UPPER_LIP = 0x08
    LOWER_LIP = 0x09
    JAW = 0x0A
    NECK = 0x0B
    UPPER_ARM = 0x0C
    ELBOW = 0x0D
    FOREARM = 0x0E
    WRIST = 0x0F
    PALM = 0x10
    THUMB = 0x11
    INDEX_FINGER = 0x12
    MIDDLE_FINGER = 0x13
    RING_FINGER = 0x14
    LITTLE_FINGER = 0x15
    HEAD = 0x16
    SHOULDER = 0x17
    HIP = 0x18
    WAIST = 0x19
    THIGH = 0x1A
    KNEE = 0x1B
    CALF = 0x1C
    ANKLE = 0x1D
    FOOT = 0x1E
    HEEL = 0x1F
    BALL_OF_FOOT = 0x20
    BIG_TOE = 0x21
    SECOND_TOE = 0x22
    THIRD_TOE = 0x23
    FOURTH_TOE = 0x24
    LITTLE_TOE = 0x25
    BROW = 0x26
    CHEEK = 0x27


class PhysicalDescriptor:
    def __init__(self, designator: Designator, qualifier: Qualifier, effort: int=0):
        self.designator = designator
        self.qualifier = qualifier
        self.effort = effort


class PhysicalDescriptorSet:
    _total = 0
    _length = 0
    _sets = {}  # type: Dict[int, PhysicalDescriptorSet]

    @classmethod
    def get_descriptor_by_index(cls, index):
        return cls._sets[index]

    @classmethod
    def parse(cls, index, data):
        data = bytes(data)
        if index is 0:
            if len(data) != 3:
                raise ValueError("Physical descriptor at index 0 is 3 bytes in size")
            cls._total, cls._length = _struct.unpack("<BH",data)
            return
        if cls._length is 0:
            raise ValueError("Please parse the Physical Descriptor Set at index 0 first")
        if index > cls._total:
            raise IndexError("index({:d}) is out of bounds".format(index))
        if index in cls._sets.keys():
            del cls._sets[index]
        bias = Bias((data[0] & 0xE0) >> 5)
        preference = data[0] & 0x1F
        pdset = PhysicalDescriptorSet(index, bias, preference)
        for i in range(cls._length):
            offset = (i * 2) + 1
            designator, flags = _struct.unpack("<BB",data[offset:offset+2])
            pdset.append(PhysicalDescriptor(
                Designator(designator),
                Qualifier((flags & 0xE0) >> 5),
                flags & 0x1F
            ))

    @classmethod
    def get_total(cls):
        return cls._total

    def __init__(self, index, bias: Bias, preference: int=0, descriptors=None):
        if type(index) is not int or index in self._sets.keys():
            raise IndexError("Invalid index for PhysicalDescriptorSet")
        self.index = index
        self.bias = bias,
        if not 0 <= preference <= 31:
            raise ValueError("preference({}) can not be outside of range 0 to 31".format(preference))
        self.preference = preference
        self.descriptors = []

        if descriptors is not None:
            if type(descriptors) not in (list, tuple):
                descriptors = (descriptors,)
            self.extend(descriptors)

        self._sets[index] = self

    def __iter__(self):
        return iter(self.descriptors)

    def __getitem__(self, item):
        return self.descriptors[item]

    def __setitem__(self, key, value):
        if not isinstance(value, PhysicalDescriptor):
            raise ValueError("Can not assign '{}' to descriptors".format(type(value)))
        self.descriptors[key] = value

    def append(self, item):
        self.extend((item,))

    def extend(self, items):
        if len([descriptor for descriptor in items if not isinstance(descriptor, PhysicalDescriptor)]):
            raise ValueError("Can not assign item that's not a PhysicalDescriptor")
        self.descriptors.extend(items)
