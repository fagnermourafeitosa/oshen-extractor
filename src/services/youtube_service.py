import os
import yt_dlp
from src.core.utils import generate_filename

class YouTubeService:
    def download(self, url: str, name: str, format_type: str = "video") -> str:
        """
        Downloads video or audio from YouTube.
        format_type: 'video' or 'audio'
        Returns the path to the downloaded file.
        """
        filename_base = generate_filename(name, url)
        # yt-dlp handles extension automatically based on format
        output_tmpl = f"downloads/{filename_base}.%(ext)s"
        
        ydl_opts = {
            'outtmpl': output_tmpl,
            'quiet': True,
            'no_warnings': True,
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
            ydl_opts.update({
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            })

        try:
            os.makedirs("downloads", exist_ok=True)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                downloaded_file = ydl.prepare_filename(info)
                
                if format_type == 'audio':
                     # The postprocessor might change the extension to mp3
                     pre_extension_file = os.path.splitext(downloaded_file)[0]
                     downloaded_file = f"{pre_extension_file}.mp3"
                     
                return downloaded_file
        except Exception as e:
            raise Exception(f"Failed to download from YouTube: {str(e)}")
