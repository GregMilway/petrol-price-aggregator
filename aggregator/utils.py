import logging
import re
import time
from typing import Any

import requests
from config import FF_BASE_URL

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
        print(data)
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
