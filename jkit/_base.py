from abc import ABCMeta, abstractmethod
from typing import List

from msgspec import Struct, convert, to_builtins
from msgspec import ValidationError as MsgspecValidationError
from typing_extensions import Self

from jkit.exceptions import ValidationError


class DataObject(Struct):
    def _validate(self) -> Self:
        from jkit.config import DATA_OBJECT_CONFIG

        if not DATA_OBJECT_CONFIG.enable_validation:
            return self

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


class CheckableObject(metaclass=ABCMeta):
    def __init__(self) -> None:
        self._checked = False

    @abstractmethod
    async def check(self) -> None:
        raise NotImplementedError

    async def _auto_check(self) -> None:
        from jkit.config import RESOURCE_OBJECT_CONFIG

        if not RESOURCE_OBJECT_CONFIG.auto_checking:
            return

        if not self._checked:
            await self.check()

    def _as_checked(self) -> Self:
        """将资源对象设置为已检查状态

        默认情况下，从 DataObject 获取的资源标识符创建的资源对象不进行检查。
        此操作有利于提升性能。
        可通过修改 `RESOURCE_OBJECT_CONFIG.force_check_object_from_data_object` 的值
        改变此行为。
        """

        from jkit.config import RESOURCE_OBJECT_CONFIG

        if RESOURCE_OBJECT_CONFIG.force_check_object_from_data_object:
            self._checked = True

        return self


class SlugAndUrlObject(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def from_slug(cls, slug: str, /) -> Self:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_url(cls, url: str, /) -> Self:
        raise NotImplementedError

    @property
    @abstractmethod
    def slug(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def url(self) -> str:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.slug == other.slug

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(slug="{self.slug}")'


class IdAndUrlObject(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def from_id(cls, id: int, /) -> Self:  # noqa: A002
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_url(cls, url: str, /) -> Self:
        raise NotImplementedError

    @property
    @abstractmethod
    def id(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def url(self) -> str:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(id="{self.id}")'


class ConfigObject(Struct):
    def _validate(self) -> Self:
        return convert(to_builtins(self), type=self.__class__)


CONFIG_CONFIG = {
    "eq": False,
    "kw_only": True,
    "gc": False,
}
