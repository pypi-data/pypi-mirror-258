from dataclasses import dataclass
from datetime import date, datetime
from enum import StrEnum, auto


class RateBands(StrEnum):
    TIER_1 = auto()
    TIER_2 = auto()


class AggregateType(StrEnum):
    HOURLY = auto()
    DAILY = auto()
    MONTHLY = auto()


@dataclass(slots=True)
class HourlyRead:
    measurement_time: datetime
    rate_band: str
    usage: float
    cost: float


@dataclass(slots=True)
class DailyRead:
    measurement_time: date
    usage: float


@dataclass(slots=True)
class MonthlyRead:
    start_date: date
    end_date: date
    monthly_usage: int
    off_peak_usage: int
    mid_peak_usage: int
    on_peak_usage: int
    ulo_usage: int
    monthly_cost: float
    off_peak_cost: float
    mid_peak_cost: float
    on_peak_cost: float
    ulo_cost: float
    rate_plan: str
    number_of_days: int


@dataclass(slots=True)
class BillingPeriod:
    start_date: date
    end_date: date
    rate_plan: RateBands
    current_billing_period: bool


@dataclass(slots=True)
class BillRead:
    start_date: date
