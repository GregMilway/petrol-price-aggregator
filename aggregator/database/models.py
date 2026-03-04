from datetime import datetime, time
from enum import StrEnum

from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, Time

from ..schema import FuelType


class Weekday(StrEnum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"
    BANK_HOLIDAY = "bank_holiday"


class Address(SQLModel, table=True):
    address_line_1: str
    address_line_2: str | None = Field(default=None)
    city: str
    country: str
    county: str | None = Field(default=None)
    postcode: str
    latitude: float
    longitude: float
    station_id: str = Field(foreign_key="Station.station_id")
    station: "Station" = Relationship(
        back_populates="location",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class Amenity(SQLModel, table=True):
    amenity: str
    station_id: str = Field(foreign_key="Station.station_id")
    station: "Station" = Relationship(
        back_populates="amenity",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class FuelPrices(SQLModel, table=True):
    __tablename__ = "fuel_prices"
    fuel_type: FuelType
    price: float
    price_last_updated: datetime = Field(sa_column=Column(DateTime))
    price_change_effective_timestamp: datetime = Field(sa_column=Column(DateTime))
    station_id: str = Field(foreign_key="Station.station_id")
    station: "Station" = Relationship(
        back_populates="fuel_prices",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class FuelTypes(SQLModel, table=True):
    __tablename__ = "fuel_types"
    fuel_type: FuelType
    station_id: str = Field(foreign_key="Station.station_id")
    station: "Station" = Relationship(
        back_populates="fuel_type",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class OpeningTime(SQLModel, table=True):
    __tablename__ = "opening_time"
    weekday: Weekday
    type: str | None = Field(default=None)
    open: time = Field(sa_column=Column(Time))
    close: time = Field(sa_column=Column(Time))
    is_24_hours: bool
    station_id: str = Field(foreign_key="Station.station_id")
    station: "Station" = Relationship(
        back_populates="opening_times",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class Station(SQLModel, table=True):
    station_id: str = Field(primary_key=True)
    public_phone_number: str | None = Field(default=None)
    trading_name: str
    is_same_trading_and_brand_name: bool
    brand_name: str
    temporary_closure: bool
    permanent_closure: bool | None = Field(default=None)
    permanent_closure_date: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True),
            default=None,
        )
    )
    is_motorway_service_station: bool
    is_supermarket_service_station: bool
    location: Address = Relationship(
        back_populates="station",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    amenities: list[Amenity] = Relationship(
        back_populates="station",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    fuel_prices: list[FuelPrices] = Relationship(
        back_populates="station",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    fuel_types: list[FuelTypes] = Relationship(
        back_populates="station",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    opening_times: list[OpeningTime] = Relationship(
        back_populates="station",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
