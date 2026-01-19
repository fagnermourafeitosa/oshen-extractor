import pytest
import os
import httpx
from unittest.mock import MagicMock, mock_open
from src.services.social_networks.providers.ytdlp_provider import YtDlpProvider
from src.services.social_networks.providers.tikwm_provider import TikWmProvider

@pytest.fixture
def mock_ydl(mocker):
    return mocker.patch("yt_dlp.YoutubeDL")

def test_ytdlp_provider_should_download_video_correctly(mock_ydl):
    provider = YtDlpProvider(download_dir="test_downloads")
    
    mock_instance = mock_ydl.return_value.__enter__.return_value
    mock_instance.extract_info.return_value = {}
    mock_instance.prepare_filename.return_value = "test_downloads/video.mp4"
    
    result = provider.download("https://site.com", "file", "video")
    
    assert result == "test_downloads/video.mp4"
    mock_instance.extract_info.assert_called_once()

def test_ytdlp_provider_should_handle_audio_conversion_extension(mock_ydl):
    provider = YtDlpProvider(download_dir="test_downloads")
    
    mock_instance = mock_ydl.return_value.__enter__.return_value
    mock_instance.extract_info.return_value = {}
    mock_instance.prepare_filename.return_value = "test_downloads/audio.m4a"
    
    result = provider.download("https://site.com", "file", "audio")
    
    # Logic in YtDlpProvider forces .mp3 for audio format
    assert result == "test_downloads/audio.mp3"

def test_tikwm_provider_should_call_api_and_download_file(mocker):
    provider = TikWmProvider(download_dir="test_downloads")
    
    # Mock httpx
    mock_response_api = MagicMock()
    mock_response_api.json.return_value = {"code": 0, "data": {"play": "http://cdn.com/vid.mp4"}}
    mock_response_video = MagicMock()
    mock_response_video.content = b"bytes"
    
    mock_client = mocker.patch("httpx.Client")
    mock_client_inst = mock_client.return_value.__enter__.return_value
    mock_client_inst.get.side_effect = [mock_response_api, mock_response_video]
    
    mocker.patch("builtins.open", mock_open())
    mocker.patch("os.makedirs")
    
    result = provider.download_no_watermark("https://tiktok.com", "video")
    
    assert ".mp4" in result
    assert "video" in result
    assert mock_client_inst.get.call_count == 2
