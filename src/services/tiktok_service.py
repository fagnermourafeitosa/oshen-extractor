import os
import httpx
from src.core.utils import generate_filename

class TikTokService:
    def download(self, url: str, name: str) -> str:
        """
        Downloads video from TikTok without watermark using TikWM API.
        Returns the path to the downloaded file.
        """
        filename_base = generate_filename(name, url)
        download_dir = "downloads"
        os.makedirs(download_dir, exist_ok=True)
        
        # TikWM API endpoint
        api_url = f"https://www.tikwm.com/api/?url={url}"
        
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.get(api_url)
                response.raise_for_status()
                data = response.json()
                
                if data.get("code") != 0:
                    raise Exception(f"TikWM API error: {data.get('msg', 'Unknown error')}")
                
                video_url = data["data"]["play"]
                
                # Download the actual video file
                video_response = client.get(video_url)
                video_response.raise_for_status()
                
                # Determine extension (usually mp4)
                file_path = f"{download_dir}/{filename_base}.mp4"
                
                with open(file_path, "wb") as f:
                    f.write(video_response.content)
                    
                return file_path
                
        except Exception as e:
            raise Exception(f"Failed to download from TikTok via TikWM: {str(e)}")
