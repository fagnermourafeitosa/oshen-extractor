from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from src.services.instagram_service import InstagramService
from pydantic import BaseModel

router = APIRouter()
service = InstagramService()

class DownloadRequest(BaseModel):
    url: str
    name: str

@router.post("/download")
def download_instagram(request: DownloadRequest):
    try:
        file_path = service.download(request.url, request.name)
        return FileResponse(file_path, filename=file_path.split("/")[-1], media_type='application/octet-stream')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
