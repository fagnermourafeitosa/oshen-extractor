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

def test_tiktok_download(mock_ydl):
    service = TikTokService()
    url = "https://tiktok.com/@user/video/123"
    name = "test-video"
    
    mock_instance = mock_ydl.return_value.__enter__.return_value
    mock_instance.extract_info.return_value = {}
    mock_instance.prepare_filename.return_value = "downloads/test-video-12345.mp4"
    
    result = service.download(url, name)
    
    assert result == "downloads/test-video-12345.mp4"
    mock_instance.extract_info.assert_called_once_with(url, download=True)

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
