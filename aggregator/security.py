import logging
from datetime import datetime, timedelta

import requests
from config import FF_BASE_URL, client_secrets


class ClientToken:
    def __init__(self):
        self._token: str = ""
        self.expiry: datetime = datetime.now()
        self.logger: logging.Logger = logging.getLogger("security")

    def _fetch_token(self):
        url = FF_BASE_URL + "/oauth/generate_access_token"
        resp = requests.post(
            url,
            data={
                "client_id": client_secrets.CLIENT_ID,
                "client_secret": client_secrets.CLIENT_SECRET,
            },
        )
        resp.raise_for_status()
        data = resp.json()["data"]
        self._token = data["access_token"]
        self.expiry = datetime.now() + timedelta(seconds=data["expires_in"])

    def token(self) -> str:
        if not self._token or self.expiry <= datetime.now():
            self.logger.info("Fetching new token")
            self._fetch_token()
            self.logger.info("New token expiry: %s", self.expiry)
        return self._token
