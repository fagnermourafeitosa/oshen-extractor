import pytest
from unittest.mock import MagicMock
from src.services.instagram_service import InstagramService
from src.services.tiktok_service import TikTokService
from src.services.youtube_service import YouTubeService

@pytest.fixture
def mock_ydl(mocker):
    return mocker.patch("yt_dlp.YoutubeDL")

def test_instagram_download(mock_ydl):
    service = InstagramService()
    url = "https://instagram.com/p/123"
    name = "test-post"
    
    # Configure mock
    mock_instance = mock_ydl.return_value.__enter__.return_value
    mock_instance.extract_info.return_value = {}
    mock_instance.prepare_filename.return_value = "downloads/test-post-12345.mp4"
    
    result = service.download(url, name)
    
    assert result == "downloads/test-post-12345.mp4"
    mock_instance.extract_info.assert_called_once_with(url, download=True)

def test_tiktok_download(mocker):
    service = TikTokService()
    url = "https://tiktok.com/@user/video/123"
    name = "test-video"
    
    # Mock httpx.Client
    mock_response_api = MagicMock()
    mock_response_api.json.return_value = {
        "code": 0,
        "msg": "success",
        "data": {"play": "https://example.com/video.mp4"}
    }
    mock_response_api.raise_for_status = MagicMock()
    
    mock_response_video = MagicMock()
    mock_response_video.content = b"fake-video-content"
    mock_response_video.raise_for_status = MagicMock()
    
    mock_client = mocker.patch("httpx.Client")
    mock_client_instance = mock_client.return_value.__enter__.return_value
    mock_client_instance.get.side_effect = [mock_response_api, mock_response_video]
    
    # Mock open and os.makedirs
    mocker.patch("os.makedirs")
    mock_open = mocker.patch("builtins.open", mocker.mock_open())
    
    result = service.download(url, name)
    
    assert "test-video" in result
    assert result.endswith(".mp4")
    assert mock_client_instance.get.call_count == 2

def test_youtube_download_video(mock_ydl):
    service = YouTubeService()
    url = "https://youtube.com/watch?v=123"
    name = "test-yt"
    
    mock_instance = mock_ydl.return_value.__enter__.return_value
    mock_instance.extract_info.return_value = {}
    mock_instance.prepare_filename.return_value = "downloads/test-yt-12345.mp4"
    
    result = service.download(url, name, "video")
    
    assert result == "downloads/test-yt-12345.mp4"
    mock_instance.extract_info.assert_called_once_with(url, download=True)

def test_youtube_download_audio(mock_ydl):
    service = YouTubeService()
    url = "https://youtube.com/watch?v=123"
    name = "test-audio"
    
    mock_instance = mock_ydl.return_value.__enter__.return_value
    mock_instance.extract_info.return_value = {}
    mock_instance.prepare_filename.return_value = "downloads/test-audio-12345.m4a" 
    
    result = service.download(url, name, "audio")
    
    # Check if extension was changed to mp3 (as per logic)
    assert result == "downloads/test-audio-12345.mp3"
    mock_instance.extract_info.assert_called_once_with(url, download=True)
