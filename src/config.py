from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    API_VERSION: str = "1.0.0"
    ENV: str = "dev"  # dev | test | prod
    
    DATABASE_URL: str = "sqlite:///./app.db"
    DB_ECHO: bool = False           
    DB_POOL_SIZE: int = 5           
    DB_MAX_OVERFLOW: int = 10       

settings = Settings()