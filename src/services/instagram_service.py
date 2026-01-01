import os
import yt_dlp
from src.core.utils import generate_filename

class InstagramService:
    def download(self, url: str, name: str) -> str:
        """
        Downloads media from Instagram using yt-dlp.
        Returns the path to the downloaded file.
        """
        filename_base = generate_filename(name, url)
        # We don't include extension in outtmpl as yt-dlp adds it
        output_tmpl = f"downloads/{filename_base}.%(ext)s"
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_tmpl,
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }

        try:
            os.makedirs("downloads", exist_ok=True)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                downloaded_file = ydl.prepare_filename(info)
                return downloaded_file
        except Exception as e:
            raise Exception(f"Failed to download from Instagram: {str(e)}")
