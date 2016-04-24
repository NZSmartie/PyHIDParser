from enum import Enum


class EnumMask(object):

    def __init__(self, enum, value):
        self._enum=enum
        self._value=value

    def __and__(self, other):
        assert isinstance(other,self._enum)
        return self._value&other.bwv

    def __or__(self, other):
        assert isinstance(other,self._enum)
        return EnumMask(self._enum, self._value|other.bwv)

    def __repr__(self):
        return "<{} for {}: {}>".format(
            self.__class__.__name__,
            self._enum,
            self._enum.__repr_members__(self._value)
        )


class FlagEnum(Enum):
    @property
    def bwv(self):
        cls=self.__class__
        idx=list(cls.__members__.values()).index(self)
        return self.value # 2**idx

    def __or__(self, other):
        return EnumMask(self.__class__, self.bwv|other.bwv)

    def __and__(self, other):
        if isinstance(other, self.__class__):
            return self.bwv&other.bwv
        elif isinstance(other, EnumMask):
            return other&self
        else:
            raise ValueError("Not a valid {0}".format(self.__class__.__name__))

    @classmethod
    def __repr_members__(cls, value):
        return [member for member in cls.__members__ if cls.__members__[member].value & value > 0]
