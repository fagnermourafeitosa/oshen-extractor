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
        print(f"DEBUG: QueueService initialized for {self.queue_name} on {settings.REDIS_HOST}:{settings.REDIS_PORT}")

    def push(self, payload: dict) -> None:
        """
        Pushes the payload to the Redis queue.
        """
        try:
            result = self.r.lpush(self.queue_name, json.dumps(payload))
            print(f"DEBUG: Pushed to {self.queue_name}. New length: {result}")
        except Exception as e:
            print(f"DEBUG: Error pushing to queue {self.queue_name}: {e}")
            raise e
