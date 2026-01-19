from fastapi import APIRouter
from src.api.v1.endpoints.socialnetworks import instagram, tiktok, youtube
from src.api.v1.endpoints.whatsapp import register_connection, webhook

api_router = APIRouter()

# Register standard routers
api_router.include_router(instagram.router, prefix="/instagram", tags=["instagram"])
api_router.include_router(tiktok.router, prefix="/tiktok", tags=["tiktok"])
api_router.include_router(youtube.router, prefix="/youtube", tags=["youtube"])

# WhatsApp Routes - Centralized registration of sub-routers
api_router.include_router(register_connection.router, prefix="/whatsapp", tags=["whatsapp"])
api_router.include_router(webhook.router, prefix="/whatsapp", tags=["whatsapp"])