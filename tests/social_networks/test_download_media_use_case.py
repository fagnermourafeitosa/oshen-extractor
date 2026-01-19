import pytest
from unittest.mock import MagicMock
from src.services.social_networks.use_cases.download_media import DownloadMediaUseCase

@pytest.fixture
def use_case():
    return DownloadMediaUseCase()

def test_should_route_tiktok_url_to_tikwm_provider(use_case, mocker):
    spy_tikwm = mocker.patch.object(use_case.tikwm, "download_no_watermark", return_value="downloads/tiktok.mp4")
    spy_ytdlp = mocker.patch.object(use_case.ytdlp, "download")
    
    url = "https://www.tiktok.com/@user/video/123"
    result = use_case.execute(url, "my-video")
    
    assert result == "downloads/tiktok.mp4"
    spy_tikwm.assert_called_once_with(url, "my-video")
    spy_ytdlp.assert_not_called()

def test_should_route_instagram_url_to_ytdlp_provider(use_case, mocker):
    spy_ytdlp = mocker.patch.object(use_case.ytdlp, "download", return_value="downloads/insta.mp4")
    spy_tikwm = mocker.patch.object(use_case.tikwm, "download_no_watermark")
    
    url = "https://www.instagram.com/reels/123/"
    result = use_case.execute(url, "reel")
    
    assert result == "downloads/insta.mp4"
    spy_ytdlp.assert_called_once_with(url, "reel", "video")
    spy_tikwm.assert_not_called()

def test_should_route_youtube_url_to_ytdlp_provider_with_audio_format(use_case, mocker):
    spy_ytdlp = mocker.patch.object(use_case.ytdlp, "download", return_value="downloads/audio.mp3")
    
    url = "https://youtube.com/watch?v=123"
    result = use_case.execute(url, "song", format_type="audio")
    
    assert result == "downloads/audio.mp3"
    spy_ytdlp.assert_called_once_with(url, "song", "audio")

def test_should_fallback_to_ytdlp_for_unknown_but_potentially_supported_urls(use_case, mocker):
    spy_ytdlp = mocker.patch.object(use_case.ytdlp, "download", return_value="downloads/generic.mp4")
    
    url = "https://some-other-site.com/video"
    result = use_case.execute(url, "video")
    
    assert result == "downloads/generic.mp4"
    spy_ytdlp.assert_called_once_with(url, "video", "video")
