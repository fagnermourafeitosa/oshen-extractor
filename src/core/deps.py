from fastapi import Header, HTTPException, status
from src.core.config import settings

async def verify_token(x_token: str = Header(...)):
    if x_token != settings.OSHEN_EXTRACTOR_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
