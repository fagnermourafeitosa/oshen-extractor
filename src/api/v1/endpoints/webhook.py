from fastapi import APIRouter, Request, HTTPException
from src.services.queue_service import QueueService
from src.core.config import settings

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
queue_service = QueueService()

QUEUE_KEY = settings.WHATSAPP_REDIS_QUEUENAME

@router.post("")
async def evolution_webhook(req: Request):
    payload = await req.json()

    if payload.get("event") != "MESSAGES_UPSERT":
        return {"ignored": True}

    data = payload.get("data", {})
    message = data.get("message", {}).get("conversation")

    if not message:
        return {"ignored": True}

    queue_service.push({
        "group_id": data["key"]["remoteJid"],
        "group_name": data.get("pushName"),
        "message": message,
        "timestamp": data.get("messageTimestamp")
    })

    return {"ok": True}        