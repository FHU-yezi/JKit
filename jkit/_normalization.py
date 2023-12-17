from datetime import datetime
from typing import Union


def normalize_datetime(input_data: Union[int, float], /) -> datetime:
    if isinstance(input_data, (int, float)):
        return datetime.fromtimestamp(input_data).replace(microsecond=0, tzinfo=None)

    return datetime.now()


def normalize_assets_amount(input_data: int, /) -> float:
    return input_data / 1000
