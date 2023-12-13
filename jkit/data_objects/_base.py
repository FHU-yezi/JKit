from typing import Self

from msgspec import Struct, convert, to_builtins


class DataObject(Struct):
    def validate(self) -> Self:
        return convert(to_builtins(self), type=self.__class__)


DATA_OBJECT_CONFIG = {
    "frozen": True,
    "eq": False,
    "kw_only": True,
}
