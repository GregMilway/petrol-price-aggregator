import logging
import re
import time
from typing import Any

import requests
from config import FF_BASE_URL
from schema.station import OpeningTimes

END_OF_BATCH_MESSAGE = re.compile(r"Requested batch \d+ is not available")
utils_logger = logging.getLogger("utils")


def fetch_batched(
    endpoint: str,
    token: str,
    batch_size=500,
    dwell_time=1,
    **params,
) -> list[dict[str, Any]]:
    batched = []

    i = 0
    # Convert any kwargs to kebab-case
    params = {k.replace("_", "-"): v for k, v in params.items()}
    headers = {"Authorization": f"Bearer {token}"}
    while True:
        i += 1
        utils_logger.info("Fetching batch: %s", i)
        params["batch-number"] = i
        resp = requests.get(
            endpoint,
            params=params,
            headers=headers,
        )
        data = resp.json()
        if not resp.ok:
            msg = data["data"]["data"]["message"]
            if END_OF_BATCH_MESSAGE.match(msg):
                break
            else:
                resp.raise_for_status()
        batched.extend(data)
        if len(data) < batch_size:
            # We've reached the end of the batched data
            break
        else:
            # Otherwise, be kind and wait before fetching the next batch
            time.sleep(dwell_time)

    return batched


def get_fuel_prices(
    token: str,
    **params,
) -> list[dict[str, Any]]:
    log_message = (
        f"Fetching fuel prices from {params['effective_start_date']}"
        if "effective_start_date" in params
        else "Fetching all fuel prices"
    )
    utils_logger.info(log_message)
    return fetch_batched(
        FF_BASE_URL + "/pfs/fuel-prices",
        token,
        **params,
    )


def get_stations(
    token: str,
    **params,
) -> list[dict[str, Any]]:
    log_message = (
        f"Fetching station info from {params['effective_start_date']}"
        if "effective_start_date" in params
        else "Fetching all station info"
    )
    utils_logger.info(log_message)
    return fetch_batched(
        FF_BASE_URL + "/pfs",
        token,
        **params,
    )


def opening_times_to_rows(opening_times: OpeningTimes, node_id: str) -> list[dict[str, Any]]:
    rows = []
    for day, info in opening_times.usual_days:
        row = {
            "weekday": day,
            "type": None,
            "open": info.open,
            "close": info.close,
            "is_24_hours": info.is_24_hours,
            "station_id": node_id,
        }
        rows.append(row)
    bh = opening_times.bank_holiday
    rows.append(
        {
            "weekday": "bank_holiday",
            "type": bh.type,
            "open": bh.open_time,
            "close": bh.close_time,
            "is_24_hours": bh.is_24_hours,
            "station_id": node_id,
        }
    )
    return rows


def rows_to_opening_times(rows: list[dict[str, Any]]) -> OpeningTimes:
    assert len(rows) == 8
    usual_days = {}
    bank_holiday = {}
    for row in rows:
        weekday = row["weekday"]
        if weekday == "bank_holiday":
            bank_holiday["type"] = row["type"]
            bank_holiday["open_time"] = row["open"]
            bank_holiday["close_time"] = row["close"]
            bank_holiday["is_24_hours"] = row["is_24_hours"]
        else:
            usual_days[weekday] = {
                "open": row["open"],
                "close": row["close"],
                "is_24_hours": row["is_24_hours"],
            }
    data = {"usual_days": usual_days, "bank_holiday": bank_holiday}
    return OpeningTimes(**data)
