from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Carrega as variáveis do arquivo .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Banco de Dados
    DATABASE_URL: str = "sqlite:///./meutea.db"

    # Segurança JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()