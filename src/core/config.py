from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Oshen Extractor API"
    API_V1: str = "/api/v1"
    OSHEN_EXTRACTOR_TOKEN: str
    OSHEN_EXTRACTOR_BASE_URL: str
    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None

    # Evolution API Configuration
    DEFAULT_EVOLUTION_INSTANCE_NAME: str = "oshen"
    EVOLUTION_API_URL: str
    EVOLUTION_API_KEY: str
    # The external URL of THIS application (Oshen Extractor) reachable by Evolution
    WEBHOOK_PUBLIC_URL: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
