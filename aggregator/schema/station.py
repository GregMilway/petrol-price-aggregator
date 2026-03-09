"""API schema for deserializing data from /api/v1/pfs?batch-number=1"""

from datetime import datetime, time

from pydantic import BaseModel

from .fuel import FuelType


class Address(BaseModel):
    address_line_1: str
    address_line_2: str | None
    city: str
    country: str | None
    county: str | None
    postcode: str
    latitude: float
    longitude: float


class DayOpening(BaseModel):
    open: time
    close: time
    is_24_hours: bool


class BankHolidayOpening(BaseModel):
    type: str
    open_time: time
    close_time: time
    is_24_hours: bool


class UsualDays(BaseModel):
    monday: DayOpening
    tuesday: DayOpening
    wednesday: DayOpening
    thursday: DayOpening
    friday: DayOpening
    saturday: DayOpening
    sunday: DayOpening


class OpeningTimes(BaseModel):
    usual_days: UsualDays
    bank_holiday: BankHolidayOpening


class Station(BaseModel):
    node_id: str
    public_phone_number: str | None
    trading_name: str
    is_same_trading_and_brand_name: bool
    brand_name: str
    temporary_closure: bool
    permanent_closure: bool | None
    permanent_closure_date: datetime | None
    is_motorway_service_station: bool
    is_supermarket_service_station: bool
    location: Address
    amenities: list[str]
    opening_times: OpeningTimes
    fuel_types: list[FuelType]
