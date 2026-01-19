import logging
import json
import redis
from src.core.config import settings

logger = logging.getLogger(__name__)

class RedisStream:
    """
    Infrastructure provider for Redis Stream operations.
    Handles connection and raw data publishing.
    """
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )
        self.suffix = '-whatsapp-messages'

    def publish_message(self, instance_name: str, data: dict) -> str:
        queue_name = f"{instance_name or settings.DEFAULT_EVOLUTION_INSTANCE_NAME}{self.suffix}"
        try:
            message_id = self.client.xadd(queue_name, {"payload": json.dumps(data)})
            logger.info(f"Redis Stream: Published to {queue_name} (ID: {message_id})")
            return str(message_id)
        except Exception as e:
            logger.error(f"Redis Stream: Error publishing to {queue_name}: {e}")
            raise e
