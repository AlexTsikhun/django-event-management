from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DJANGO_SECRET_KEY: str
    EMAIL_HOST_USER: str
    EMAIL_HOST_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
