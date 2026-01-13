from fastapi import APIRouter, Request, HTTPException
from src.services.queue_service import QueueService

router = APIRouter()
queue_service = QueueService()

@router.post("/evolution")
async def evolution_webhook(req: Request):
    try:
        payload = await req.json()
        queue_service.push(payload)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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