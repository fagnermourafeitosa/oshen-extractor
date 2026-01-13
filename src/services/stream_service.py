import logging
import json
import redis
from src.core.config import settings

logger = logging.getLogger(__name__)

class StreamService:
    def __init__(self):
        self.r = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )
        self.queue_name = settings.WHATSAPP_REDIS_STREAM
        logger.info(f"StreamService initialized for {self.queue_name} on {settings.REDIS_HOST}:{settings.REDIS_PORT}")

    def push(self, payload: dict) -> None:
        """
        Pushes the payload to the Redis stream.
        """
        try:
            # Redis Streams expectation for fields: value
            result = self.r.xadd(self.queue_name, {"payload": json.dumps(payload)})
            logger.info(f"Pushed to stream {self.queue_name}. New message ID: {result}")
        except Exception as e:
            logger.error(f"Error pushing to stream {self.queue_name}: {e}")
            raise e
