from abc import ABCMeta, abstractmethod
from typing import Callable, List, Optional

from msgspec import Struct, convert, to_builtins
from msgspec import ValidationError as MsgspecValidationError
from typing_extensions import Self

from jkit.config import CONFIG
from jkit.exceptions import ValidationError


class DataObject(Struct):
    def _validate(self) -> Self:
        if not CONFIG.data_validation.enabled:
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
        if not CONFIG.resource_check.auto_check:
            return

        if not self._checked:
            await self.check()

    def _as_checked(self) -> Self:
        if CONFIG.resource_check.force_check_safe_data:
            self._checked = True

        return self


class SlugAndUrlObject(metaclass=ABCMeta):
    @classmethod
    def _check_params(
        cls,
        *,
        object_readable_name: str,
        slug: Optional[str],
        url: Optional[str],
        slug_check_func: Callable[[str], bool],
        url_convert_func: Callable[[str], str],
    ) -> str:
        # 如果同时提供了 Slug 和 Url
        if slug is not None and url is not None:
            raise ValueError(
                f"{object_readable_name} Slug 与{object_readable_name}链接不可同时提供"
            )

        # 如果提供了 Slug
        if slug is not None:
            if not slug_check_func(slug):
                raise ValueError(f"{slug} 不是有效的{object_readable_name} Slug")

            return slug
        # 如果提供了 Url
        elif url is not None:  # noqa: RET505
            # 转换函数中会对 Url 进行检查，并在 Url 无效时抛出异常
            return url_convert_func(url)

        # 如果 Slug 与 Url 均未提供
        raise ValueError(
            f"必须提供{object_readable_name} Slug 或{object_readable_name}链接"
        )

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
