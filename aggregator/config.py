from pydantic_settings import BaseSettings, SettingsConfigDict

FF_BASE_URL = "https://www.fuel-finder.service.gov.uk/api/v1"

_base_config = SettingsConfigDict(
    env_file="./.env",
    env_ignore_empty=True,
    extra="ignore",
)


class ClientSecrets(BaseSettings):
    CLIENT_ID: str
    CLIENT_SECRET: str

    model_config = _base_config


class DatabaseSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    PROTOCOL: str

    model_config = _base_config

    @property
    def db_url(self):
        return f"{self.PROTOCOL}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


client_secrets = ClientSecrets()
db_settings = DatabaseSettings()
