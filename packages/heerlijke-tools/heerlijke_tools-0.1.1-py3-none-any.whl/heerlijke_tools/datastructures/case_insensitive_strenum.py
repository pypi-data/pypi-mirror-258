from enum import auto
from strenum import StrEnum
from strenum.mixins import Comparable


class CaseInsensitiveStrEnum(Comparable, StrEnum):
    def _cmp_values(self, other):
        return self.value, str(other).upper()

    @classmethod
    def _missing_(cls, value):
        lower_value = value.lower()
        for member in cls:
            if member.value.lower() == lower_value:
                return member

        return super()._missing_(value)
