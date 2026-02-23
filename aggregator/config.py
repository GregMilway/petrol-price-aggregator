from pydantic_settings import BaseSettings, SettingsConfigDict

FF_BASE_URL = "https://www.fuel-finder.service.gov.uk/api/v1"


class ClientSecrets(BaseSettings):
    CLIENT_ID: str
    CLIENT_SECRET: str

    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore",
    )


client_secrets = ClientSecrets()
