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
        #composed by instance name + '-whatsapp-messages'
        self.queue_name_suffix = '-whatsapp-messages'
        logger.info(f"StreamService initialized for {self.queue_name} on {settings.REDIS_HOST}:{settings.REDIS_PORT}")

    def push(self, payload: dict) -> None:
        """
        Pushes the payload to the Redis stream.
        """
        try:
            #TODO extract instance name from payload
            #use default for now..
            instance_name = settings.DEFAULT_EVOLUTION_INSTANCE_NAME
            queue_name = self.queue_name(instance_name)

            # Redis Streams expectation for fields: value
            result = self.r.xadd(queue_name, {"payload": json.dumps(payload)})
            logger.info(f"Pushed to stream {queue_name}. New message ID: {result}")
        except Exception as e:
            logger.error(f"Error pushing to stream {queue_name}: {e}")
            raise e
    
    @property
    def queue_name(self, instance_name: str):
        #TODO should be replaced by instance name that coming from each message
        return f"{instance_name}{self.queue_name_suffix}"