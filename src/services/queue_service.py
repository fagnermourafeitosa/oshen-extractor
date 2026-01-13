import logging
import json
import redis
from src.core.config import settings

logger = logging.getLogger(__name__)

class QueueService:
    def __init__(self):
        self.r = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )
        self.queue_name = settings.WHATSAPP_REDIS_QUEUENAME
        logger.info(f"QueueService initialized for {self.queue_name} on {settings.REDIS_HOST}:{settings.REDIS_PORT}")

    def push(self, payload: dict) -> None:
        """
        Pushes the payload to the Redis queue.
        """
        try:
            result = self.r.lpush(self.queue_name, json.dumps(payload))
            logger.info(f"Pushed to {self.queue_name}. New length: {result}")
        except Exception as e:
            logger.error(f"Error pushing to queue {self.queue_name}: {e}")
            raise e
