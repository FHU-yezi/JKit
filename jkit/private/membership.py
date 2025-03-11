from __future__ import annotations

from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Literal

from jkit._base import DataObject, ResourceObject
from jkit._network import send_request
from jkit._normalization import normalize_datetime
from jkit.constraints import NonNegativeInt, PositiveInt, UserName, UserSlug
from jkit.credentials import JianshuCredential
from jkit.user import User

MembershipType = Literal["BRONZE", "SILVER", "GOLD", "PLATINA"]


class ReferralInfoData(DataObject, frozen=True):
    total_referral_memberships: NonNegativeInt
    active_referral_memberships: NonNegativeInt


class _ReferralMembershipUserInfoData(DataObject, frozen=True):
    id: PositiveInt
    slug: UserSlug
    name: UserName

    def to_user_obj(self) -> User:
        return User.from_slug(self.slug)


class ReferralMembershipData(DataObject, frozen=True):
    time: datetime
    membership_type: MembershipType
    membership_duration_days: PositiveInt

    user_info: _ReferralMembershipUserInfoData | None


class Membership(ResourceObject):
    def __init__(self, *, credential: JianshuCredential) -> None:
        self._credential = credential

    @property
    async def referral_url(self) -> str:
        data = await send_request(
            datasource="JIANSHU",
            method="GET",
            path="/asimov/member_distributions",
            credential=self._credential,
            response_type="JSON",
        )

        referral_slug = data["agent_ref"]

        return f"https://www.jianshu.com/mobile/club?ref={referral_slug}"

    @property
    async def referral_info(self) -> ReferralInfoData:
        data = await send_request(
            datasource="JIANSHU",
            method="GET",
            path="/asimov/member_distributions/referrals/user",
            credential=self._credential,
            response_type="JSON",
        )

        return ReferralInfoData(
            total_referral_memberships=data["referrals"]["total_count"],
            active_referral_memberships=data["referrals"]["active_count"],
        )._validate()

    async def iter_referral_memberships(
        self, *, start_page: int = 1
    ) -> AsyncGenerator[ReferralMembershipData, None]:
        current_page = start_page
        while True:
            data = await send_request(
                datasource="JIANSHU",
                method="GET",
                path="/asimov/member_distributions/transactions",
                params={"page": current_page},
                credential=self._credential,
                response_type="JSON",
            )

            if not data["transactions"]:
                return

            for item in data["transactions"]:
                yield ReferralMembershipData(
                    time=normalize_datetime(item["created_at"]),
                    membership_type={
                        "bronze": "BRONZE",
                        "silver": "SILVER",
                        "gold": "GOLD",
                        "platina": "PLATINA",
                    }[item["type"]],  # type: ignore
                    membership_duration_days=item["days"],
                    user_info=_ReferralMembershipUserInfoData(
                        id=item["user"]["id"],
                        slug=item["user"]["slug"],
                        name=item["user"]["nickname"],
                    )
                    if "user" in item
                    else None,
                )._validate()

            current_page += 1
