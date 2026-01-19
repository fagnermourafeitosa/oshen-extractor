import os
import yt_dlp
import logging
from typing import Dict, Any, Optional
from src.core.utils import generate_filename

logger = logging.getLogger(__name__)

class YtDlpProvider:
    """
    Infrastructure provider using yt-dlp to download media from various platforms (Instagram, YouTube, etc.).
    """
    def __init__(self, download_dir: str = "downloads"):
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)

    def download(self, url: str, name: str, format_type: str = "video") -> str:
        filename_base = generate_filename(name, url)
        output_tmpl = f"{self.download_dir}/{filename_base}.%(ext)s"
        
        ydl_opts = {
            'outtmpl': output_tmpl,
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }

        if format_type == 'audio':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            # Flexible format for both Instagram and YouTube
            ydl_opts.update({
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            })

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                downloaded_file = ydl.prepare_filename(info)
                
                if format_type == 'audio':
                    # Postprocessor might change extension to mp3
                    pre_extension_file = os.path.splitext(downloaded_file)[0]
                    downloaded_file = f"{pre_extension_file}.mp3"
                
                logger.info(f"YtDlpProvider: Downloaded {url} to {downloaded_file}")
                return downloaded_file
        except Exception as e:
            logger.error(f"YtDlpProvider: Failed to download from {url}: {e}")
            raise Exception(f"Provider error: {str(e)}")
