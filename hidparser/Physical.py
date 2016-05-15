from enum import Enum as _Enum
import struct as _struct


class Bias(_Enum):
    NOT_APPLICABLE = 0
    RIGHT_HAND = 1
    LEFT_HAND = 2
    BOTH_HANDS = 3
    EITHER_HAND = 4

    def __str__(self):
        return self._name_.replace("_", " ").title()


class Qualifier(_Enum):
    NOT_APPLICABLE = 0
    RIGHT = 1
    LEFT = 2
    BOTH = 3
    EITHER = 4
    CENTER = 5

    def __str__(self):
        return self._name_.replace("_", " ").title()


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

    def __str__(self):
        return self._name_.replace("_", " ").title()


class PhysicalDescriptor:
    def __init__(self, designator: Designator, qualifier: Qualifier, effort: int=0):
        self.designator = designator
        self.qualifier = qualifier
        self.effort = effort

    def __repr__(self):
        return "<{}: {}, {}, Effort {:d}>".format(
            self.__class__.__name__,
            self.designator.__str__(),
            self.qualifier.__str__(),
            self.effort
        )


class PhysicalDescriptorSubSet:
    def __init__(self, bias: Bias, preference: int=0, descriptors=None):
        self.bias = bias
        if not 0 <= preference <= 31:
            raise ValueError("preference({}) can not be outside of range 0 to 31".format(preference))
        self.preference = preference
        self.descriptors = []

        if descriptors is not None:
            if type(descriptors) not in (list, tuple):
                descriptors = (descriptors,)
            self.extend(descriptors)

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

    def __repr__(self):
        return "<{}: Bias({}), Preference({}), [{}]>".format(
            self.__class__.__name__,
            self.bias.__str__(),
            self.preference,
            ", ".join([desc.__repr__() for desc in self.descriptors])
        )


class PhysicalDescriptorSet:
    def __init__(self):
        self._total = 0
        self._length = 0
        self._sets = {}  # type: Dict[int, PhysicalDescriptorSubSet]

    def parse(self, index, data):
        data = bytes(data)
        if index is 0:
            if len(data) != 3:
                raise ValueError("Physical descriptor at index 0 is 3 bytes in size")
            self._total, self._length = _struct.unpack("<BH", data)
            return
        if self._length is 0:
            raise ValueError("Please parse the Physical Descriptor Set at index 0 first")
        if index > self._total:
            raise IndexError("index({:d}) is out of bounds".format(index))
        if index in self._sets.keys():
            del self._sets[index]
        bias = Bias((data[0] & 0xE0) >> 5)
        preference = data[0] & 0x1F

        pdset = PhysicalDescriptorSubSet(bias, preference)
        self._sets[index] = pdset

        for i in range(self._length):
            offset = (i * 2) + 1
            designator, flags = _struct.unpack("<BB",data[offset:offset+2])
            pdset.append(PhysicalDescriptor(
                Designator(designator),
                Qualifier((flags & 0xE0) >> 5),
                flags & 0x1F
            ))

    def __getitem__(self, item):
        return self._sets[item]

    def __len__(self):
        return self._total
