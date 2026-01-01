import os
import yt_dlp
from src.core.utils import generate_filename

class TikTokService:
    def download(self, url: str, name: str) -> str:
        """
        Downloads video from TikTok without watermark using yt-dlp.
        Returns the path to the downloaded file.
        """
        filename_base = generate_filename(name, url)
        output_tmpl = f"downloads/{filename_base}.%(ext)s"
        
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': output_tmpl,
            'quiet': True,
            'no_warnings': True,
        }

        try:
            os.makedirs("downloads", exist_ok=True)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                downloaded_file = ydl.prepare_filename(info)
                return downloaded_file
        except Exception as e:
            raise Exception(f"Failed to download from TikTok: {str(e)}")
