from jkit.data_objects._base import DATA_OBJECT_CONFIG, DataObject


class UserInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: int  # noqa: A003
    url: str
    slug: str
    name: str
    introduction: str
