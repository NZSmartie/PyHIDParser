from enum import Enum


class ValueRange:
    def __init__(self, minimum=None, maximum=None):
        self.minimum = minimum if minimum is not None else ~0x7FFFFFFF
        self.maximum = maximum if maximum is not None else 0x7FFFFFFF

    def __repr__(self):
        return "<{}: minimum: {}, maximum: {}>".format(self.__class__.__name__, self.minimum, self.maximum)

    def in_range(self, value):
        return self.minimum <= value <= self.maximum

    def __cmp__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueRange("other is not of type {}".format(self.__class__.__name__))
        return self.minimum == other.minimum and self.maximum == other.maximum

    def scale_to(self, new_range, value):
        if not isinstance(new_range, ValueRange):
            raise ValueError("new_range is not ValueRange")
        if type(value) not in [int, float]:
            raise ValueError("{} is not a numeric value".format(type(value)))
        if not self.in_range(value):
            raise ArithmeticError("value is outside of accepted range")
        value = (value - self.minimum) / (self.maximum - self.minimum)
        return new_range.minimum + value * (new_range.maximum - new_range.minimum)


class EnumMask(object):
    def __init__(self, enum, value):
        self._enum=enum
        self._value=value

    def __and__(self, other):
        assert isinstance(other,self._enum)
        return self._value&other.value

    def __or__(self, other):
        assert isinstance(other,self._enum)
        return EnumMask(self._enum, self._value|other.value)

    def __repr__(self):
        return "<{} for {}: {}>".format(
            self.__class__.__name__,
            self._enum,
            self._enum.__repr_members__(self._value)
        )


class FlagEnum(Enum):
    def __or__(self, other):
        return EnumMask(self.__class__, self.value|other.value)

    def __and__(self, other):
        if isinstance(other, self.__class__):
            return self.value&other.value
        elif isinstance(other, EnumMask):
            return other&self
        else:
            raise ValueError("Not a valid {0}".format(self.__class__.__name__))

    @classmethod
    def __repr_members__(cls, value):
        return [member for member in cls.__members__ if cls.__members__[member].value & value > 0]
