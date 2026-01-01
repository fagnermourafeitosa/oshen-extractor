import pytest
import os
from unittest.mock import MagicMock

def test_download_instagram_endpoint(client, mocker, tmp_path):
    # Create a dummy file in a temp directory
    d = tmp_path / "downloads"
    d.mkdir()
    p = d / "sample.mp4"
    p.write_text("dummy content")
    
    file_path = str(p)

    mock_service = mocker.patch("src.api.v1.endpoints.instagram.service")
    mock_service.download.return_value = file_path
    
    # Do NOT mock os.path.isfile or os.stat, let FileResponse use the real temp file

    response = client.post(
        "/api/v1/instagram/download",
        json={"url": "http://instagram.com/p/123", "name": "insta-test"}
    )
    
    # Verify response
    assert response.status_code == 200
    # FileResponse usually sets content-type based on media_type arg or guessing. 
    # In endpoint we explicitly set 'application/octet-stream'
    assert response.headers["content-type"] == "application/octet-stream"
    mock_service.download.assert_called_once_with("http://instagram.com/p/123", "insta-test")

def test_download_tiktok_endpoint(client, mocker, tmp_path):
    d = tmp_path / "downloads"
    d.mkdir()
    p = d / "sample_tk.mp4"
    p.write_text("dummy content")
    file_path = str(p)

    mock_service = mocker.patch("src.api.v1.endpoints.tiktok.service")
    mock_service.download.return_value = file_path
    
    response = client.post(
        "/api/v1/tiktok/download",
        json={"url": "http://tiktok.com/v/123", "name": "tiktok-test"}
    )
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "video/mp4"
    mock_service.download.assert_called_once_with("http://tiktok.com/v/123", "tiktok-test")

def test_download_youtube_endpoint(client, mocker, tmp_path):
    d = tmp_path / "downloads"
    d.mkdir()
    p = d / "sample_yt.mp4"
    p.write_text("dummy content")
    file_path = str(p)

    mock_service = mocker.patch("src.api.v1.endpoints.youtube.service")
    mock_service.download.return_value = file_path
    
    response = client.post(
        "/api/v1/youtube/download",
        json={"url": "http://youtube.com/w/123", "name": "yt-test", "format_type": "video"}
    )
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "video/mp4"
    mock_service.download.assert_called_once_with("http://youtube.com/w/123", "yt-test", "video")
