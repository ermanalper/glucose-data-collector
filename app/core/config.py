# app/core/config.py
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(__file__).resolve().parent.parent.parent / ".env"

# CONSTS BEGIN
FETCH_IN_MINUTES = 5
NIGHTSCOUT_DOCKER_URL = "http://localhost:1337/api/v1/entries.json?count=1"
IS_DEVELOPMENT = True
INTERPOLATION_STORAGE_PATH= Path(__file__).resolve().parent.parent.parent / "storage/interpolations.jsonl"
# CONSTS END


class Settings(BaseSettings):
    dexcom_email: str
    dexcom_password: str
    nightscout_docker_api_secret: str

    postgres_user: str
    postgres_password: str
    postgres_db: str
    database_url: str

    api_key: str

    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding='utf-8', extra='ignore')



settings = Settings()


