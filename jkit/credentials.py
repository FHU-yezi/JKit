from __future__ import annotations

from base64 import b64decode
from datetime import datetime
from typing import Any

from jkit._base import CredentialObject
from jkit._codec import JSON_DECODER
from jkit._normalization import normalize_datetime
from jkit.constants import _JWT_TOKEN_REGEX
from jkit.exceptions import ExpiredCredentialError, InvalidCredentialError


class JianshuCredential(CredentialObject):
    def __init__(self, *, remember_user_token: str) -> None:
        self._remember_user_token = remember_user_token

    @classmethod
    def from_remember_user_token(cls, remember_user_token: str, /) -> JianshuCredential:
        return cls(remember_user_token=remember_user_token)

    @property
    def headers(self) -> dict[str, str]:
        return {"Cookie": f"remember_user_token={self._remember_user_token}"}


class BeijiaoyiCredential(CredentialObject):
    def __init__(self, *, bearer_token: str) -> None:
        if not _JWT_TOKEN_REGEX.fullmatch(bearer_token):
            raise InvalidCredentialError("凭证不是有效的 JWT Token 格式")

        try:
            jwt_body = self.__class__._get_decoded_jwt_body(bearer_token)
        except Exception:
            raise InvalidCredentialError("凭证不是有效的 JWT Token 格式") from None

        self._create_time = normalize_datetime(int(jwt_body["iat"]))
        self._expire_time = normalize_datetime(int(jwt_body["exp"]))

        if self._expire_time < datetime.now():
            raise ExpiredCredentialError(f"凭证已于 {self._expire_time} 过期")

        self._bearer_token = bearer_token

    @classmethod
    def _get_decoded_jwt_body(cls, token: str) -> dict[str, Any]:
        return JSON_DECODER.decode(b64decode(token.split(".")[1]))

    @classmethod
    def from_bearer_token(cls, bearer_token: str, /) -> BeijiaoyiCredential:
        return cls(bearer_token=bearer_token)

    @property
    def headers(self) -> dict[str, str]:
        if self._expire_time < datetime.now():
            raise ExpiredCredentialError(f"凭证已于 {self._expire_time} 过期")

        return {"Authorization": f"Bearer {self._bearer_token}"}

    @property
    def create_time(self) -> datetime:
        return self._create_time

    @property
    def expire_time(self) -> datetime:
        return self._expire_time
