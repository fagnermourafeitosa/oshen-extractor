import pytest
import json
from unittest.mock import AsyncMock, MagicMock
from fastapi import Request, HTTPException
from src.services.whatsapp.use_cases.process_webhook import ProcessWebhookUseCase

@pytest.fixture
def use_case():
    return ProcessWebhookUseCase()

@pytest.fixture
def mock_stream(mocker):
    return mocker.patch("src.services.whatsapp.use_cases.process_webhook.RedisStream")

def create_mock_request(payload):
    request = MagicMock(spec=Request)
    request.json = AsyncMock(return_value=payload)
    return request

@pytest.mark.asyncio
async def test_should_process_valid_message_upsert_and_push_to_stream(mocker):
    use_case = ProcessWebhookUseCase()
    mock_stream_instance = MagicMock()
    use_case.stream = mock_stream_instance
    
    payload = {
        "event": "messages.upsert",
        "instance": "inst-123",
        "data": {
            "key": {"remoteJid": "12345@s.whatsapp.net"},
            "pushName": "User",
            "message": {"conversation": "Hello world!"},
            "messageTimestamp": 1600000000
        }
    }
    req = create_mock_request(payload)
    
    result = await use_case.execute(req)
    
    assert result == {"ok": True}
    mock_stream_instance.publish_message.assert_called_once()
    call_args = mock_stream_instance.publish_message.call_args[0]
    assert call_args[0] == "inst-123"
    assert call_args[1]["message"] == "Hello world!"

@pytest.mark.asyncio
async def test_should_ignore_supported_events(mocker):
    use_case = ProcessWebhookUseCase()
    mock_stream_instance = MagicMock()
    use_case.stream = mock_stream_instance
    
    payload = {"event": "other.event", "data": {}}
    req = create_mock_request(payload)
    
    result = await use_case.execute(req)
    
    assert result == {"ignored": True}
    mock_stream_instance.publish_message.assert_not_called()

@pytest.mark.asyncio
async def test_should_ignore_messages_without_content_or_media(mocker):
    use_case = ProcessWebhookUseCase()
    mock_stream_instance = MagicMock()
    use_case.stream = mock_stream_instance
    
    payload = {
        "event": "messages.upsert",
        "data": {"message": {}} # Empty message
    }
    req = create_mock_request(payload)
    
    result = await use_case.execute(req)
    
    assert result == {"ignored": True}
    mock_stream_instance.publish_message.assert_not_called()

@pytest.mark.asyncio
async def test_should_raise_exception_on_invalid_json(mocker):
    use_case = ProcessWebhookUseCase()
    req = MagicMock(spec=Request)
    req.json = AsyncMock(side_effect=Exception("Invalid JSON"))
    
    with pytest.raises(HTTPException) as exc:
        await use_case.execute(req)
    assert exc.value.status_code == 400
