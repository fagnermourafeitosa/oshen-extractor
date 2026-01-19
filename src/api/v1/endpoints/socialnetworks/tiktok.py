from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from src.services.social_networks.use_cases.download_media import DownloadMediaUseCase
from pydantic import BaseModel

router = APIRouter()

class DownloadRequest(BaseModel):
    url: str
    name: str

class TikTokHandler:
    def __init__(self, use_case: DownloadMediaUseCase = Depends()):
        self.use_case = use_case

    def download(self, request: DownloadRequest):
        file_path = self.use_case.execute(request.url, request.name)
        return FileResponse(file_path, filename=file_path.split("/")[-1], media_type='video/mp4')

@router.post("/download")
def download_tiktok(
    request: DownloadRequest, 
    handler: TikTokHandler = Depends()
):
    try:
        return handler.download(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
