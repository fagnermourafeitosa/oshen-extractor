from fastapi import FastAPI, Depends
from src.core.config import settings
from src.core.deps import verify_token
from src.api.api import api_router
from src.api.v1.endpoints import webhook

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/")
def read_root():
    return {"message": "Welcome to Oshen Extractor API"}



app.include_router(api_router, prefix=settings.API_V1, dependencies=[Depends(verify_token)])

app.include_router(webhook.router, prefix="/evolution", tags=["evolution"], dependencies=[Depends(verify_token)])