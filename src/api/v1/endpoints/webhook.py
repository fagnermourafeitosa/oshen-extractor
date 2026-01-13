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
    message = message_obj.get("conversation") or \
              message_obj.get("extendedTextMessage", {}).get("text")

    if not message:
        logger.info(f"No message content found. Message keys: {list(message_obj.keys())}")
        if is_group:
            logger.info(f"DEBUG GROUP PAYLOAD: {json.dumps(data)}")
        return {"ignored": True}

    logger.info(f"Processing message from {data.get('pushName')}: {message[:50]}...")

    stream_service.push({
        "group_id": data.get("key", {}).get("remoteJid"),
        "group_name": data.get("pushName"),
        "message": message,
        "timestamp": data.get("messageTimestamp"),
        "raw": payload  # Enviamos o payload bruto completo conforme solicitado
    })

    return {"ok": True}        