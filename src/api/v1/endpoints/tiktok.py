from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from src.services.tiktok_service import TikTokService
from pydantic import BaseModel

router = APIRouter()
service = TikTokService()

class DownloadRequest(BaseModel):
    url: str
    name: str

@router.post("/download")
def download_tiktok(request: DownloadRequest):
    try:
        file_path = service.download(request.url, request.name)
        return FileResponse(file_path, filename=file_path.split("/")[-1], media_type='video/mp4')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
