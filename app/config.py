from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    APP_PORT: int = 8000

    # Accepter les variables en plus (MARIADB_...) sans planter
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",         # clé: IGNORER les variables non mappées
        case_sensitive=True
    )

settings = Settings()
