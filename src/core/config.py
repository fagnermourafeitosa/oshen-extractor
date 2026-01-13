from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Oshen Extractor API"
    API_V1: str = "/api/v1"
    OSHEN_EXTRACTOR_TOKEN: str
    OSHEN_EXTRACTOR_BASE_URL: str
    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None

    WHATSAPP_REDIS_QUEUENAME: str = "oshen-whatsapp-messages"

    class Config:
        env_file = ".env"

settings = Settings()
