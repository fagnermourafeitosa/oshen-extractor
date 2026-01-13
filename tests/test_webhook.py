from unittest.mock import MagicMock
from src.core.config import settings

def test_webhook_evolution_success(client, mocker):
    # Mock the push method of the queue_service instance imported in webhook module
    mock_push = mocker.patch("src.api.v1.endpoints.webhook.queue_service.push")
    
    payload = {"event": "test", "data": "value"}
    headers = {"x-token": settings.OSHEN_EXTRACTOR_TOKEN}
    
    response = client.post("/webhook/evolution", json=payload, headers=headers)
    
    assert response.status_code == 200
    assert response.json() == {"ok": True}
    mock_push.assert_called_once_with(payload)

def test_webhook_evolution_unauthorized(client, mocker):
    mock_push = mocker.patch("src.api.v1.endpoints.webhook.queue_service.push")
    payload = {"event": "test"}
    
    # Missing header
    response = client.post("/webhook/evolution", json=payload)
    assert response.status_code == 422
    mock_push.assert_not_called()
    
    # Invalid header
    response = client.post("/webhook/evolution", json=payload, headers={"x-token": "wrong-token"})
    assert response.status_code == 401
    mock_push.assert_not_called()

def test_webhook_evolution_redis_error(client, mocker):
    mock_push = mocker.patch("src.api.v1.endpoints.webhook.queue_service.push")
    mock_push.side_effect = Exception("Connection refused")
    
    payload = {"event": "test"}
    headers = {"x-token": settings.OSHEN_EXTRACTOR_TOKEN}
    
    response = client.post("/webhook/evolution", json=payload, headers=headers)
    
    assert response.status_code == 500
    # Check if detail contains exception message
    assert "Connection refused" in response.json()["detail"]
