from msgspec import Struct, convert, to_builtins
from typing_extensions import Self


class DataObject(Struct):
    def validate(self) -> Self:
        return convert(to_builtins(self), type=self.__class__)


DATA_OBJECT_CONFIG = {
    "frozen": True,
    "eq": False,
    "kw_only": True,
}
