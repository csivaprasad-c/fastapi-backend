from pydantic_settings import BaseSettings, SettingsConfigDict

class DataSourceSettings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str

    model_config = SettingsConfigDict(
        env_file="./.env", 
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore"
    )

    @property
    def POSTGRES_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = DataSourceSettings()

print(settings.POSTGRES_SERVER)
print(settings.POSTGRES_PORT)
print(settings.POSTGRES_DB)
print(settings.POSTGRES_USER)
print(settings.POSTGRES_URL)