"""API schema for deserializing data from /api/v1/pfs/fuel-prices"""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class FuelType(StrEnum):
    B7_PREMIUM = "B7_PREMIUM"
    B7_STANDARD = "B7_STANDARD"
    B10 = "B10"
    E5 = "E5"
    E10 = "E10"
    HVO = "HVO"


class FuelPrice(BaseModel):
    fuel_type: FuelType
    price: float
    price_last_updated: datetime
    price_change_effective_timestamp: datetime


class Fuel(BaseModel):
    node_id: str
    mft_organisation_name: str
    public_phone_number: str | None
    trading_name: str
    fuel_prices: list[FuelPrice]
