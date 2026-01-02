from fastapi import FastAPI
from src.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/")
def read_root():
    return {"message": "Welcome to Oshen Extractor API"}

from src.api.api import api_router

from fastapi import Depends
from src.core.deps import verify_token

app.include_router(api_router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_token)])
