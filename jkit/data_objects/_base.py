from msgspec import Struct


class DataObject(Struct):
    pass


DATA_OBJECT_CONFIG = {
    "frozen": True,
    "eq": False,
    "kw_only": True,
}
