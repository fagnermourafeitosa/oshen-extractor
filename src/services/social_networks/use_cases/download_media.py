import logging
from typing import Dict, Any
from src.services.social_networks.providers.ytdlp_provider import YtDlpProvider
from src.services.social_networks.providers.tikwm_provider import TikWmProvider

logger = logging.getLogger(__name__)

class DownloadMediaUseCase:
    """
    Application use case to orchestrate media downloads from various social networks.
    Decides which provider to use based on the URL or request parameters.
    """
    def __init__(self):
        self.ytdlp = YtDlpProvider()
        self.tikwm = TikWmProvider()

    def execute(self, url: str, name: str, format_type: str = "video") -> str:
        """
        Executes the download process.
        Returns the local path to the downloaded file.
        """
        url_lower = url.lower()
        
        try:
            if "tiktok.com" in url_lower:
                logger.info(f"DownloadMediaUseCase: Routing to TikWmProvider for {url}")
                return self.tikwm.download_no_watermark(url, name)
            
            elif "instagram.com" in url_lower or "youtube.com" in url_lower or "youtu.be" in url_lower:
                logger.info(f"DownloadMediaUseCase: Routing to YtDlpProvider for {url}")
                return self.ytdlp.download(url, name, format_type)
            
            else:
                # Fallback to yt-dlp for other generic supported sites
                logger.info(f"DownloadMediaUseCase: Fallback routing to YtDlpProvider for {url}")
                return self.ytdlp.download(url, name, format_type)
                
        except Exception as e:
            logger.error(f"DownloadMediaUseCase: Failed to execute download for {url}: {e}")
            raise e
