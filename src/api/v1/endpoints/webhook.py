import logging
import json
from fastapi import APIRouter, Request, HTTPException
from src.services.stream_service import StreamService
from src.core.config import settings

logger = logging.getLogger(__name__)


router = APIRouter()
stream_service = StreamService()

@router.post("")
async def evolution_webhook(req: Request):
    payload = await req.json()
    event = payload.get("event", "").upper()
    logger.info(f"Received webhook payload event: {payload.get('event')}")

    if event not in ["MESSAGES_UPSERT", "MESSAGES.UPSERT"]:
        logger.info(f"Ignoring event type: {payload.get('event')}")
        return {"ignored": True}

    data = payload.get("data", {})
    message_obj = data.get("message", {})
    
    remote_jid = data.get("key", {}).get("remoteJid", "")
    is_group = "@g.us" in remote_jid
    
    if is_group:
        logger.info(f"Group message detected from {remote_jid}")

    # Extrai o texto de diferentes formatos possíveis da Evolution API
    base_message = message_obj.get("ephemeralMessage", {}).get("message", message_obj)
    
    # Tenta extrair texto de vários lugares comuns
    message = (
        base_message.get("conversation") or 
        base_message.get("extendedTextMessage", {}).get("text") or 
        base_message.get("imageMessage", {}).get("caption") or 
        base_message.get("videoMessage", {}).get("caption")
    )
    
    image_msg = base_message.get("imageMessage", {})
    video_msg = base_message.get("videoMessage", {})
    media_msg = image_msg or video_msg
    
    media_url = media_msg.get("url")
    
    # Extração de Metadados Técnicos
    media_metadata = {}
    if media_msg:
        media_metadata = {
            "mime_type": media_msg.get("mimetype"),
            "file_checksum": media_msg.get("fileSha256"),
            "media_decryption_key": media_msg.get("mediaKey"),
            "thumbnail_raw": media_msg.get("jpegThumbnail")
        }

    if not message and not media_url:
        logger.info(f"No message content found. Message keys: {list(message_obj.keys())}")
        if is_group:
            logger.info(f"DEBUG GROUP PAYLOAD: {json.dumps(data)}")
        return {"ignored": True}

    logger.info(f"Processing message from {data.get('pushName')}: {message[:50]}...")

    push_data = {
        "group_id": data.get("key", {}).get("remoteJid"),
        "group_name": data.get("pushName"),
        "message": message,
        "media_url": media_url,
        "timestamp": data.get("messageTimestamp"),
        **media_metadata, # Espalha os metadados (mime_type, checksum, key, thumbnail)
        "raw": payload # Payload bruto para garantir
    }
    
    stream_service.push(push_data)

    return {"ok": True}        