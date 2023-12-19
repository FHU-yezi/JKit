from abc import ABCMeta, abstractmethod
from typing import Any, List

from msgspec import Struct, convert, to_builtins
from msgspec import ValidationError as MsgspecValidationError
from typing_extensions import Self

from jkit.exceptions import ValidationError


class DataObject(Struct):
    def _validate(self) -> Self:
        try:
            return convert(to_builtins(self), type=self.__class__)
        except MsgspecValidationError as e:
            raise ValidationError(e.args[0]) from None

    def __repr__(self) -> str:
        field_strings: List[str] = []
        for field in self.__struct_fields__:
            value = self.__getattribute__(field)

            if isinstance(value, str) and len(value) >= 100:
                formatted_value = value[:100] + "[truncated...]"
            else:
                formatted_value = value.__repr__()

            field_strings.append(f"{field}={formatted_value}")

        return (
            self.__class__.__name__ + "(\n    " + ",\n    ".join(field_strings) + "\n)"
        )


DATA_OBJECT_CONFIG = {
    "frozen": True,
    "eq": False,
    "kw_only": True,
}


class ResourceObject:
    pass


class StandardResourceObject(ResourceObject, metaclass=ABCMeta):
    def __init__(self) -> None:
        self._validated = False

    @classmethod
    @abstractmethod
    def from_url(cls, url: str, /) -> Self:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_slug(cls, slug: str, /) -> Self:
        raise NotImplementedError

    @property
    @abstractmethod
    def url(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def slug(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def validate(self) -> None:
        raise NotImplementedError

    def _from_trusted_source(self) -> Self:
        """将资源对象设置为已校验状态

        从 DataObject 获取的资源标识符视为可信来源，对从其创建的资源对象跳过校验流程。
        此操作有利于提升性能。
        可通过修改 `BEHAVIOR_CONFIG.skip_validation_for_trusted_source` 的值改变此行为。
        """

        from jkit.config import BEHAVIOR_CONFIG

        if BEHAVIOR_CONFIG.skip_validation_for_trusted_source:
            self._validated = True
        return self

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__) and self.url == other.url:
            return True

        return False


class RankingResourceObject(ResourceObject):
    pass


class ConfigObject(Struct):
    def _validate(self) -> Self:
        return convert(to_builtins(self), type=self.__class__)


CONFIG_CONFIG = {
    "eq": False,
    "kw_only": True,
    "gc": False,
}
