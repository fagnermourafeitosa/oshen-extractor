from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from src.services.youtube_service import YouTubeService
from pydantic import BaseModel

router = APIRouter()
service = YouTubeService()

class DownloadRequest(BaseModel):
    url: str
    name: str
    format_type: str = "video"

@router.post("/download")
def download_youtube(request: DownloadRequest):
    try:
        file_path = service.download(request.url, request.name, request.format_type)
        media_type = 'audio/mpeg' if request.format_type == 'audio' else 'video/mp4'
        return FileResponse(file_path, filename=file_path.split("/")[-1], media_type=media_type)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
