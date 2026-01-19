import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException, BackgroundTasks
from src.services.whatsapp.use_cases.register_instance import RegisterInstanceUseCase

@pytest.fixture
def use_case():
    return RegisterInstanceUseCase()

@pytest.fixture
def mock_api(mocker):
    return mocker.patch("src.services.whatsapp.use_cases.register_instance.EvolutionApi")

@pytest.mark.asyncio
async def test_should_register_instance_sequentially_and_trigger_callback(mocker):
    # Instantiate use case first
    use_case = RegisterInstanceUseCase()
    
    # Mock the internal api attribute directly
    mock_api_instance = AsyncMock()
    use_case.api = mock_api_instance
    
    mock_api_instance.create_instance = AsyncMock(return_value={"id": "123"})
    mock_api_instance.set_webhook = AsyncMock()
    mock_api_instance.send_callback = AsyncMock()
    
    background_tasks = MagicMock(spec=BackgroundTasks)
    
    # Execute
    result = await use_case.execute(
        instance_name="test-instance",
        callback_url="https://callback.com",
        background_tasks=background_tasks
    )
    
    # Assertions
    assert result["status"] == "success"
    mock_api_instance.create_instance.assert_called_once_with("test-instance")
    mock_api_instance.set_webhook.assert_called_once()
    background_tasks.add_task.assert_called_once()
    
    # Verify the callback was added with the correct data
    callback_call = background_tasks.add_task.call_args
    assert callback_call[0][0] == mock_api_instance.send_callback
    assert callback_call[0][1] == "https://callback.com"
    assert callback_call[0][2]["status"] == "success"

@pytest.mark.asyncio
async def test_should_raise_http_exception_when_api_creation_fails(mocker):
    use_case = RegisterInstanceUseCase()
    mock_api_instance = AsyncMock()
    use_case.api = mock_api_instance
    
    mock_api_instance.create_instance = AsyncMock(side_effect=Exception("API Error"))
    
    background_tasks = MagicMock(spec=BackgroundTasks)
    
    # Execute and Assert
    with pytest.raises(HTTPException) as exc:
        await use_case.execute("fail-instance", "https://url.com", background_tasks)
    
    assert exc.value.status_code == 400
    assert "API Error" in str(exc.value.detail)
