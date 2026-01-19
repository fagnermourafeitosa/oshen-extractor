from fastapi import FastAPI, Depends
from src.core.config import settings
from src.core.deps import verify_token
from src.api.api import api_router
import logging

# Configure logging to see messages in Docker console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/")
def read_root():
    return {"message": "Welcome to Oshen Extractor API"}

app.include_router(api_router, prefix=settings.API_V1, dependencies=[Depends(verify_token)])