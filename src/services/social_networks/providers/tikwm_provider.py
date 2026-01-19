import os
import httpx
import logging
from src.core.utils import generate_filename

logger = logging.getLogger(__name__)

class TikWmProvider:
    """
    Infrastructure provider for TikTok downloads using the TikWM API.
    """
    def __init__(self, download_dir: str = "downloads"):
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)
        self.api_url = "https://www.tikwm.com/api/"

    def download_no_watermark(self, url: str, name: str) -> str:
        filename_base = generate_filename(name, url)
        
        try:
            with httpx.Client(timeout=30.0) as client:
                # 1. Get download URL from TikWM
                response = client.get(f"{self.api_url}?url={url}")
                response.raise_for_status()
                data = response.json()
                
                if data.get("code") != 0:
                    raise Exception(f"TikWM API error: {data.get('msg', 'Unknown error')}")
                
                video_url = data["data"]["play"]
                
                # 2. Download the actual video file
                video_response = client.get(video_url)
                video_response.raise_for_status()
                
                file_path = f"{self.download_dir}/{filename_base}.mp4"
                with open(file_path, "wb") as f:
                    f.write(video_response.content)
                
                logger.info(f"TikWmProvider: Downloaded {url} to {file_path}")
                return file_path
                
        except Exception as e:
            logger.error(f"TikWmProvider: Failed to download from TikTok via TikWM: {e}")
            raise Exception(f"Provider error: {str(e)}")
