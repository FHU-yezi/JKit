from datetime import datetime
from decimal import Context, Decimal
from typing import Union


def normalize_datetime(input_data: Union[int, float, str], /) -> datetime:
    if isinstance(input_data, (int, float)):
        result = datetime.fromtimestamp(input_data)
    else:
        result = datetime.fromisoformat(input_data)

    return result.replace(microsecond=0, tzinfo=None)


def normalize_assets_amount(input_data: int, /) -> float:
    return input_data / 1000


def normalize_assets_amount_precise(input_data: int, /) -> Decimal:
    return Context(prec=18).create_decimal_from_float(input_data / 10**18)


def normalize_percentage(input_data: Union[int, float], /) -> float:
    return input_data / 100
