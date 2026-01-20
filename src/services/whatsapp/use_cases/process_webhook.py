import logging
from typing import Dict, Any, Optional
from fastapi import Request, HTTPException
from src.services.whatsapp.providers.redis_stream import RedisStream

logger = logging.getLogger(__name__)

class ProcessWebhookUseCase:
    """
    Application use case to process incoming webhooks from Evolution API.
    Handles: Parsing -> Data Extraction/Structuring -> Redis Streaming.
    """
    def __init__(self):
        self.stream = RedisStream()

    async def execute(self, request: Request) -> Dict[str, Any]:
        try:
            payload = await request.json()
            logger.info(f"Webhook received: {payload}")
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid JSON")

        processed_data = self._parse_payload(payload)
        
        if not processed_data:
            logger.warning("Webhook ignored (irrelevant event or empty data)")
            return {"ignored": True}

        instance_name = processed_data.get("instance_name")
        self.stream.publish_message(instance_name, processed_data)
        
        return {"ok": True}

    def _parse_payload(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Internal logic to map raw Evolution payload to internal structure.
        """
        event = payload.get("event", "").upper()
        if event not in ["MESSAGES_UPSERT", "MESSAGES.UPSERT"]:
            return None

        data = payload.get("data", {})
        instance_name = payload.get("instance")
        
        message_obj = data.get("message", {})
        base_message = message_obj.get("ephemeralMessage", {}).get("message", message_obj)
        
        # Content Extraction
        message_text = (
            base_message.get("conversation") or 
            base_message.get("extendedTextMessage", {}).get("text") or 
            base_message.get("imageMessage", {}).get("caption") or 
            base_message.get("videoMessage", {}).get("caption")
        )
        
        media_msg = base_message.get("imageMessage") or base_message.get("videoMessage")
        media_url = media_msg.get("url") if media_msg else None
        
        media_metadata = {}
        if media_msg:
            media_metadata = {
                "mime_type": media_msg.get("mimetype"),
                "file_checksum": media_msg.get("fileSha256"),
                "media_decryption_key": media_msg.get("mediaKey"),
                "thumbnail_raw": media_msg.get("jpegThumbnail")
            }

        if not message_text and not media_url:
            return None

        return {
            "instance_name": instance_name,
            "group_id": data.get("key", {}).get("remoteJid"),
            "group_name": data.get("pushName"),
            "message": message_text,
            "media_url": media_url,
            "timestamp": data.get("messageTimestamp"),
            **media_metadata,
            "raw": payload
        }
