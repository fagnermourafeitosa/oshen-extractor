from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Oshen Extractor API"
    API_V1_STR: str = "/api/v1"
    OSHEN_EXTRACTOR_TOKEN: str
    OSHEN_EXTRACTOR_BASE_URL: str
    
    class Config:
        env_file = ".env"

settings = Settings()
