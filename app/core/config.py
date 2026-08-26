# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

# CONSTS BEGIN
FETCH_IN_MINUTES = 5
NIGHTSCOUT_DOCKER_URL = "http://localhost:1337/api/v1/entries.json?count=1"
IS_DEVELOPMENT = True
# CONSTS END

class Settings(BaseSettings):
    dexcom_email: str
    dexcom_password: str

    nightscout_docker_api_secret: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")



settings = Settings()


