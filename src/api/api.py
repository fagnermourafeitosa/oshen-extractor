from fastapi import APIRouter
from src.api.v1.endpoints import instagram, tiktok, youtube

api_router = APIRouter()

api_router.include_router(instagram.router, prefix="/instagram", tags=["instagram"])
api_router.include_router(tiktok.router, prefix="/tiktok", tags=["tiktok"])
api_router.include_router(youtube.router, prefix="/youtube", tags=["youtube"])
