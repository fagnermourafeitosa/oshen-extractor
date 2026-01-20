import asyncio
import logging
import httpx
from src.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("webhook-config")

async def configure_evolution_webhook():
    if not settings.EVOLUTION_API_URL or not settings.EVOLUTION_API_KEY:
        logger.warning("Evolution API URL or Key not configured. Skipping webhook registration.")
        return

    if not settings.WEBHOOK_PUBLIC_URL:
        logger.warning("WEBHOOK_PUBLIC_URL not configured. Skipping webhook registration.")
        return

    instance_name = settings.DEFAULT_EVOLUTION_INSTANCE_NAME
    base_url = settings.EVOLUTION_API_URL.rstrip("/")
    headers = {
        "apikey": settings.EVOLUTION_API_KEY,
        "Content-Type": "application/json"
    }
    
    # 1. Check if instance exists (optional, but good practice)
    # For now, we assume instance exists or we just try to set the webhook directly.
    
    # 2. Configure Webhook
    webhook_url = f"{base_url}/webhook/set/{instance_name}"
    
    # Construct the webhook URL for THIS application
    # Ensure no double slashes
    target_url = settings.WEBHOOK_PUBLIC_URL.rstrip("/")
    if not target_url.endswith("/api/v1/whatsapp/webhook"):
        target_url += "/api/v1/whatsapp/webhook"

    data = {
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

    logger.info(f"Attempting to configure webhook for instance '{instance_name}' at {webhook_url}")
    logger.info(f"Target Webhook URL: {target_url}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(webhook_url, json=data, headers=headers, timeout=10.0)
            response.raise_for_status()
            logger.info(f"Webhook configured successfully! Response: {response.json()}")
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to configure webhook: {e.response.text}")
        except Exception as e:
            logger.error(f"An error occurred while configuring webhook: {e}")

if __name__ == "__main__":
    asyncio.run(configure_evolution_webhook())
