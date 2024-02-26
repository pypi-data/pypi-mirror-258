import asyncio
import logging
from datetime import date, datetime, timedelta
from itertools import chain
from typing import Final
from zoneinfo import ZoneInfo

import aiohttp
import boto3  # type: ignore
from aiohttp.client_exceptions import ClientResponseError

from .aws_srp import AWSSRP
from .exceptions import CannotConnect, InvalidAuth
from .models import AggregateType, BillingPeriod, DailyRead, HourlyRead, MonthlyRead

logger = logging.getLogger(__name__)
DEBUG_LOG_RESPONSE = False


class HydroOttawa:
    """Class that can get historical and forecasted usage/cost from Bidgely's NA API."""

    BASE_URL: Final = "https://api-myaccount.hydroottawa.com"

    def __init__(
        self,
        session: aiohttp.ClientSession,
        username: str,
        password: str,
    ) -> None:
        self.session: aiohttp.ClientSession = session
        self.username: str = username
        self.password: str = password
        self.x_access: str | None = None
        self.x_id: str | None = None
        self.auth_token: str | None = None
        return None

    async def async_login(self) -> None:
        "Returns user-id and token for Bidgely."
        client = await self.session.loop.run_in_executor(
            None,
            boto3.client,
            "cognito-idp",
            "ca-central-1",
        )  # type: ignore
        aws = AWSSRP(
            username=self.username,
            password=self.password,
            pool_id="ca-central-1_VYnwOhMBK",
            client_id="7scfcis6ecucktmp4aqi1jk6cb",
            client=client,
            loop=self.session.loop,
        )
        try:
            tokens = await aws.authenticate_user()
            self.x_access = tokens["AuthenticationResult"]["AccessToken"]
            self.x_id = tokens["AuthenticationResult"]["IdToken"]

            headers = {"x-id": self.x_id, "x-access": self.x_access}

            async with self.session.get(
                f"{self.BASE_URL}/app-token", headers=headers
            ) as resp:
                self.auth_token = resp.headers["x-amzn-remapped-authorization"]
        except ClientResponseError as err:
            if err.status in (401, 403):
                raise InvalidAuth(err)
            else:
                raise CannotConnect(err)
        return None

    async def fetch_hourly(self, fetch_date: date | None = None) -> list[HourlyRead]:
        if fetch_date is None:
            fetch_date = datetime.now(ZoneInfo("America/Toronto")) - timedelta(days=1)
            fetch_date = fetch_date.date()
        url = f"{self.BASE_URL}/usage/hourly"
        headers = {
            "x-id": self.x_id,
            "x-access": self.x_access,
            "Authorization": self.auth_token,
        }
        async with self.session.post(
            url, headers=headers, json={"date": f"{fetch_date}"}
        ) as resp:
            processed: list[HourlyRead] = []
            reads = await resp.json()
            for read in reads["intervals"]:
                read_date = datetime.fromisoformat(read["endDateTime"]).replace(
                    tzinfo=ZoneInfo("America/Toronto")
                )
                hourly = HourlyRead(
                    read_date,
                    read["rateBand"],
                    read["hourlyUsage"],
                    read["hourlyCost"],
                )
                processed.append(hourly)
        return processed

    async def fetch_daily(
        self, start_date: date | None = None, end_date: date | None = None
    ) -> list[DailyRead]:
        if start_date is None:
            start_date = datetime.now(ZoneInfo("America/Toronto")) - timedelta(days=8)
            start_date = start_date.date()
        if end_date is None:
            end_date = datetime.now(ZoneInfo("America/Toronto")).date() - timedelta(
                days=1
            )
        url = f"{self.BASE_URL}/usage/daily"
        headers = {
            "x-id": self.x_id,
            "x-access": self.x_access,
            "Authorization": self.auth_token,
        }
        async with self.session.post(
            url,
            headers=headers,
            json={"startDate": f"{start_date}", "endDate": f"{end_date}"},
        ) as resp:
            processed: list[DailyRead] = []
            reads = await resp.json()
            for read in reads["intervals"]:
                read_date = date.fromisoformat(read["date"])
                daily = DailyRead(
                    read_date,
                    read["dailyUsage"],
                )
                processed.append(daily)
        return processed

    async def fetch_monthly(
        self, start_date: date | None = None, end_date: date | None = None
    ) -> list[MonthlyRead]:
        if start_date is None:
            start_date = datetime.now(ZoneInfo("America/Toronto")) - timedelta(days=365)
            start_date = start_date.date()
        if end_date is None:
            end_date = datetime.now(ZoneInfo("America/Toronto")).date() - timedelta(
                days=1
            )
        url = f"{self.BASE_URL}/usage/monthly"
        headers = {
            "x-id": self.x_id,
            "x-access": self.x_access,
            "Authorization": self.auth_token,
        }
        async with self.session.post(
            url,
            headers=headers,
            json={"startDate": f"{start_date}", "endDate": f"{end_date}"},
        ) as resp:
            processed: list[MonthlyRead] = []
            reads = await resp.json()
            for read in reads["intervals"]:
                read_start_date = date.fromisoformat(read["startDate"])
                read_end_date = date.fromisoformat(read["endDate"])
                monthly = MonthlyRead(
                    read_start_date,
                    read_end_date,
                    read["monthlyUsage"],
                    read["offPeakUsage"],
                    read["midPeakUsage"],
                    read["onPeakUsage"],
                    read["uloUsage"],
                    read["monthlyCost"],
                    read["offPeakCost"],
                    read["midPeakCost"],
                    read["onPeakCost"],
                    read["uloCost"],
                    read["ratePlan"],
                    read["numberOfDays"],
                )
                processed.append(monthly)
        return processed

    async def get_billing_periods(self) -> list[BillingPeriod]:
        headers = {
            "x-id": self.x_id,
            "x-access": self.x_access,
            "Authorization": self.auth_token,
        }
        billing_periods: list[BillingPeriod] = []
        async with self.session.get(
            f"{self.BASE_URL}/usage/billing-period-list", headers=headers
        ) as resp:
            reads = await resp.json()
            for period in reads:
                print(period)
                billing_periods.append(
                    BillingPeriod(
                        date.fromisoformat(period["startDate"]),
                        date.fromisoformat(period["endDate"]),
                        period["ratePlan"],
                        period["currentBillingPeriod"],
                    )
                )
        return billing_periods

    async def get_usage(
        self,
        start_date: date | None = None,
        end_date: date | None = None,
        aggregate: AggregateType = AggregateType.HOURLY,
    ) -> list[HourlyRead] | list[DailyRead] | list[MonthlyRead]:
        if start_date is None:
            start_date = datetime.now(ZoneInfo("America/Toronto")) - timedelta(days=8)
            start_date = start_date.date()
        if end_date is None:
            end_date = datetime.now(ZoneInfo("America/Toronto")).date() - timedelta(
                days=1
            )

        match aggregate:
            case AggregateType.HOURLY:
                tasks = []
                days = (
                    start_date + timedelta(days=x)
                    for x in range((end_date - start_date).days + 1)
                )
                for day in days:
                    single_day = self.fetch_hourly(day)
                    tasks.append(single_day)
                result = await asyncio.gather(*tasks)
                hourlies: list[HourlyRead] = list(chain(*result))
                return hourlies
            case AggregateType.DAILY:
                return await self.fetch_daily(start_date, end_date)
            case AggregateType.MONTHLY:
                logger.error("Monthly readings are not supported yet.")
                monthlies: list[MonthlyRead] = []
                return monthlies
