from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Database
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "jsonplaceholder_etl"
    db_user: str = "etl_app"
    db_password: str

    jsonplaceholder_base_url: str = "https://jsonplaceholder.typicode.com"

    log_level: str = "INFO"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()