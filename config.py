from pydantic_settings import BaseSettings, SettingsConfigDict

ALGORITHM = "HS256"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str
    secret_key: str
    frontend_url: str
    debug: bool = False
    token_expire_minutes: int = 30

settings = Settings() # type: ignore