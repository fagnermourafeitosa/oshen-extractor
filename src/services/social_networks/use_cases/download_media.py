import logging
from typing import Dict, Any
from src.services.social_networks.providers.ytdlp_provider import YtDlpProvider
from src.services.social_networks.providers.tikwm_provider import TikWmProvider
from src.core.url_utils import sanitize_url

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
        # Sanitize URL to remove tracking parameters
        cleaned_url = sanitize_url(url)
        if cleaned_url != url:
            logger.info(f"DownloadMediaUseCase: Sanitized URL from {url} to {cleaned_url}")
        
        url_lower = cleaned_url.lower()
        
        try:
            if "tiktok.com" in url_lower:
                logger.info(f"DownloadMediaUseCase: Routing to TikWmProvider for {cleaned_url}")
                return self.tikwm.download_no_watermark(cleaned_url, name)
            
            elif "instagram.com" in url_lower or "youtube.com" in url_lower or "youtu.be" in url_lower:
                logger.info(f"DownloadMediaUseCase: Routing to YtDlpProvider for {cleaned_url}")
                return self.ytdlp.download(cleaned_url, name, format_type)
            
            else:
                # Fallback to yt-dlp for other generic supported sites
                logger.info(f"DownloadMediaUseCase: Fallback routing to YtDlpProvider for {cleaned_url}")
                return self.ytdlp.download(cleaned_url, name, format_type)
                
        except Exception as e:
            logger.error(f"DownloadMediaUseCase: Failed to execute download for {url}: {e}")
            raise e
