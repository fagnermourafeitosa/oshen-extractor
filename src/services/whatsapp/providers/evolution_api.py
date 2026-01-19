import logging
import httpx
from typing import Dict, Any
from src.core.config import settings

logger = logging.getLogger(__name__)

class EvolutionApi:
    """
    Infrastructure provider for interacting with the Evolution API.
    Handles low-level HTTP communication and timeouts.
    """
    def __init__(self):
        self.base_url = settings.EVOLUTION_API_URL.rstrip("/")
        self.headers = {
            "apikey": settings.EVOLUTION_API_KEY,
            "Content-Type": "application/json"
        }

    async def create_instance(self, instance_name: str) -> Dict[Any, Any]:
        url = f"{self.base_url}/instance/create"
        payload = {
            "instanceName": instance_name,
            "token": settings.OSHEN_EXTRACTOR_TOKEN,
            "qrcode": True
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=self.headers, timeout=10.0)
            response.raise_for_status()
            logger.info(f"Evolution API: Instance '{instance_name}' created.")
            return response.json()

    async def set_webhook(self, instance_name: str, target_url: str) -> Dict[Any, Any]:
        url = f"{self.base_url}/webhook/set/{instance_name}"
        payload = {
            "webhook": {
                "enabled": True,
                "url": target_url,
                "webhookByEvents": True,
                "events": ["MESSAGES_UPSERT"],
                "customHeaders": {
                    "x-token": settings.OSHEN_EXTRACTOR_TOKEN
                }
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=self.headers, timeout=10.0)
            response.raise_for_status()
            logger.info(f"Evolution API: Webhook set for {instance_name} at {target_url}")
            return response.json()

    async def send_callback(self, callback_url: str, data: Dict[str, Any]) -> None:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(callback_url, json=data, timeout=10.0)
                response.raise_for_status()
                logger.info(f"Evolution API: Callback successfully sent to {callback_url}")
            except Exception as e:
                logger.error(f"Evolution API: Callback failure to {callback_url}: {e}")
