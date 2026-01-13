import json
import redis
from src.core.config import settings

class QueueService:
    def __init__(self):
        self.r = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )
        self.queue_name = settings.WHATSAPP_REDIS_QUEUENAME

    def push(self, payload: dict) -> None:
        """
        Pushes the payload to the Redis queue.
        """
        try:
            self.r.lpush(self.queue_name, json.dumps(payload))
        except Exception as e:
            print(f"Error pushing to queue: {e}")
            raise e
