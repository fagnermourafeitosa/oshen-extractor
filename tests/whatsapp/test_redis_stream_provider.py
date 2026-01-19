import pytest
import json
from unittest.mock import MagicMock
from src.services.whatsapp.providers.redis_stream import RedisStream

def test_should_publish_message_to_redis_successfully(mocker):
    # Mock Redis class
    mock_redis_cls = mocker.patch("src.services.whatsapp.providers.redis_stream.redis.Redis")
    mock_redis_inst = mock_redis_cls.return_value
    
    provider = RedisStream()
    
    payload = {"message": "hello", "sender": "123"}
    provider.publish_message("test-instance", payload)
    
    # Verify xadd was called with correct stream name and payload
    mock_redis_inst.xadd.assert_called_once()
    args, kwargs = mock_redis_inst.xadd.call_args
    assert args[0] == "test-instance-whatsapp-messages"
    assert args[1] == {"payload": json.dumps(payload)}
    # Note: Code doesn't pass maxlen/approximate yet, but we'll accept the call

def test_should_raise_exception_on_redis_error(mocker):
    mock_redis_cls = mocker.patch("src.services.whatsapp.providers.redis_stream.redis.Redis")
    mock_redis_inst = mock_redis_cls.return_value
    mock_redis_inst.xadd.side_effect = Exception("Redis connection lost")
    
    provider = RedisStream()
    
    with pytest.raises(Exception) as exc:
        provider.publish_message("fail", {})
    
    assert "Redis connection lost" in str(exc.value)
