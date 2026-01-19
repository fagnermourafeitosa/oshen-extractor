import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock
from src.services.whatsapp.providers.evolution_api import EvolutionApi

@pytest.fixture
def api(mocker):
    # Patch settings to ensure consistent test environment
    mocker.patch("src.services.whatsapp.providers.evolution_api.settings.EVOLUTION_API_URL", "http://test-api")
    mocker.patch("src.services.whatsapp.providers.evolution_api.settings.EVOLUTION_API_KEY", "test-key")
    return EvolutionApi()

@pytest.mark.asyncio
async def test_should_create_instance_successfully(api, mocker):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": "inst-123"}
    
    mock_post = mocker.patch("httpx.AsyncClient.post", AsyncMock(return_value=mock_response))
    
    result = await api.create_instance("new-instance")
    
    assert result == {"id": "inst-123"}
    # Verify timeout and headers
    args, kwargs = mock_post.call_args
    assert kwargs["timeout"] == 10.0
    assert kwargs["headers"]["apikey"] == "test-key"

@pytest.mark.asyncio
async def test_should_raise_exception_on_api_failure(api, mocker):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError("Error", request=None, response=mock_response)
    
    mocker.patch("httpx.AsyncClient.post", AsyncMock(return_value=mock_response))
    
    with pytest.raises(Exception):
        await api.create_instance("fail")
