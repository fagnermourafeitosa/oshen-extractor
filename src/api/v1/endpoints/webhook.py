import logging
from fastapi import APIRouter, Request, HTTPException
from src.services.stream_service import StreamService
from src.core.config import settings

logger = logging.getLogger(__name__)

# Só DEVE:
# validar
# enqueue
# responder 200
# payload REAL completo da Evolution (mensagem de grupo)

# Campos que importam pra você:
# remoteJid → ID do grupo
# pushName → nome do grupo
# message.conversation → texto cru

# messageTimestamp
# {
#   "event": "MESSAGES_UPSERT",
#   "instance": "instance-01",
#   "data": {
#     "key": {
#       "remoteJid": "1203630XXXXX@g.us",
#       "fromMe": false,
#       "id": "3EB0C8F9..."
#     },
#     "pushName": "Grupo de Achadinhos ADM 2",
#     "messageTimestamp": 1736671743,
#     "message": {
#       "conversation": "Ricca Escova Raquete Flex Red\n\nPOR R$ 22,37\nCompre aqui: https://amzn.to/xxxx"
#     }
#   }
# }
# validação de assinatura (se quiser segurança)


# Exemplo de Enfileiramento (Lógica que vai no FastAPI/Producer):
# Quando enviar para o Redis, o BullMQ espera esse padrão de retry:
# job_options = {
#     "attempts": 5,                # Tenta 5 vezes antes de mandar para o DLQ
#     "backoff": {
#         "type": "exponential",    # Espera cada vez mais tempo entre tentativas
#         "delay": 2000             # Começa com 2 segundos (2s, 4s, 8s, 16s...)
#     },
#     "removeOnComplete": True      # Limpa o Redis ao terminar (performance)
# }

# maxRetriesPerRequest: null: O BullMQ gerencia as reconexões do Redis internamente; se você não colocar isso, o ioredis mata o processo.

# concurrency: Como o seu processamento é I/O (esperar o NestJS responder), você pode subir esse número para processar centenas de mensagens por segundo sem suar.

# SIGTERM / SIGINT: Quando você der um docker compose down ou deployar na Hostinger, o worker avisa o Redis: "Terminei o que estava fazendo, agora pode me desligar". Sem isso, mensagens no meio do parsing somem.

router = APIRouter()
stream_service = StreamService()

QUEUE_KEY = settings.WHATSAPP_REDIS_STREAM

@router.post("")
async def evolution_webhook(req: Request):
    payload = await req.json()
    logger.info(f"Received webhook payload event: {payload.get('event')}")

    if payload.get("event") != "MESSAGES_UPSERT":
        logger.info(f"Ignoring event type: {payload.get('event')}")
        return {"ignored": True}

    data = payload.get("data", {})
    message_obj = data.get("message", {})
    
    # Extrai o texto de diferentes formatos possíveis da Evolution API
    message = message_obj.get("conversation") or \
              message_obj.get("extendedTextMessage", {}).get("text")

    if not message:
        logger.info(f"No message content found in payload data: {data}")
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